#! /usr/bin/env python3

import zipfile, bs4, re, writeData

# SKN uses uppercase letters for proper names both in the original and normalized versions, but not for sentence beginnings. We do not change casing here.

ziparchive = zipfile.ZipFile("skn-vrt.zip")
files = [x for x in ziparchive.namelist() if x.endswith(".vrt")]
for filename in sorted(files):
	m = re.search(r'/SKN(\d\d.?)_', filename)
	fileid = m.group(1)
	data = []
	n_utt = 0
	n_tok_orig, n_tok_norm = 0, 0
	vrtfile = ziparchive.open(filename)
	soup = bs4.BeautifulSoup(vrtfile, 'xml')
	for par in soup.find_all("paragraph"):
		# if par["role"] == "muu":
		# 	continue
		for s in par.find_all("sentence"):
			origwords = []
			normwords = []
			lines = s.text.split("\n")
			for l in lines:
				if l.strip() == "":
					continue
				e = l.split("\t")
				# column 1 (detailed) contains plenty of combining diacritics that need to be taken care of specifically
				# column 2 (simplified) doesn't contain any combining diacritics
				o = e[1].strip()
				o = re.sub(r'\s+', ' ', o)
				if o != "" and o != "_":
					origwords.append(o)
				# column 0 (standard) contains a single combining diacritic (by error) - we just remove it
				n = e[0].replace("̬", "").strip()
				n = re.sub(r'\s+',' ', n)
				if n != "" and n != "_":
					normwords.append(n)
			if len(origwords) == 0 or len(normwords) == 0:
				continue
			data.append((origwords, normwords))
			n_utt += 1
			n_tok_orig += len(origwords)
			n_tok_norm += len(normwords)

	print(f"{fileid}: {n_utt} utterances, {n_tok_orig} original words, {n_tok_norm} normalized words")
	writeData.writeCSMT("skn", fileid, data)
