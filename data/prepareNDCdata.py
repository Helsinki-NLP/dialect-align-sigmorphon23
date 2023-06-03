#! /usr/bin/env python3

import zipfile, bs4, re, os, writeData

fillers = {"ja", "mm", "nei", "å", "m", "e", "ok", "da", "jaha", "ja_vel", "hæ", "hm", "oi", "og", "så", "jo", "ehe", "men", "jaha", "...", "?", " mhm", "det", "er", "var", "akkurat", "jeg", "I"}

# Uppercase letters are used for proper names (Italia), speaker abbreviations (F1) and some specific linguistic features (L). We do not change the casing in preprocessing.

def clean(s):
	s = s.replace("*", "").replace("#", "").replace("|", "")
	# replace references to other informants by I
	s = re.sub(r'\b\w+_\d\d(\w\w)?\b', 'I', s)
	# remove existing underscores if they are at the end of a token or constitute a full token
	s = re.sub(r'_\b', '', s)
	s = re.sub(r'\s+', ' ', s)
	s = s.strip()
	return s

ziparchive = zipfile.ZipFile("ndc-aligned.zip")
files = [x for x in ziparchive.namelist() if x.endswith(".vrt")]
for f in sorted(files):
	filename = f.split("/")[-1].replace(".vrt", "")
	data = []
	n_utt = 0
	n_tok_orig, n_tok_norm = 0, 0
	vrtfile = ziparchive.open(f)
	soup = bs4.BeautifulSoup(vrtfile, 'xml')
	for u in soup.find_all("u"):
		origwords = []
		normwords = []
		for line in u.text.split("\n"):
			if line.strip() == "":
				continue
			elements = line.split("\t")
			orig = clean(elements[0])
			norm = clean(elements[1])
			if orig == "" and norm == "":
				continue
			origwords.append(orig)
			normwords.append(norm)

		# skip utterances that only consist of fillers
		if set(normwords) - fillers == set():
			continue
		if len(origwords) == 0 or len(normwords) == 0:
			continue
		data.append((origwords, normwords))
		n_utt += 1
		n_tok_orig += len(origwords)
		n_tok_norm += len(normwords)

	print(f"{filename}: {n_utt} utterances, {n_tok_orig} original words, {n_tok_norm} normalized words")
	writeData.writeCSMT("ndc", filename, data)
