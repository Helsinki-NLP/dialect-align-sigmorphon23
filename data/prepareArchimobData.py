#! /usr/bin/env python3

import zipfile, bs4, re, writeData

goldids = ['1007', '1048', '1063', '1143', '1198', '1270']

# ArchiMob should not contain any uppercase letters, so no change of casing is required here.

ziparchive = zipfile.ZipFile("Archimob_Release_2.zip")
xmlfiles = [x for x in ziparchive.namelist() if x.endswith(".xml") and not x.endswith("person_file.xml")]
current_doc_id = ""
current_doc_data = []
for x in sorted(xmlfiles):
	m = re.search(r'/(\d\d\d\d)_?\d?\.xml$', x)
	fileid = m.group(1)
	if fileid != current_doc_id:
		if current_doc_data != []:
			writeData.writeCSMT("archimob43", current_doc_id, current_doc_data)
			if current_doc_id in goldids:
				writeData.writeCSMT("archimob6", current_doc_id, current_doc_data)
		current_doc_id = fileid
		current_doc_data = []

	n_utt = 0
	n_tok_orig, n_tok_norm = 0, 0
	xmlfile = ziparchive.open(x)
	soup = bs4.BeautifulSoup(xmlfile, 'xml')
	for u in soup.find_all("u"):
		# if u["who"] == "interviewer" or u["who"] == "otherPerson":
		# 	continue
		origwords = []
		normwords = []
		for w in u.find_all("w"):
			orig = w.text.strip().replace("(", "").replace(")", "")
			orig = orig.replace("(", "").replace(")", "")
			# acute accents are used in phase 1 only to indicate non-standard word stress => remove
			#orig = orig.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ä́", "ä")
			# grave accents are used for open vowels in phase 1 => remove according to guidelines
			# easy cases
			#orig = orig.replace("à", "a").replace("ò", "o").replace("è", "ä").replace("ö̀", "ö")
			# according to guidelines, ì/ù/`ü can be replaced by e/o/ö if pronunciation is really open
			# checks in the data have shown that Peters makes a distinction between u/ù and i/ì, but does not use o and e in these cases, whereas the other transcribers do
			# we suggest therefore to replace all ì/ù/`ü by e/o/ö, but this decision may need to be revised
			#orig = orig.replace("ì", "e").replace("ù", "o").replace("ǜ", "ö")
			if orig != "":
				origwords.append(orig)

			norm = w["normalised"].strip()
			# there is one single case of combining diacritic in the normalized data - just get rid of it
			norm = norm.replace("é", "e")
			if norm != "" and norm != "DELETED":
				normwords.append(norm)

		if len(origwords) == 0 or len(normwords) == 0:
			continue
		current_doc_data.append((origwords, normwords))
		n_utt += 1
		n_tok_orig += len(origwords)
		n_tok_norm += len(normwords)
	print(f"{x} ==> {fileid}: {n_utt} utterances, {n_tok_orig} original words, {n_tok_norm} normalized words")

if current_doc_data != []:
	writeData.writeCSMT("archimob43", current_doc_id, current_doc_data)
	if current_doc_id in goldids:
		writeData.writeCSMT("archimob6", current_doc_id, current_doc_data)
