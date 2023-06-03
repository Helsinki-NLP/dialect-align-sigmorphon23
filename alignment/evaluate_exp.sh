#! /bin/bash -l

METHOD=$1
EXT=$2

echo $METHOD $EXT

touch $METHOD/eval.$EXT.txt
echo "" > $METHOD/eval.$EXT.txt
for PROJECT in archimob6 ndc skn; do
	python3 evaluate.py "$METHOD/$PROJECT/*.$EXT" ../data >> $METHOD/eval.$EXT.txt
	python3 evaluate.py "$METHOD/concat/$PROJECT.*.$EXT" ../data >> $METHOD/eval.$EXT.txt
done
