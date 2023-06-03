#! /usr/bin/env python3

import os

def mkdirp(path):
	try:
		os.mkdir(path)
	except FileExistsError:
		pass

def writeCSMT(folder, fileid, data):
	mkdirp(f"{folder}")
	f_orig = open(f"{folder}/{fileid}.orig", "w")
	f_norm = open(f"{folder}/{fileid}.norm", "w")
	for sent_orig, sent_norm in data:
		orig = [" ".join(list(w.replace(" ", "_"))) for w in sent_orig]
		orig = "_ " + " _ ".join(orig) + " _"
		f_orig.write(orig + "\n")
		norm = [" ".join(list(w.replace(" ", "_"))) for w in sent_norm]
		norm = "_ " + " _ ".join(norm) + " _"
		f_norm.write(norm + "\n")
	f_orig.close()
	f_norm.close()
	print(f"{len(data)} utterances written to {folder}/{fileid}.*")
