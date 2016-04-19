#!/usr/bin/env python
"""Make yaml files for OpenSesame help menu"""

from __future__ import absolute_import, print_function, division

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''

import os
import sys

from create_rst_api_reference import inspect_members, exclude, expyriment

T = "  "
HOME = "Official Website: /"
DOC = " /docs/{0}/"
FULLDOC = "Full Documentation:" + DOC
SUPPORT = """Community/Support:
  Newsletter: /newsletter
  Forum: /forum
  Mailinglist: /mailinglist
  IRC/Matrix chat: /chat
  Facebook: /facebook
  Twitter: /twitter
  Reddit: /reddit
  Google+: /googleplus
"""
YAML_FILE = "sitemap.yml"


def get_version():
    try:
        info = expyriment.misc.get_system_info()
    except: # expyriment < 0.9
        info = expyriment.get_system_info()
    ver = info['python_expyriment_version']
    if len(ver)>0:
        print("Expyriment version:", ver)
        return ver
    else:
        p = os.path.abspath(os.path.join(os.path.split(sys.argv[0])[0], '..', '..'))
        changes_md = os.path.join(p, "CHANGES.md")
        with open(changes_md, 'r') as fl:
            for line in fl:
                if line.startswith("Version"):
                    ver = line.split(" ")[1]
                    print("Expyriment version from CHANGES.md:", ver)
                    return ver

def parse_module(mod_name, tab, doc_path):
    modules, classes, methods, functions, attributes = inspect_members(mod_name)
    rtn  = []
    submodels_add_later = []
    if len(modules)>0:
        for m in modules:
            if m[0] not in exclude:
                if m[0]=="constants":
                    rtn.append(tab + m[0] + ":" + doc_path + \
                                    mod_name + "." + m[0] + ".html")
                elif m[0] == "extras":
                    submodels_add_later.append(m[0])
                elif m[0] != "defaults":
                    tmp = parse_module(mod_name=mod_name + "." + m[0],\
                                tab=tab+T, doc_path=doc_path)
                    if len(tmp)>0:
                        rtn.append(tab + m[0] + ":")
                        rtn.extend(tmp)

    if len(classes)>0:
        for cl in classes:
            if cl[0] not in exclude:
                rtn.append(tab + cl[0] + ":")
                rtn.append(tab + T + "__init__:" + doc_path + \
                        mod_name + ".html#" + mod_name + "." + cl[0])

                rtn.extend(parse_module(mod_name=mod_name + "." + cl[0], \
                            tab=tab+ T, doc_path=doc_path))

    if len(methods)>0:
        for m in methods:
            if m[0] not in exclude:
                rtn.append(tab + m[0] + ":" + doc_path + \
                            mod_name + ".html#" + mod_name + "." + m[0])

    if len(functions)>0:
        for func in functions:
            if func[0] not in exclude:
                rtn.append(tab + func[0] + ":" + doc_path + \
                                mod_name + ".html#" + mod_name + "."+ func[0])

    for m in submodels_add_later:
        tmp = parse_module(mod_name=mod_name + "." + m, \
                            tab=tab+T, doc_path=doc_path)
        if len(tmp)>0:
            rtn.append(tab + m + ":")
            rtn.extend(tmp)

    return rtn


def api_ref_structure(version):
    """api reference structure with text as yaml text"""
    rtn = []
    rtn.append("API Reference:")
    rtn.extend(parse_module(mod_name="expyriment", tab=T,
                            doc_path = DOC.format(version)))

    return "\n".join(rtn)

if __name__ == "__main__":

    print("creating sitemap:", YAML_FILE)
    version = get_version()
    with open(YAML_FILE, "w+") as fl:
        fl.write(HOME + "\n")
        fl.write(api_ref_structure(version) + "\n")
        fl.write(FULLDOC.format(version) + "\n")
        fl.write(SUPPORT+ "\n")
