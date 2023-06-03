#! /usr/bin/env python3

import os, collections

def sizes():
	for corpus in ["archimob6", "archimob43", "ndc", "skn"]:
		nb_docs, nb_lines, nb_words, nb_chars = 0, 0, 0, 0
		for filename in os.listdir(corpus):
			if filename.endswith(".orig"):
				fileid = filename.replace(".orig", "")
				nb_docs += 1
				f = open(corpus + "/" + filename)
				for line in f:
					nb_lines += 1
					nb_words += line.count("_") - 1
					nb_chars += len(line.strip()) // 2
		print(corpus)
		print("Nb docs:        {}".format(nb_docs))
		print("Nb lines:       {}".format(nb_lines))
		print("Nb words:       {}".format(nb_words))
		print("Avg lines/doc:  {:.0f}".format(nb_lines/nb_docs))
		print("Avg words/doc:  {:.0f}".format(nb_words/nb_docs))
		print("Avg chars/doc:  {:.0f}".format(nb_chars/nb_docs))
		print("Avg words/line: {:.2f}".format(nb_words/nb_lines))
		print("Avg chars/line: {:.2f}".format(nb_chars/nb_lines))
		print("Avg chars/word: {:.2f}".format(nb_chars/nb_words))
		print()

def vocabs():
	for corpus in ["archimob6", "ndc", "skn"]:
		print(corpus)
		vocabs = {"orig": collections.defaultdict(int), "norm": collections.defaultdict(int)}
		for side in vocabs:
			f = open("concat/" + corpus + ".all." + side)
			for line in f:
				chars = line.strip().split(" ")
				for c in chars:
					vocabs[side][c] += 1
			f.close()
			print(side, "vocab:", len(vocabs[side]))
			#print(vocabs[side])
		print("intersection vocab:", len(set(vocabs['orig'].keys()) & set(vocabs['norm'].keys())))
		print("union vocab:", len(set(vocabs['orig'].keys()) | set(vocabs['norm'].keys())))
		orig_not_in_norm = set(vocabs['orig'].keys()) - set(vocabs['norm'].keys())
		print("orig chars not in norm vocab:", len(orig_not_in_norm))
		#print(orig_not_in_norm)
		print()

if __name__ == "__main__":
	sizes()
	vocabs()
