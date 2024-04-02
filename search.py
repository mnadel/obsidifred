#!/usr/bin/env python3

import os
import sys
import json
import subprocess

basedir = os.environ["vault_path"]
query = " ".join(sys.argv[1:])

def rg(basedir, needle):
	p = subprocess.run(["rg", "--no-ignore-vcs", "--type", "md", "-lS", needle, basedir], capture_output=True)
	if p.returncode != 0:
		return []
	
	match_list = []

	for file in [x for x in p.stdout.decode().split("\n") if len(x) > 0]:
		_, filename = os.path.split(file)
		relpath = file.removeprefix(basedir)[1:]
		intermediate = relpath.removesuffix(filename)[:-1]
		match_list.append({
			"title": filename[:-3],
			"subtitle": intermediate,
			"arg": os.path.join("./", relpath)
		})

	return match_list

def search_titles(basedir, needle):
	match_list = []

	for root, dirs, files in os.walk(basedir):
		for file in files:
			if file.lower().endswith(".md"):
				fpath = os.path.join(root, file)
				if  needle.lower() in fpath.lower():
					relpath = root[len(basedir)+1:]
					match_list.append({
						"title": file[:-3],
						"subtitle": relpath,
						"arg": os.path.join("./", relpath, file)
					})
	
	return match_list

def search(basedir, query):
	terms = query.split(" ")
    # map of filename to alfred json object
	matches = {}
    # map of filename to number of terms matched
	counts = {}

	for term in terms:
		for match in rg(basedir, term) + search_titles(basedir, term):
			k = match["arg"]
			matches[k] = match
			if k in counts:
				counts[k] = counts[k] + 1
			else:
				counts[k] = 1
	
    # return a list of alfred objects that which matched all our terms
	return [v for k,v in matches.items() if counts[k] >= len(terms)]

print(json.dumps({"items": search(basedir, query)}))
