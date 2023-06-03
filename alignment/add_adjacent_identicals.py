#! /usr/bin/env python

import sys, os

# adds alignment points based on identity, both on source and target sides, both rightwards and leftwards:

# A A       A A
# | .   ==> | /
# B         B  

# A A       A A
# . |   ==> \ |
#   B         B

# A         A  
# | .   ==> | \
# B B       B B

#   A         A
# . |   ==> / |
# B B       B B


srcfile = open(sys.argv[1])
tgtfile = open(sys.argv[2])
alfile = open(sys.argv[3])
outfile = open(sys.argv[4], 'w')

src_right, src_left, tgt_right, tgt_left, errors, added = 0, 0, 0, 0, 0, 0

for srcline, tgtline, alline in zip(srcfile, tgtfile, alfile):
	src = srcline.strip().split(" ")
	tgt = tgtline.strip().split(" ")
	try:
		alignments = [(int(x.split("-")[0]), (int(x.split("-")[1]))) for x in alline.strip().split(" ")]
	except ValueError:
		print(f"Cannot parse alignment in file {sys.argv[3]}:")
		print(alline.strip())
		errors += 1
		outfile.write(alline)		# write the line without change
		continue
	
	add_alignments = set()
	srcalign = set([x[0] for x in alignments])
	for i in range(len(src)-1):
		if (i in srcalign) and (i+1 not in srcalign) and (src[i] == src[i+1]):
			j = [x[1] for x in alignments if x[0] == i]
			if len(j) != 1:
				print("multiple alignments, skip")
				continue
			j = j[0]
			add_alignments.add((i+1, j))
			src_right += 1
		elif (i not in srcalign) and (i+1 in srcalign) and (src[i] == src[i+1]):
			j = [x[1] for x in alignments if x[0] == i+1]
			if len(j) != 1:
				print("multiple alignments, skip")
				continue
			j = j[0]
			add_alignments.add((i, j))
			src_left += 1
	
	tgtalign = set([x[1] for x in alignments])
	for i in range(len(tgt)-1):
		if (i in tgtalign) and (i+1 not in tgtalign) and (tgt[i] == tgt[i+1]):
			j = [x[0] for x in alignments if x[1] == i]
			if len(j) != 1:
				print("multiple alignments, skip")
				continue
			j = j[0]
			add_alignments.add((j, i+1))
			tgt_right += 1
		elif (i not in tgtalign) and (i+1 in tgtalign) and (tgt[i] == tgt[i+1]):
			j = [x[0] for x in alignments if x[1] == i+1]
			if len(j) != 1:
				print("multiple alignments, skip")
				continue
			j = j[0]
			add_alignments.add((j, i))
			tgt_left += 1

	added += len(add_alignments)
	all_alignments = sorted(alignments + list(add_alignments), key=lambda x: x[0])
	outfile.write(" ".join(["{}-{}".format(x[0], x[1]) for x in all_alignments]) + "\n")

fileid = os.path.basename(sys.argv[3])
#print("TEXT\tSRC_R\tSRC_L\tTGT_R\tTGT_L\tADDED")
print(f"{fileid}\t{src_right}\t{src_left}\t{tgt_right}\t{tgt_left}\t{added}")
srcfile.close()
tgtfile.close()
alfile.close()
outfile.close()
