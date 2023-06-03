#! /usr/bin/env python

import argparse, edlib, sys, math
import numpy as np

###################################################

# https://stackoverflow.com/questions/66636450/how-to-implement-alignment-through-traceback-for-levenshtein-edit-distance

def backtrace_weighted(first, second, matrix, costs):
	f = [char for char in first]
	s = [char for char in second]
	new_f, new_s = [], []
	new_t = []
	new_list = []	# builds Pharaoh-style alignment pairs directly
	row = len(f)
	col = len(s)

	while row > 0 or col > 0:
		r = matrix[row,col]
		a = matrix[row-1,col]
		b = matrix[row-1,col-1]
		c = matrix[row,col-1]

		if row > 0 and col > 0 and math.isclose(r, b + costs[f[row-1], s[col-1]], abs_tol=10**-4):
			# when diagonal backtrace substitution or no substitution
			new_f = [f[row-1]] + new_f
			new_s = [s[col-1]] + new_s
			if f[row-1] == s[col-1]:
				new_t = ["|"] + new_t
			else:
				new_t = ["."] + new_t
			new_list.append((row-1, col-1))
			row, col = row-1, col-1

		elif row > 0 and math.isclose(r, a + costs[f[row-1],''], abs_tol=10**-4):
			new_f = [f[row-1]] + new_f
			new_s = [" "] + new_s
			new_t = [" "] + new_t
			row = row-1

		elif col > 0 and math.isclose(r, c + costs['',s[col-1]], abs_tol=10**-4):
			new_f = [" "] + new_f
			new_s = [s[col-1]] + new_s
			new_t = [" "] + new_t
			col = col-1
		
		else:
			print("No option applies, give up on sentence")
			print(r, a + costs[f[row-1],''], c + costs['',s[col-1]], b + costs[f[row-1], s[col-1]])
			return new_f, new_s, new_t, new_list

	return new_f, new_s, new_t, new_list


def weighted_levenshtein_leftmost(x, y, costs):
	# reverse strings to simulate leftmost attachment behavior of edlib
	x = x[::-1]
	y = y[::-1]
	rows = len(x) + 1
	cols = len(y) + 1
	distance = np.zeros((rows, cols), dtype=np.float32)

	for i in range(1, rows):
		distance[i][0] = distance[i-1][0] + costs[x[i-1], '']		# del
	for k in range(1, cols):
		distance[0][k] = distance[0][k-1] + costs['', y[k-1]]		# ins

	for col in range(1, cols):
		for row in range(1, rows):
			distance[row][col] = min(distance[row-1][col] + costs[x[row-1], ''],	# del
									 distance[row][col-1] + costs['', y[col-1]],	# ins
									 distance[row-1][col-1] + costs[x[row-1], y[col-1]])	# sub
	
	
	new_x, new_y, new_t, new_list = backtrace_weighted(x, y, distance, costs)
	new_list = [(rows-r-2, cols-c-2) for (r, c) in new_list]
	return "".join(new_x[::-1]), "".join(new_y[::-1]), "".join(new_t[::-1]), new_list


def weighted_levenshtein_rightmost(x, y, costs):
	rows = len(x) + 1
	cols = len(y) + 1
	distance = np.zeros((rows, cols), dtype=np.float32)

	for i in range(1, rows):
		distance[i][0] = distance[i-1][0] + costs[x[i-1], '']		# del
	for k in range(1, cols):
		distance[0][k] = distance[0][k-1] + costs['', y[k-1]]		# ins

	for col in range(1, cols):
		for row in range(1, rows):
			distance[row][col] = min(distance[row-1][col] + costs[x[row-1], ''],	# del
									 distance[row][col-1] + costs['', y[col-1]],	# ins
									 distance[row-1][col-1] + costs[x[row-1], y[col-1]])	# sub
	
	
	new_x, new_y, new_t, new_list = backtrace_weighted(x, y, distance, costs)
	new_list.sort(key=lambda x: x[0])
	return "".join(new_x), "".join(new_y), "".join(new_t), new_list

###################################################

