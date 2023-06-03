#! /bin/bash -l

#SBATCH -J eflomalpriors
#SBATCH -o log_eflomalpriors.%j.out
#SBATCH -e log_eflomalpriors.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 24:00:00

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-efmaral

DATADIR=../../data

declare -A SYM=( ["isc"]="intersect" ["uni"]="union" ["gdf"]="grow-diag-final" ["gdfa"]="grow-diag-final-and")

set -e

for PROJECT in archimob6 ndc skn; do
	echo $PROJECT
	python ../mergefiles.py $DATADIR/concat/$PROJECT.all.orig $DATADIR/concat/$PROJECT.all.norm > $PROJECT.all.text
	makepriors.py -i $PROJECT.all.text -f ../eflomal/concat/$PROJECT.all.fwd -r ../eflomal/concat/$PROJECT.all.rev -p $PROJECT.all.priors
	mkdir -p $PROJECT

	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		align_eflomal.py -s $DATADIR/$PROJECT/$FID.orig -t $DATADIR/$PROJECT/$FID.norm -f $PROJECT/$FID.fwd -r $PROJECT/$FID.rev --priors $PROJECT.all.priors
		for S in "${!SYM[@]}"; do
			atools -c "${SYM[$S]}" -i$PROJECT/$FID.fwd -j$PROJECT/$FID.rev > $PROJECT/$FID.$S
		done
	done

	mkdir -p concat
	align_eflomal.py -s $DATADIR/concat/$PROJECT.all.orig -t $DATADIR/concat/$PROJECT.all.norm -f concat/$PROJECT.all.fwd -r concat/$PROJECT.all.rev --priors $PROJECT.all.priors
	for S in "${!SYM[@]}"; do
		atools -c "${SYM[$S]}" -iconcat/$PROJECT.all.fwd -jconcat/$PROJECT.all.rev > concat/$PROJECT.all.$S
	done

	rm $PROJECT.all.text
done
