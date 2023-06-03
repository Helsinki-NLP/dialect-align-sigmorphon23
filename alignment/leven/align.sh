#! /bin/bash -l

#SBATCH -J leven
#SBATCH -o log.%j.out
#SBATCH -e log.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 2:00:00

DATADIR=../../data

module load python-data
source ../../pyenv/bin/activate

for PROJECT in archimob6 ndc skn; do
	echo $PROJECT
	mkdir -p $PROJECT
	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		python3 ../levenshtein_align.py -method edlib -src $DATADIR/$PROJECT/$FID.orig -tgt $DATADIR/$PROJECT/$FID.norm -fwd $PROJECT/$FID.fwd -rev $PROJECT/$FID.rev
	done
	mkdir -p concat
	python3 ../levenshtein_align.py -method edlib -src $DATADIR/concat/$PROJECT.all.orig -tgt $DATADIR/concat/$PROJECT.all.norm -fwd concat/$PROJECT.all.fwd -rev concat/$PROJECT.all.rev
done
deactivate

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-efmaral

declare -A SYM=( ["isc"]="intersect" ["uni"]="union" ["gdf"]="grow-diag-final" ["gdfa"]="grow-diag-final-and")

for PROJECT in archimob6 ndc skn; do
	echo "Symmetrize" $PROJECT
	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		for S in "${!SYM[@]}"; do
			atools -c "${SYM[$S]}" -i$PROJECT/$FID.fwd -j$PROJECT/$FID.rev > $PROJECT/$FID.$S
		done
	done
	for S in "${!SYM[@]}"; do
		atools -c "${SYM[$S]}" -iconcat/$PROJECT.all.fwd -jconcat/$PROJECT.all.rev > concat/$PROJECT.all.$S
	done
done