def backtrace_damerau(first, second, matrix):
	f = [char for char in first]
	s = [char for char in second]
	new_f, new_s = [], []
	new_t = []
	new_list = []	# builds Pharaoh-style alignment pairs directly
	row = len(f)
	col = len(s)

	while row > 0 or col > 0:
		r = matrix[row,col]
		a = matrix[row-1,col]
		b = matrix[row-1,col-1]
		c = matrix[row,col-1]

		if row > 1 and col > 1 and f[row-1] == s[col-2] and f[row-2] == s[col-1] and matrix[row-2, col-2] < r:		# transposition
			new_f = [f[row-2], f[row-1]] + new_f
			new_s = [s[col-2], s[col-1]] + new_s
			new_t = ["/", "\\"] + new_t
			new_list.append((row-2, col-1))
			new_list.append((row-1, col-2))
			#print("Swap:", "".join([f[row-2], f[row-1]]), "".join([s[col-2], s[col-1]]))
			row, col = row-2, col-2

		elif row > 0 and col > 0 and r == b + 1 and f[row-1] != s[col-1]:		# diagonal, substitution
			new_f = [f[row-1]] + new_f
			new_s = [s[col-1]] + new_s
			new_t = ["."] + new_t
			new_list.append((row-1, col-1))
			row, col = row-1, col-1
		
		elif row > 0 and col > 0 and r == b and f[row-1] == s[col-1]:		# diagonal, identity
			new_f = [f[row-1]] + new_f
			new_s = [s[col-1]] + new_s
			new_t = ["|"] + new_t
			new_list.append((row-1, col-1))
			row, col = row-1, col-1

		elif row > 0 and r == a + 1:
			new_f = [f[row-1]] + new_f
			new_s = [" "] + new_s
			new_t = [" "] + new_t
			row = row-1

		elif col > 0 and r == c + 1:
			new_f = [" "] + new_f
			new_s = [s[col-1]] + new_s
			new_t = [" "] + new_t
			col = col-1
			
		else:
			print("No option applies, give up on sentence")
			print(r, a + 1, c + 1, b + 1)
			return new_f, new_s, new_t, new_list

	return new_f, new_s, new_t, new_list

def levenshtein_damerau(x, y):
	# don't reverse strings here to keep it simple and working :)
	rows = len(x) + 1
	cols = len(y) + 1
	distance = np.zeros((rows, cols), dtype=np.short)

	for i in range(1, rows):
		distance[i,0] = i		# del
	for k in range(1, cols):
		distance[0,k] = k		# ins

	for col in range(1, cols):
		for row in range(1, rows):
			cost = 0 if x[row-1] == y[col-1] else 1
			distance[row,col] = min(distance[row-1,col] + 1,	# del
									 distance[row,col-1] + 1,	# ins
									 distance[row-1,col-1] + cost)	# sub
			if col > 2 and row > 2 and x[row-2] == y[col-1] and x[row-1] == y[col-2]:
				distance[row,col] = min(distance[row,col], distance[row-2, col-2] + 1)	# swap
	
	new_x, new_y, new_t, new_list = backtrace_damerau(x, y, distance)
	new_list.sort(key=lambda x: x[0])
	return "".join(new_x), "".join(new_y), "".join(new_t), new_list

###################################################

def build_alignment(orig_src, link_src, orig_tgt, link_tgt, link_type):
	src_i = 0
	tgt_i = 0
	alignments = []
	for s, t, x in zip(link_src, link_tgt, link_type):
		# link type: | = identity, . = substitution, (space) = ins or del
		if x == "|" or x == ".":
			if src_i >= len(orig_src):
				print("Src index out of bounds", src_i, len(orig_src), orig_src)
			elif s != orig_src[src_i]:
				print("Src mismatch:", s, orig_src[src_i], orig_src)
			if tgt_i >= len(orig_tgt):
				print("Tgt index out of bounds", tgt_i, len(orig_tgt), orig_tgt)
			elif t != orig_tgt[tgt_i]:
				print("Tgt mismatch:", t, orig_tgt[tgt_i], orig_tgt)
			alignments.append((src_i, tgt_i))
			src_i += 1
			tgt_i += 1
		elif s == " ":
			tgt_i += 1
		elif t == " ":
			src_i += 1
	return alignments


def align_edlib(src, tgt):
	result = edlib.align(tgt, src, task='path')
	align = edlib.getNiceAlignment(result, tgt, src, gapSymbol=" ")
	alignments = build_alignment(src, align['target_aligned'], tgt, align['query_aligned'], align['matched_aligned'])
	return alignments


