#! /usr/bin/env python3

import sys

sepChar = "#"
sepInChar = ":"
nullChar = "@"

reverse = (len(sys.argv) >= 2 and sys.argv[1] == "-rev")

for line in sys.stdin:
	if "NO ALIGNMENT" in line:
		sys.stdout.write("\n")
		continue
	elements = line.strip().split("\t")
	if reverse:
		src = elements[1].strip()
		tgt = elements[0].strip()
	else:
		src = elements[0].strip()
		tgt = elements[1].strip()
	src_chunks = [x for x in src.split(sepChar) if x != ""]
	tgt_chunks = [x for x in tgt.split(sepChar) if x != ""]
	alignments = []
	srcid, tgtid = 0, 0
	for src_chunk, tgt_chunk in zip(src_chunks, tgt_chunks):
		if src_chunk == nullChar:
			tgtid += 1
			# no alignment
		elif tgt_chunk == nullChar:
			srcid += 1
			# no alignment
		else:
			if sepInChar in src_chunk and sepInChar in tgt_chunk:
				src_elem = src_chunk.split(sepInChar)
				tgt_elem = tgt_chunk.split(sepInChar)
				assert(len(src_elem) == len(tgt_elem) and len(src_elem) == 2)
				if src_elem[0] == tgt_elem[0] or src_elem[1] == tgt_elem[1]:
					alignments.append((srcid, tgtid))
					alignments.append((srcid+1, tgtid+1))
				elif src_elem[0] == tgt_elem[1] or src_elem[1] == tgt_elem[0]:
					#print("Swap detected:", src_chunk, "<=>", tgt_chunk)
					alignments.append((srcid+1, tgtid))
					alignments.append((srcid, tgtid+1))
				else:
					alignments.append((srcid, tgtid))
					alignments.append((srcid+1, tgtid+1))
				srcid += 2
				tgtid += 2
			elif sepInChar in src_chunk:
				for i in range(src_chunk.count(sepInChar)+1):
					alignments.append((srcid, tgtid))
					srcid += 1
				tgtid += 1
			elif sepInChar in tgt_chunk:
				for i in range(tgt_chunk.count(sepInChar)+1):
					alignments.append((srcid, tgtid))
					tgtid += 1
				srcid += 1
			else:
				alignments.append((srcid, tgtid))
				srcid += 1
				tgtid += 1
	sys.stdout.write(" ".join(["{}-{}".format(a[0], a[1]) for a in alignments]) + "\n")
