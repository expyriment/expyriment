#!/bin/sh
# Linux shell script to download (from GitHub) & install the latest Expyriment version

DIR=/tmp/expyriment_install
sudo rm -rf $DIR
mkdir -p $DIR

# Get version
wget -P $DIR https://raw.github.com/expyriment/expyriment/master/CHANGES.md
VER=`awk 'BEGIN{FS=" "}{ if ($1 ~ /Version/){ print $2;exit}}' $DIR/CHANGES.md`

# Print change log
head -n 3 $DIR/CHANGES.md
awk 'BEGIN{FS=" "; f = 0} 
{ if (f == 1){ 
    if ($1 ~ /Version/){exit;}
        print $0;}
    if ($1 ~ /Version/){f = 1; print $0}
}' $DIR/CHANGES.md

# Download and install
while [ 1 ]
do
    echo -n "Download and install Expyriment $VER (y/n)? "
    read ans

    if [ "$ans" = "y" ]; then
        wget -P $DIR https://github.com/expyriment/expyriment/releases/download/v$VER/expyriment-$VER.zip
        cd $DIR
        unzip expyriment-$VER.zip
        cd expyriment-$VER
        # Try the python2 comamnd (e.g. Archlinux)
        type python2 > /dev/null
        if [ "$?" -eq 0 ]; then
            echo "using the 'python2' command to install"
            sudo python2 setup.py install
        # Otherwise use the normal python command
        else
            echo "using the 'python' command to install"
			sudo python setup.py install
        fi
        break
    fi
    if [ "$ans" = "n" ]; then
        echo "Nothing done."
        break
    fi
done
