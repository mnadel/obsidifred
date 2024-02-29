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

def ripgrep_search(basedir, needle):
	match_list = []

	p = subprocess.run(["rg", "-lS", needle, basedir], capture_output=True)
	if p.returncode != 0:
		sys.exit(p.returncode)
	for file in [x for x in p.stdout.decode().split("\n") if x.lower().endswith(".md")]:
		_, filename = os.path.split(file)
		relpath = file.removeprefix(basedir)[1:]
		intermediate = relpath.removesuffix(filename)[:-1]
		match_list.append({
			"title": filename[:-3],
			"subtitle": intermediate,
			"arg": os.path.join("./", relpath)
		})

	return match_list

def contains(fpath, term):
	if os.path.getsize(fpath) < 1:
		return False

	with open(fpath, mode="r", encoding="utf-8") as f:
		if case_sensitive:
			s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
			return s.find(term) != -1
		else:
			return term.lower() in f.read().lower()

def native_search(basedir, needle):
	match_list = []

	for root, dirs, files in os.walk(basedir):
		for file in files:
			if file.lower().endswith(".md"):
				fpath = os.path.join(root, file)
				if contains(fpath, needle):
					relpath = root[len(basedir)+1:]
					match_list.append({
						"title": file[:-3],
						"subtitle": relpath,
						"arg": os.path.join("./", relpath, file)
					})
	
	return match_list

def searcher():
	return ripgrep_search if use_ripgrep else native_search

print(json.dumps({"items": searcher()(basedir, needle)}))
