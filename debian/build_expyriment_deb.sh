#!/bin/bash
# Script to build the Expyriment deb and tar packages
#   Call this script (as root) from the Expyriment install folder with the 
#   Debian script folder as argument (Note: adapt scripts first)
#   Files will be in /tmp/build

export DEBFULLNAME="Oliver Lindemann"
export DEBEMAIL="lindemann09@gmail.com"

DEBIAN_SCRIPTS=$1
DIR=/tmp/build/

#get version
VERSION=`awk 'BEGIN{FS=" "}{ if ($1 ~ /Version/){ print $2;exit}}' CHANGES.txt`

#copy and make tarbal
mkdir -p $DIR
sudo rm $DIR/* -rf
cp -ra ../expyriment-$VERSION $DIR 
cd $DIR
tar czf expyriment-$VERSION.tar.gz expyriment-$VERSION
cd expyriment-$VERSION

###initial release
#dh_make -s -c gpl -f ../expyriment-$VERSION.tar.gz
#cd debian
#rm *.ex *.EX
#rm README.* *.dirs

# copy debian files
cp $DEBIAN_SCRIPTS $DIR/expyriment-$VERSION -rav

#debian/rules binary
