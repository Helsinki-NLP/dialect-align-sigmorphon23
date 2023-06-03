#! /bin/bash -l

#SBATCH -J fastal
#SBATCH -o log_fastal.%j.out
#SBATCH -e log_fastal.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 24:00:00

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-moses

DATADIR=../../data

declare -A SYM=( ["isc"]="intersect" ["uni"]="union" ["gdf"]="grow-diag-final" ["gdfa"]="grow-diag-final-and")

for PROJECT in archimob6 ndc skn; do
	echo $PROJECT
	mkdir -p $PROJECT
	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		python ../mergefiles.py $DATADIR/$PROJECT/$FID.orig $DATADIR/$PROJECT/$FID.norm > $PROJECT/$FID.text
		fast_align -i $PROJECT/$FID.text -d -o -v > $PROJECT/$FID.fwd
		fast_align -i $PROJECT/$FID.text -d -o -v -r > $PROJECT/$FID.rev
		for S in "${!SYM[@]}"; do
			atools -c "${SYM[$S]}" -i$PROJECT/$FID.fwd -j$PROJECT/$FID.rev > $PROJECT/$FID.$S
		done
	done

	mkdir -p concat
	python ../mergefiles.py $DATADIR/concat/$PROJECT.all.orig $DATADIR/concat/$PROJECT.all.norm > concat/$PROJECT.all.text
	fast_align -i concat/$PROJECT.all.text -d -o -v > concat/$PROJECT.all.fwd
	fast_align -i concat/$PROJECT.all.text -d -o -v -r > concat/$PROJECT.all.rev
	for S in "${!SYM[@]}"; do
		atools -c "${SYM[$S]}" -iconcat/$PROJECT.all.fwd -jconcat/$PROJECT.all.rev > concat/$PROJECT.all.$S
	done
done
