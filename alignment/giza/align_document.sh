#! /bin/bash

set -e

module use -a /projappl/nlpl/software/modules/etc
module load nlpl-moses

GIZABINDIR=/projappl/nlpl/software/modules/moses/4.0-a89691f/giza

PROJECT=$1
FID=$2
DATADIR=../../data

echo "Aligning file: $PROJECT/$FID"

mkdir -p $PROJECT
cp $DATADIR/$PROJECT/$FID.orig $PROJECT/$FID.orig
cp $DATADIR/$PROJECT/$FID.norm $PROJECT/$FID.norm

$GIZABINDIR/plain2snt.out $PROJECT/$FID.orig $PROJECT/$FID.norm
# creates $PROJECT/$FID.orig_$FID.norm.snt (both ways) + $PROJECT/$FID.orig.vcb + $PROJECT/$FID.norm.vcb

$GIZABINDIR/snt2cooc.out $PROJECT/$FID.orig.vcb $PROJECT/$FID.norm.vcb  $PROJECT/$FID."orig_"$FID.norm.snt > $PROJECT/$FID.orig_norm.cooc
$GIZABINDIR/snt2cooc.out $PROJECT/$FID.norm.vcb $PROJECT/$FID.orig.vcb  $PROJECT/$FID."norm_"$FID.orig.snt > $PROJECT/$FID.norm_orig.cooc

# use 10 classes (instead of the default 100)
$GIZABINDIR/mkcls -n10 -c10 -p$PROJECT/$FID.orig -V$PROJECT/$FID.orig.vcb.classes
$GIZABINDIR/mkcls -n10 -c10 -p$PROJECT/$FID.norm -V$PROJECT/$FID.norm.vcb.classes

$GIZABINDIR/GIZA++ -S $PROJECT/$FID.orig.vcb -T $PROJECT/$FID.norm.vcb -C $PROJECT/$FID.orig_$FID.norm.snt -CoocurrenceFile $PROJECT/$FID.orig_norm.cooc -o $PROJECT/$FID.align.fwd
$GIZABINDIR/GIZA++ -S $PROJECT/$FID.norm.vcb -T $PROJECT/$FID.orig.vcb -C $PROJECT/$FID.norm_$FID.orig.snt -CoocurrenceFile $PROJECT/$FID.norm_orig.cooc -o $PROJECT/$FID.align.rev

python3 ../convert_giza.py $PROJECT/$FID.align.fwd.A3.final $PROJECT/$FID.fwd
python3 ../convert_giza.py $PROJECT/$FID.align.rev.A3.final $PROJECT/$FID.rev -r
rm $PROJECT/$FID.align.* $PROJECT/$FID.orig* $PROJECT/$FID.norm*