def align_weighted(src, tgt, costs):
	s, t, a, l = weighted_levenshtein_leftmost(src, tgt, costs)
	#alignments = build_alignment(src, s, tgt, t, a)
	if a[0] in ".|" and (0, 0) not in l:
		print("Beginning not found")
	if a[-1] in ".|" and (len(src)-1, len(tgt)-1) not in l:
		print("End not found")
	return l


def align_weighted_right(src, tgt, costs):
	s, t, a, l = weighted_levenshtein_rightmost(src, tgt, costs)
	#alignments = build_alignment(src, s, tgt, t, a)
	if a[0] in ".|" and (0, 0) not in l:
		print("Beginning not found")
	if a[-1] in ".|" and (len(src)-1, len(tgt)-1) not in l:
		print("End not found")
	return l


def align_damerau(src, tgt):
	s, t, a, l = levenshtein_damerau(src, tgt)
	error = False
	for x in l:
		if len(x) != 2 or not isinstance(x[0], int) or not isinstance(x[1], int) or x[0] < 0 or x[1] < 0:
			print("Invalid alignment pair:", x)
			error = True
	if error:
		print(s)
		print(a)
		print(t)
		print(l)
		print()
	if a[0] in ".|" and (0, 0) not in l:
		print("Beginning not found")
	if a[-1] in ".|" and (len(src)-1, len(tgt)-1) not in l:
		print("End not found")
	return l


def load_costs(costsfile):
	fwd_costs = {}
	rev_costs = {}
	for line in costsfile:
		elem = line.split(" ")
		src = elem[0].strip().replace("@", "")
		tgt = elem[1].strip().replace("@", "")
		val = float(elem[2].strip())
		fwd_costs[src, tgt] = val
		rev_costs[tgt, src] = val
	return fwd_costs, rev_costs


def test():
	x = levenshtein_damerau("elephant", "relevnat")
	#x = levenshtein_damerau("elepxant", "eleynat")
	#x = levenshtein_damerau("art", "rat")
	for a in x:
		print(a)
	print()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Character alignment with Levenshtein distance')
	parser.add_argument('-method', choices=['edlib', 'weighted', 'weighted_right', 'damerau'], help='Algorithm used for the alignment')
	parser.add_argument('-src', type=argparse.FileType('r'), help='File with the source data')
	parser.add_argument('-tgt', type=argparse.FileType('r'), help='File with the target data')
	parser.add_argument('-fwd', type=argparse.FileType('w'), help='File into which forward alignments are written (optional)')
	parser.add_argument('-rev', type=argparse.FileType('w'), help='File into which reverse alignments are written (optional)')
	parser.add_argument('-costs', type=argparse.FileType('r'), help='File with the transition costs')
	parser.add_argument('-test', action='store_true', help='Calls the test() function for debugging, ignoring all other arguments')
	args = parser.parse_args()

	if args.test:
		test()
		sys.exit(0)
	
	if args.fwd is None and args.rev is None:
		print("No output file specified, stopping here")
		sys.exit(0)
	
	if args.costs is not None:
		fwd_costs, rev_costs = load_costs(args.costs)

	for srcline, tgtline in zip(args.src, args.tgt):
		# assumes that every token is a single character
		src = srcline.strip().replace(" ", "")
		tgt = tgtline.strip().replace(" ", "")

		if args.fwd is not None:
			if args.method == 'edlib':
				fwd_align = align_edlib(src, tgt)
			elif args.method == 'weighted':
				fwd_align = align_weighted(src, tgt, fwd_costs)
			elif args.method == 'weighted_right':
				fwd_align = align_weighted_right(src, tgt, fwd_costs)
			elif args.method == 'damerau':
				fwd_align = align_damerau(src, tgt)
			else:
				raise NotImplementedError(args.method)
			fwd_alignstr = " ".join(["{}-{}".format(x[0], x[1]) for x in fwd_align])
			args.fwd.write(fwd_alignstr + "\n")
		
		if args.rev is not None:
			if args.method == 'edlib':
				rev_align = align_edlib(tgt, src)
			elif args.method == 'weighted':
				rev_align = align_weighted(tgt, src, rev_costs)
			elif args.method == 'weighted_right':
				rev_align = align_weighted_right(tgt, src, rev_costs)
			elif args.method == 'damerau':
				rev_align = align_damerau(tgt, src)
			else:
				raise NotImplementedError(args.method)
			rev_alignstr =  " ".join(["{}-{}".format(x[1], x[0]) for x in rev_align])
			args.rev.write(rev_alignstr + "\n")
