#! /usr/bin/env python3

import sys, os, glob

total_alignments = 0
total_alignment_pairs = 0
total_src = 0
total_tgt = 0
unaligned_src = 0
unaligned_tgt = 0
same_alignments = 0
diff_alignments = 0
cross_alignment_pairs = 0
vc_alignments = 0
errors = 0

vowels = set(list("aAäÄàãáåÅæÆᴀăâÀɐeEèÈéẽëᴇêəĕḛɛḙėiIìíïɪîịĭḭᵻÌÎoOöÖòÒõóøØôŏŎɔȯȮᴏuUüùǜᴜúṵŭŬûᴜyYʏỳŷ"))
consonants = set(list("bBʙdDᴅðδgGɢpPtTᴛkKᴋḱfFvVsSšśχϑcCqQxXzZ"))
# not considered: l L ʟ ĺ Ĺ m M ᴍ n N Ǹ Ń r R ʀ ŕ ǹ ŋ ɴ ṋ w W ẁ j J ᴊ h H ʜ

# when running this command, make sure to put the file name pattern into quotes:
# $ python3 evaluate.py "m2m/ndc/*.fwd"
pattern = sys.argv[1]
files = glob.glob(pattern)
print(pattern)
print("Number of files: {}".format(len(files)))
if len(files) == 0:
	sys.exit()
datadir = sys.argv[2]

for f in files:
	dirname, basename = os.path.split(f)
	project = dirname.split("/")[-1]
	fileid = basename.rsplit(".", 1)[0]
	srcfilename = f"{datadir}/{project}/{fileid}.orig"
	tgtfilename = f"{datadir}/{project}/{fileid}.norm"

	srcfile = open(srcfilename)
	tgtfile = open(tgtfilename)
	alfile = open(f)

	for srcline, tgtline, alline in zip(srcfile, tgtfile, alfile):
		srctokens = srcline.strip().split(" ")
		tgttokens = tgtline.strip().split(" ")
		try:
			alignments = [(int(x.split("-")[0]), (int(x.split("-")[1]))) for x in alline.strip().split(" ")]
		except ValueError:
			print(f"Cannot parse alignment in file {f}:")
			print(alline.strip())
			errors += 1
			continue
		
		if max([x[0] for x in alignments]) > len(srctokens) or  max([x[1] for x in alignments]) > len(tgttokens):
			print(f"Cannot parse data in file {f}:")
			print(len(srctokens), srctokens)
			print(len(tgttokens), tgttokens)
			print(alline.strip())
			errors += 1
			continue

		total_src += len(srctokens)
		total_tgt += len(tgttokens)
		total_alignments += len(alignments)
		
		unaligned_src += len(set(range(len(srctokens))) - set([x[0] for x in alignments]))
		unaligned_tgt += len(set(range(len(tgttokens))) - set([x[1] for x in alignments]))

		for i, a in enumerate(alignments):
			for b in alignments[i+1:]:
				total_alignment_pairs += 1
				if (b[0] > a[0] and b[1] < a[1]) or (b[0] < a[0] and b[1] > a[1]):
					cross_alignment_pairs += 1

		for a in alignments:
			if srctokens[a[0]] == tgttokens[a[1]]:
				same_alignments += 1
			else:
				diff_alignments += 1
		
		for a in alignments:
			if srctokens[a[0]].lower() in vowels and tgttokens[a[1]].lower() in consonants:
				vc_alignments += 1
			elif srctokens[a[0]].lower() in consonants and tgttokens[a[1]].lower() in vowels:
				vc_alignments += 1

print("Unaligned source tokens:\t{:.2f}%".format(unaligned_src/total_src*100))
print("Unaligned target tokens:\t{:.2f}%".format(unaligned_tgt/total_tgt*100))
#print("Alignment to identicals:\t{:.2f}%".format(same_alignments/total_alignments*100))
print("Alignment to differents:\t{:.2f}%".format(diff_alignments/total_alignments*100))
print("Vowel-cons alignments:\t{:.2f}%".format(vc_alignments/total_alignments*100))
print("Crossing alignment pairs:\t{:.2f}%".format(cross_alignment_pairs/total_alignment_pairs*100))
print("Format errors:\t{}".format(errors))
print()
