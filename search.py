#!/usr/bin/env python3

import os
import sys
import mmap
import json
import subprocess

use_ripgrep = "ripgrep" in os.environ
basedir = os.environ["vault_path"]
term = " ".join(sys.argv[1:])
case_sensitive = term.lower() != term # use smart case searching (if there's an uppercase letter then it's case sensitive)
needle = str.encode(term) if case_sensitive else term

if "debug" in os.environ:
	print("searching", basedir, "for", needle, file=sys.stderr)

match_list = []

def contains(fpath, term):
	if os.path.getsize(fpath) < 1:
		return False

	with open(fpath, mode="r", encoding="utf-8") as f:
		if case_sensitive:
			s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
			return s.find(term) != -1
		else:
			return term.lower() in f.read().lower()

if use_ripgrep:
	p = subprocess.run(["rg", "-lS", needle, basedir], capture_output=True)
	if p.returncode != 0:
		sys.exit(p.returncode)
	for file in [x for x in p.stdout.decode().split("\n") if len(x) > 0]:
		dirname, filename = os.path.split(file)
		relpath = file.removeprefix(basedir)[1:]
		relintermediate = relpath.removesuffix(filename)[:-1]
		match_list.append({
			"title": filename[:-3],
			"subtitle": relintermediate,
			"arg": os.path.join("./", relpath)
		})
else:
	for root, dirs, files in os.walk(basedir):
		for file in files:
			if file.endswith(".md"):
				fpath = os.path.join(root, file)
				if contains(fpath, needle):
					relpath = root[len(basedir)+1:]
					match_list.append({
						"title": file[:-3],
						"subtitle": relpath,
						"arg": os.path.join("./", relpath, file)
					})

print(json.dumps({"items": match_list}))
