#! /bin/bash -l

#SBATCH -J leven_aai
#SBATCH -o log.%j.out
#SBATCH -e log.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=4G
#SBATCH -A project_2005047
#SBATCH -t 4:00:00

DATADIR=../../data

for PROJECT in archimob6 ndc skn; do
	echo $PROJECT
	mkdir -p aai/$PROJECT
	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		for S in fwd rev isc uni gdf gdfa; do
			python3 ../add_adjacent_identicals.py $DATADIR/$PROJECT/$FID.orig $DATADIR/$PROJECT/$FID.norm $PROJECT/$FID.$S aai/$PROJECT/$FID.$S
		done
	done
	mkdir -p aai/concat
	for S in fwd rev isc uni gdf gdfa; do
		python3 ../add_adjacent_identicals.py $DATADIR/concat/$PROJECT.all.orig $DATADIR/concat/$PROJECT.all.norm concat/$PROJECT.all.$S aai/concat/$PROJECT.all.$S
	done
done
