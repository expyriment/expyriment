#!/usr/bin/env python
"""Make rst files for the expyriment API reference"""
from __future__ import absolute_import, print_function
import __future__
import builtins

import os
import sys
import inspect

p = os.path.abspath(os.path.join(os.path.split(sys.argv[0])[0], '..', '..'))
#sys.path.insert(0, p)

import expyriment
import expyriment.io.extras
import expyriment.design.extras
import expyriment.stimuli.extras
import expyriment.misc.extras


exclude = dir(builtins) + dir(__future__) + ['builtins', 'ModuleType',
                                             'True', 'False']

def inspect_members(item):
    members = inspect.getmembers(eval(item))
    modules = []
    classes = []
    methods = []
    functions = []
    attributes = []
    for member in members:
        if member[0][0:1] != '_':
            if inspect.ismodule(member[1]):
                modules.append(member)
            elif inspect.isclass(member[1]):
                classes.append(member)
            elif inspect.isfunction(member[1]):
                functions.append(member)
            elif inspect.ismethod(member[1]):
                methods.append(member)
            else:
                attributes.append(member)

    return modules, classes, methods, functions, attributes

def heading(txt, t="="):
    return txt + "\n" + len(txt)*t + "\n"


def create_class_rst(class_name):
    with open(class_name + ".rst", 'w') as fl:
        fl.write(heading(class_name))
        fl.write("\n.. autoclass:: " + class_name +"\n")
        fl.write("   :members:\n")
        fl.write("   :inherited-members:\n")
        fl.write("\n   .. automethod:: " + class_name + ".__init__\n")

def create_module_rst(mod_name, no_members=False):
    with open(mod_name + ".rst", 'w') as fl:
        fl.write(heading(mod_name))
        fl.write("\n.. automodule:: " + mod_name + "\n")
        #fl.write("   :members:\n")
        #fl.write("   :undoc-members:\n")
        #fl.write("   :show-inheritance:\n")
        #fl.write("   :inherited-members:\n")

        modules, classes, methods, functions, attributes = inspect_members(mod_name)
        if len(attributes)>0:
            fl.write(heading("\nAttributes", "-"))

            for att in attributes:
                if att[0] not in exclude:
                    att = mod_name + "." + att[0]
                    fl.write(".. py:data:: " + att + "\n\n")
                    #t = eval("type(" + att + ")")
                    if att.find("EXPYRIMENT_LOGO_FILE") == -1:
                        # do not write default for EXPYRIMENT_LOGO_FILE
                        v = eval("repr(" + att + ")")
                        fl.write("   default value: {0}\n\n".format(v))

        if len(modules)>0:
            fl.write(heading("\n\nModules", "-"))
            fl.write(".. toctree::\n   :maxdepth: 1\n   :titlesonly:\n")

            for m in modules:
                if m[0] not in exclude:
                    fl.write("\n   " + mod_name + "." + m[0])
                    create_module_rst(mod_name + "." + m[0])

        if len(classes)>0:
            fl.write(heading("\n\nClasses", "-"))
            fl.write(".. toctree::\n   :titlesonly:\n")

            for cl in classes:
                if cl[0] not in exclude:
                    fl.write("\n   " + mod_name + "." + cl[0])
                    create_class_rst(mod_name + "." + cl[0])

        if len(functions)>0:
            fl.write(heading("\n\nFunctions", "-"))
            for func in functions:
                if func[0] not in exclude:
                    fl.write(".. autofunction:: " + mod_name + "." + func[0] + "\n")

        fl.write("\n\n")
        #fl.write("\n\n.. "+repr(modules) + "\n")
        #fl.write(".. "+repr(classes) + "\n")
        #fl.write(".. "+repr(methods) + "\n")
        #fl.write(".. "+repr(functions) + "\n")
        #fl.write(".. "+repr(attributes) + "\n")


def create_change_log_rst():
    """create well shaped Changelog.rst from CHANGES.md"""

    changes_md = os.path.join(p, "CHANGES.md")
    changelog_rst = "Changelog.rst"

    fl = open(changes_md, 'r')
    out = open(changelog_rst, 'w')

    out.write("""Changelog
==========

""")

    version_found = False
    for line in fl:
        if line.startswith("Version"):
            version_found = True
        if version_found:
            if line.startswith("New Feature") or line.startswith("Fixed") or\
                    line.startswith("Changes") or line.startswith("Changed"):
                out.write("\n" + line + "\n")  # additional blanklines
            elif line.startswith("--"):
                out.write(line + "\n")
            elif line.startswith("  - "):
                out.write("\n" + line)
            else:
                out.write(line)

    out.close()
    fl.close()

def make_cli_rst():
    """Make commandline interface docu"""
    from expyriment.cli import cli_documentation
    with open("CommandLineInterface.rst", 'w') as fl:
         fl.write("""
Command line interface
======================

Usage
-----
::

""")
         s = cli_documentation.replace("\n", "\n    ")
         fl.write("\n    " + s)


# main module
if __name__ == '__main__':

    with open("expyriment.rst", 'w') as fl:
        fl.write("""
expyriment
==========

.. automodule:: expyriment


Packages
--------

.. toctree::
   :maxdepth: 1
   :titlesonly:

   expyriment.control
   expyriment.design
   expyriment.io
   expyriment.misc
   expyriment.stimuli

Functions
---------
.. autofunction:: expyriment.get_version
.. autofunction:: expyriment.show_documentation

""")

    sub_modules = ["expyriment.io", "expyriment.design", "expyriment.stimuli",
               "expyriment.control", "expyriment.misc"]

    #sub_modules
    for mod_name in sub_modules:
        create_module_rst(mod_name)

    create_change_log_rst()
    make_cli_rst()
