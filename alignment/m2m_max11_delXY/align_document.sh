#! /bin/bash -l

M2M_EXE=../../m2m-aligner/m2m-aligner
DATADIR=../../data

PROJECT=$1
ORIGFILE=$2
FID=`basename $ORIGFILE .orig`

echo "Aligning $PROJECT/$FID (orig file $ORIGFILE)"

#paste $DATADIR/$PROJECT/$FID.orig $DATADIR/$PROJECT/$FID.norm > $PROJECT/$FID.fwd.input
#$M2M_EXE --inFormat news --sepChar "#" --nullChar "@" --delX --delY --maxX 1 --maxY 1 --errorInFile -i $PROJECT/$FID.fwd.input -o $PROJECT/$FID.fwd.aligned --alignerOut $PROJECT/$FID.fwd.model
python3 ../convert_m2m.py < $PROJECT/$FID.fwd.aligned > $PROJECT/$FID.fwd

#paste $DATADIR/$PROJECT/$FID.norm $DATADIR/$PROJECT/$FID.orig > $PROJECT/$FID.rev.input
#$M2M_EXE --inFormat news --sepChar "#" --nullChar "@" --delX --delY --maxX 1 --maxY 1 --errorInFile -i $PROJECT/$FID.rev.input -o $PROJECT/$FID.rev.aligned --alignerOut $PROJECT/$FID.rev.model
python3 ../convert_m2m.py -rev < $PROJECT/$FID.rev.aligned > $PROJECT/$FID.rev


module use -a /projappl/nlpl/software/modules/etc
module load nlpl-efmaral

declare -A SYM=( ["isc"]="intersect" ["uni"]="union" ["gdf"]="grow-diag-final" ["gdfa"]="grow-diag-final-and")

for S in "${!SYM[@]}"; do
	atools -c "${SYM[$S]}" -i$PROJECT/$FID.fwd -j$PROJECT/$FID.rev > $PROJECT/$FID.$S
done
