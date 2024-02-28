#!/usr/bin/env python3

import os
import sys
import mmap
import json

case_insensitive = "case_insensitive" in os.environ
basedir = os.environ["vault_path"]
needle = " ".join(sys.argv[1:]) if case_insensitive else str.encode(" ".join(sys.argv[1:]))

if "debug" in os.environ:
	print("searching", basedir, "for", needle, file=sys.stderr)

match_list = []

if len(needle) < 3:
	print(json.dumps({"items": []}))
	sys.exit(0)

def matches(fpath):
	if os.path.getsize(fpath) < 1:
		return False

	with open(fpath, mode="r", encoding="utf-8") as f:
		if case_insensitive:
			return needle.lower() in f.read().lower()
		else:
			s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
			return s.find(needle) != -1

for root, dirs, files in os.walk(basedir):
	for file in files:
		if file.endswith(".md"):
			fpath = os.path.join(root, file)
			if matches(fpath):
				relpath = root[len(basedir)+1:]
				match_list.append({
					"title": file[:-3],
					"subtitle": relpath,
					"arg": os.path.join("./", relpath, file)
				})

print(json.dumps({"items": match_list}))
