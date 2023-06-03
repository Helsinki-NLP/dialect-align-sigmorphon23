#! /bin/bash -l

#SBATCH -J m2m_max22_delXY_eqmap
#SBATCH -o log.%j.out
#SBATCH -e log.%j.err
#SBATCH -p small
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu=12G
#SBATCH -A project_2005047
#SBATCH -t 48:00:00

DATADIR=../../data

for PROJECT in archimob6 ndc skn; do
	echo $PROJECT
	mkdir -p $PROJECT
	FILES=`ls $DATADIR/$PROJECT/*.orig`
	for F in $FILES; do
		FID=`basename $F .orig`
		echo "  $FID"
		source align_document.sh $PROJECT $FID
	done
	mkdir -p concat
	source align_document.sh concat $PROJECT.all
done
