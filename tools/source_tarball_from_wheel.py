#!/usr/bin/env python
#
# Script to build a source tarball from wheel file under Linux
# The script loads the required missing file (CHANGES.md, setup.py,
# COPYING.txt, README.md) from GitHub repository
#
# This file is part of Expyriment

import os
import sys
from shutil import rmtree, move
from subprocess import call


if __name__=="__main__":

    sep = os.path.sep
    build ="/tmp/tarball_build" + sep
    missing_files = ["CHANGES.md", "setup.py", "COPYING.txt", "README.md"]

    if len(sys.argv)<=1:
       print "Usage: source_tarball_from_wheel <wheel file> [suffix]"
       print "      Suffix is optional and requires from some Debain builds"
       exit()

    # prepare filenames and folder
    wheel = sys.argv[1]
    tmp = wheel.split("-")
    try:
        if tmp[0] == "expyriment" and tmp[4]=="any.whl":
            version = tmp[1]
        else:
            version = None
    except:
        version = None

    if version is None:
        print "'{0}' is not a Expyriment wheel".format(wheel)
        exit()

    print "Expyriment {0} wheel found".format(version)

    if len(sys.argv)>2:
        suffix = sys.argv[2]
    else:
        suffix = ""
    package_name = "python-expyriment-{0}{1}".format(version, suffix)
    package_tar = "python_expyriment-{0}{1}.orig.tar.gz".format(version, suffix)
    package_path = build + package_name + sep

    rmtree(build, ignore_errors=True)
    os.makedirs(build)
    os.makedirs(package_path)

    # unpack
    call(["unzip", wheel, "-d", build])
    move(build + "expyriment", package_path)
    tmp = build + "expyriment-{0}.data".format(version) + sep + "data" + sep \
                + "share" + sep + "expyriment" + sep
    move(tmp + "documentation", package_path)
    move(tmp + "examples", package_path )
    move(tmp + "tools", package_path)

    # cleaning
    rmtree(package_path + "expyriment" + sep + "_fonts", ignore_errors=True)
    rmtree(package_path + "documentation" + sep + "html", ignore_errors=True)

    # download missing files from github
    url = "https://github.com/expyriment/expyriment/blob/v{0}/".format(version)
    for fl in missing_files:
        call(["wget", url + fl])
        move(fl, package_path)

    # make tar and clean up
    if os.path.isfile(package_tar):
        os.remove(package_tar)
    call(["tar", "czf", package_tar,  "-C", build, package_name])
    call(["sha1sum", package_tar])
    rmtree(build, ignore_errors=True)
