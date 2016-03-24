#!/usr/bin/env python
"""Make yaml files for OpenSesame help menu"""

from __future__ import absolute_import, print_function, division

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''

import os
import sys

T = "  "
HOME = "Official Webpage: /"
DOC = " /docs/{0}/"
FULLDOC = "Full Documentation:" + DOC
SUPPORT = """Community/Support:
  Twitter: /twitter.html
"""

def get_version():
    """create well shaped Changelog.rst from CHANGES.md"""

    p = os.path.abspath(os.path.join(os.path.split(sys.argv[0])[0], '..', '..'))
    changes_md = os.path.join(p, "CHANGES.md")
    with open(changes_md, 'r') as fl:
        for line in fl:
            if line.startswith("Version"):
                return line.split(" ")[1]

def get_rst_files(submodule):
    files = []
    for x in os.listdir("."):
        if x.endswith(".rst") and \
            x.startswith("expyriment." + submodule):
            tmp = x[:-4].replace("expyriment." + submodule, "")
            if len(tmp) >1:
                files.append(tmp[1:])
    files.sort()
    return files

def api_ref_structure(version):
    """uses rst file to determine api reference structure"""
    doc = DOC.format(version)
    rtn = []
    rtn.append("API Reference:")
    rtn.append(T + "base:" + doc + "expyriment.html")

    for submodule  in ["control", "design", "io", "misc", "stimuli"]:
        rtn.append(T + submodule + ":")
        rtn.append(2*T + "base:" + doc + \
                    "expyriment.{0}.html".format(submodule))
        # non extras
        for f in get_rst_files(submodule):
            if f.find("extras") <0:
                rtn.append(2*T + f + ":" + doc + \
                    "expyriment.{0}.{1}.html".format(submodule, f))
        # extras
        rtn.append(2*T + "extras:")
        for f in get_rst_files(submodule):
            if f.find("extras") >=0:
                try:
                    tmp = f.split(".")
                    rtn.append(3*T + tmp[1] + ":" + doc + \
                        "expyriment.{0}.extras.{1}.html".format(submodule, tmp[1]))
                except:
                    pass

    return "\n".join(rtn)

if __name__ == "__main__":
    print("creating sitemap")
    version = get_version()
    with open("sitemap.yml", "w+") as fl:
        fl.write(HOME + "\n")
        fl.write(api_ref_structure(version) + "\n")
        fl.write(FULLDOC.format(version) + "\n")
        fl.write(SUPPORT+ "\n")
