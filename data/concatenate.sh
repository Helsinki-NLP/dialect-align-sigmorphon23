#! /usr/bin sh

mkdir -p concat

for CORPUS in archimob6 archimob43 ndc skn;
do
	cat $CORPUS/*.orig > concat/$CORPUS.all.orig
	cat $CORPUS/*.norm > concat/$CORPUS.all.norm
done
