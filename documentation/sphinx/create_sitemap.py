#!/usr/bin/env python
"""Make yaml files for OpenSesame help menu"""

from __future__ import absolute_import, print_function, division

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''

import os
import sys

from create_rst_api_reference import inspect_members, exclude

T = "  "
HOME = "Official Webpage: /"
DOC = " /docs/{0}/"
FULLDOC = "Full Documentation:" + DOC
SUPPORT = """Community/Support:
  Newsletter: /newsletter
  Forum: /forum
  Mailinglist: /mailinglist
  Twitter: /twitter
  Facebook: /facebook
  IRC/Matrix chat: /chat
  Reddit: /reddit
  Google+: /googleplus
"""

def get_version():
    """create well shaped Changelog.rst from CHANGES.md"""

    p = os.path.abspath(os.path.join(os.path.split(sys.argv[0])[0], '..', '..'))
    changes_md = os.path.join(p, "CHANGES.md")
    with open(changes_md, 'r') as fl:
        for line in fl:
            if line.startswith("Version"):
                return line.split(" ")[1]


def parse_module(mod_name, tab, doc_path):
    modules, classes, methods, functions, attributes = inspect_members(mod_name)
    rtn  = []
    if len(modules)>0:
        for m in modules:
            if m[0] not in exclude:
                if m[0]=="constants":
                    rtn.append(tab + m[0] + ":" + doc_path +  mod_name + "." + m[0] + ".html")
                elif m[0] != "defaults":
                    rtn.append(tab + m[0] + ":")
                    rtn.extend(parse_module(mod_name=mod_name + "." + m[0], tab=tab+T, doc_path=doc_path))

    if len(classes)>0:
        for cl in classes:
            if cl[0] not in exclude:
                rtn.append(tab + cl[0] + ":")
                rtn.append(tab + T + "__init__:" + doc_path + mod_name + ".html#" + mod_name + "." + cl[0])

                rtn.extend(parse_module(mod_name=mod_name + "." + cl[0], tab=tab+ T, doc_path=doc_path))

    if len(methods)>0:
        for m in methods:
            if m[0] not in exclude:
                rtn.append(tab + m[0] + ":" + doc_path + mod_name + ".html#" + mod_name + "." + m[0])

    if len(functions)>0:
        for func in functions:
            if func[0] not in exclude:
                rtn.append(tab + func[0] + ":" + doc_path + mod_name + ".html#" + mod_name + "."+ func[0])
    return rtn


def api_ref_structure(version):
    """uses rst file to determine api reference structure"""
    rtn = []
    rtn.append("API Reference:")
    rtn.append(T + "expyriment:" + DOC.format(version) + "expyriment.html")
    rtn.extend(parse_module(mod_name="expyriment", tab=T,
                            doc_path = DOC.format(version)))

    return "\n".join(rtn)

if __name__ == "__main__":
    print("creating sitemap")
    version = get_version()
    with open("sitemap.yml", "w+") as fl:
        fl.write(HOME + "\n")
        fl.write(api_ref_structure(version) + "\n")
        fl.write(FULLDOC.format(version) + "\n")
        fl.write(SUPPORT+ "\n")
