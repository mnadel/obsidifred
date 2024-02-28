#!/usr/bin/env python3

import os
import sys
import mmap
import json

basedir = os.environ["vault_path"]
needle = str.encode(" ".join(sys.argv[1:]))

print("searching", basedir, "for", needle, file=sys.stderr)

match_list = []

if len(needle) < 3:
	print(json.dumps({"items": []}))
	sys.exit(0)

def matches(fpath):
	with open(fpath, mode="r", encoding="utf-8") as f:
		if os.path.getsize(fpath) < 1:
			return False
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
