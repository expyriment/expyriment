#!/usr/bin/env python
"""
Setup file for Expyriment
"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


import stat
import os
from os import remove, close, chmod, path
import sys
from subprocess import Popen, PIPE, call
from shutil import move, copytree, rmtree
from tempfile import mkstemp
from glob import glob

from setuptools import setup
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py
from setuptools.command.install import install
from distutils.command.install_data import install_data


# Settings
description='A Python library for cognitive and neuroscientific experiments'
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
author='Florian Krause, Oliver Lindemann'
author_email='florian@expyriment.org, oliver@expyriment.org'
license='GNU GPLv3'
url='http://www.expyriment.org'

package_dir={'expyriment': 'expyriment'}

packages = ['expyriment',
            'expyriment.control',
            'expyriment.io', 'expyriment.io.extras',
            'expyriment.io._parallelport',
            'expyriment.misc', 'expyriment.misc.extras',
            'expyriment.misc.data_preprocessing',
            'expyriment.misc.geometry',
            'expyriment.misc.statistics',
            'expyriment.stimuli', 'expyriment.stimuli.extras',
            'expyriment.design', 'expyriment.design.extras',
            'expyriment.design.randomize',
            'expyriment.design.permute']

package_data = {'expyriment': ['expyriment_logo.png', 'xpy_icon.png',
                               '_fonts/*.*']}

source_files = ['.release_info',
                'CHANGES.MD',
                'COPYING.txt',
                'Makefile',
                'README.md']

install_requires = ["pygame>=1.9,<3",
                    "pyopengl>=3.0,<4"]

extras_require = {
    'data_preprocessing': ["numpy>=1.6,<2"],
    'serialport':         ["pyserial>=3,<4"],
    'parallelport_linux': ["pyparallel>=0.2,<1"],
    'video':              ["sounddevice>=0.3,<1",
                           "mediadecoder>=0.1,<1"],
    'all':                ["numpy>=1.6,<2",
                           "pyserial>=3,<4",
                           "pyparallel>=0.2,<1",
                           "sounddevice>=0.3,<1",
                           "mediadecoder>=0.1,<1"]
    }

entry_points = {
        'console_scripts': ['expyriment=expyriment.cli:main'],
    }


class Sdist(sdist):
    def get_file_list(self):
        version_nr, revision_nr, date = get_version_info_from_release_info()
        # If code is check out from GitHub repository, change .release_info
        if date.startswith("$Format:"):
            version_nr, revision_nr, date = get_version_info_from_git()
            version_nr = "tag: " + version_nr
            move(".release_info", ".release_info.bak")
            with open(".release_info", 'w') as f:
                f.write(u"{0}\n{1}\n{2}".format(version_nr, revision_nr, date))
        for f in source_files:
            self.filelist.append(f)
        sdist.get_file_list(self)

    def run(self):
        sdist.run(self)
        try:
            move(".release_info.bak", ".release_info")
        except:
            pass


# Manipulate the header of all files (only for building/installing from
# repository)
class Build(build_py):
    """Specialized Python source builder."""

    def byte_compile(self, files):
        for f in files:
            if f.endswith('.py'):
                # Create temp file
                fh, abs_path = mkstemp()
                new_file = open(abs_path, 'wb')
                old_file = open(f, 'rb')  # was 'rUb'
                for line in old_file:
                    if line[0:11] == b'__version__':
                        new_file.write("__version__ = '{0}'\n".format(
                            version_nr).encode("utf-8"))
                    elif line[0:12] == b'__revision__':
                        new_file.write("__revision__ = '{0}'\n".format(
                            revision_nr).encode("utf-8"))
                    elif line[0:8] == b'__date__':
                        new_file.write("__date__ = '{0}'\n".format(
                            date).encode("utf-8"))
                    else:
                        new_file.write(line)
                # Close temp file
                new_file.close()
                close(fh)
                old_file.close()
                # Remove original file
                remove(f)
                # Move new file
                move(abs_path, f)
                chmod(f,
                      stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        build_py.byte_compile(self, files)


# Clear old installation when installing
class Install(install):
    """Specialized installer."""

    def run(self):
        # Clear old installation
        try:
            olddir = path.abspath(self.install_lib + path.sep + "expyriment")
            oldegginfo = glob(path.abspath(self.install_lib) + path.sep +
                              "expyriment*.egg-info")
            for egginfo in oldegginfo:
                remove(egginfo)
            if path.isdir(olddir):
                rmtree(olddir)
        except:
            pass
        install.run(self)


def get_version_info_from_git():
    """Get version number, revision number and date from git repository."""

    proc = Popen(['git', 'describe', '--tags', '--dirty', '--always'], \
                        stdout=PIPE, stderr=PIPE)
    version_nr = "{0}+{1}.{2}".format(
        *proc.stdout.read().lstrip(b"v").strip().decode("utf-8").split("-"))
    proc = Popen(['git', 'log', '--format=%H', '-1'], \
                        stdout=PIPE, stderr=PIPE)
    revision_nr = proc.stdout.read().strip()[:7].decode("utf-8")
    proc = Popen(['git', 'log', '--format=%cd', '-1'],
                     stdout=PIPE, stderr=PIPE)
    date = proc.stdout.readline().strip().decode("utf-8")
    return version_nr, revision_nr, date

def get_version_info_from_release_info():
    """Get version number, revision number and date from .release_info."""

    setup_dir = os.path.split(os.path.abspath(__file__))[0]
    with open(os.path.join(setup_dir, ".release_info")) as f:
        lines = []
        for line in f:
            lines.append(line)
    for x in lines[0].split(","):
        if "tag:" in x:
            version_nr = x.replace("tag:","").strip().lstrip("v")
        else:
            version_nr = ""
    revision_nr = lines[1].strip()[:7]
    date = lines[2].strip()
    # GitHub source archive (snapshot, no tag)
    if version_nr == "":
        with open(os.path.join(setup_dir, "CHANGES.md")) as f:
            for line in f:
                if line.lower().startswith("version"):
                    version_nr = "{0}-0-g{1}".format(line.split(" ")[1],
                                                    revision_nr)
                    break
    return version_nr, revision_nr, date

def get_version_info_from_file(filename):
    """Get version number, revision number and date from a .py file."""

    with open(filename) as f:
        for line in f:
            if line.startswith("__version__"):
                version_nr = line.split("'")[1]
            if line.startswith("__revision__"):
                revision_nr = line.split("'")[1]
            if line.startswith("__date__"):
                date = line.split("'")[1]
    return version_nr, revision_nr, date

def run():
    """Run the setup."""

    setup(name='expyriment',
          version=version_nr,
          description=description,
          long_description=long_description,
          author=author,
          author_email=author_email,
          license=license,
          url=url,
          packages=packages,
          package_dir=package_dir,
          package_data=package_data,
          install_requires=install_requires,
          extras_require=extras_require,
          cmdclass=cmdclass,
          entry_points = entry_points)

if __name__=="__main__":

    # Check if we are building/installing from a built archive/distribution
    version_nr, revision_nr, date = get_version_info_from_file("expyriment/__init__.py")
    if not version_nr == '':
        cmdclass={'install': Install}
        run()
        message = "from built archive/distribution"

    # If not, we are building/installing from source
    else:
        cmdclass={'sdist': Sdist,
                  'build_py': Build,
                  'install': Install}

        # Are we building/installing from a source archive/distribution?
        version_nr, revision_nr, date = get_version_info_from_release_info()
        if not date.startswith("$Format:"):
            run()
            message = "from source archive/distribution"

        # Are we building/installing from the GitHub repository?
        else:
            try:
                proc = Popen(['git', 'rev-list', '--max-parents=0', 'HEAD'],
                             stdout=PIPE, stderr=PIPE)
                initial_revision = proc.stdout.readline()
                if not b'e21fa0b4c78d832f40cf1be1d725bebb2d1d8f10' in \
                                                                initial_revision:
                    raise Exception
                version_nr, revision_nr, date = get_version_info_from_git()
                run()
                message = "from repository"
            except:
                raise RuntimeError("Building/Installing Expyriment failed!")

    print("")
    print("Expyriment Version: [{0}] ({1})".format(version_nr, message))
    try:
        print("Warning:", warning) #FIXME: warning is never defined!
    except:
        pass
