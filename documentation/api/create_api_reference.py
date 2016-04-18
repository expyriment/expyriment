#!/usr/bin/env python

"""
Create the API reference HTML documentation.

This script creates an HTML API documentation, based on the docstrings.
Importantly, it follows the actual namespace hierarchy and ignores everything
that starts with _.

"""


from __future__ import print_function

import __future__
import builtins


__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = '21-11-2011'


import os
import sys
import inspect  
import types
import imp


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
        if member[0][0:1] != '_' and member[0] not in exclude:
            #print(member)
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


def format_doc(doc):
    lines = doc.split("\n")
    cutoff = 0
    if len(lines) > 2:
        for char in lines[2]:
            if char != " ":
                break
            else:
                cutoff += 1
    for counter, line in enumerate(lines):
        if cutoff > 0 and line.startswith(" "*cutoff):
            lines[counter] = "    " + line[cutoff:]
        else:
            lines[counter] = "    " + line
    doc = "\n".join(lines)
    if doc[-1] != " ":
        doc = doc + "\n\n"
    return doc

def create_module_section(modules, item):
    section = ""
    for m in modules:
        section = section + "<span class='separator'>[</span><span class='module_name'><a href='" +\
        item + "." + m[0] + ".html'>" + m[0] + "</a></span><span class='separator'>] </span>"
    if section != "":
        section = "</pre><code><span class='section_heading'>Modules</span><br /><br />" + section + "<br /><br /><br /><br /></code><pre>"
    return section

def create_classes_section(classes, item):
    section = ""
    for c in classes:
        section = section + "<span class='separator'>[</span><span class='class_name'><a href='#" + c[0] + "'>" + c[0] + "</a></span><span class='separator'>] </span>"
    if section != "":
        section = "</pre><code><span class='section_heading'>Classes</span><br /><br />" + section + "<br /><br /><br /><br /></code><pre>"
    return section

def create_classes_details_section(classes, item):
    section = ""
    for c in classes:
        print(c)
        definition = "".join(inspect.getsourcelines(c[1])[0])
        start = definition.find("def __init__(self") + 17
        end = definition.find(")", start)
        if definition[start] == ",":
            call = "<span class='class_call'>(" + definition[start + 1:end].lstrip() + ")</span>"
        else:
            call = "<span class='class_call'>()</span>"
        call = call.replace(" " * 16, " " * len(c[0]))
        start = definition.find('"""', start) + 3
        end = definition.find('"""', start)
        doc = definition[start:end]
        if doc is None:
            doc = ""
        doc = format_doc(doc)
        section = section + "<span class='class_name'><a name='" + c[0] + "'></a><a href='" + item + "." + c[0] + ".html'>" + c[0] + "</a></span>" + call + "<span class='definition'><br /><br />" + doc + "</span><br />"
    if section != "":
        section = "<span class='section_heading'>Details (Classes)</span><br /><br />" + section + "<br />"
    return section

def create_methods_section(methods):
    section = ""
    for m in methods:
        section = section + "<span class='separator'>[</span><span class='method_name'><a href='#" + m[0] + "'>" + m[0] + "</a></span><span class='separator'>] </span>"
    if section != "":
        section = "</pre><code><span class='section_heading'>Methods</span><br /><br />" + section + "<br /><br /><br /><br /></code><pre>"
    return section

def create_methods_details_section(methods):
    section = ""
    for m in methods:
        definition = "".join(inspect.getsourcelines(m[1])[0])
        start = definition.find("(self") + 1
        end = definition.find(")")
        if definition[start + 4] == ",":
            call = "(" + definition[start + 5:end].lstrip() + ")"
        else:
            call = "()"
        call = call.replace("        " + " "*len(m[0]) + " ",
                            " "*len(m[0]) + " ")
        doc = m[1].__doc__
        if doc is None:
            doc = ""
        doc = format_doc(doc)
        section = section + "<span class='method_name'><a name='" + m[0] + "'></a>" + m[0] + "</span><span class='method_call'>" + call + "</span><br /><br />" + "<span class='definition'>" + doc + "</span><br />"
    if section != "":
        section = "<span class='section_heading'>Details (Methods)</span><br /><br />" + section + "<br />"
    return section

def create_functions_section(functions):
    section = ""
    for f in functions:
        section = section + "<span class='separator'>[</span><span class='function_name'><a href='#" + f[0] + "'>" + f[0] + "</a></span><span class='separator'>] <span/>"
    if section != "":
        section = "</pre><code><span class='section_heading'>Functions</span><br /><br />" + section + "<br /> <br /><br /><br /></code><pre>"
    return section

def create_functions_details_section(functions):
    section = ""
    for f in functions:
        definition = "".join(inspect.getsourcelines(f[1])[0])
        start = definition.find("(") + 1
        end = definition.find(")")
        call = definition[start:end]
        call = call.replace("    " + " "*len(f[0]) + " ",
                            " "*len(f[0] + " "))
        doc = f[1].__doc__
        if doc is None:
            doc = ""
        doc = format_doc(doc)
        section = section + "<span class='function_name'><a name='" + f[0] + \
             "'></a>" + f[0] + "</span><span class='function_call'>(" + call + \
             ")</span><br /><br />" + "<span class='definition'>" + doc + \
             "</span><br />"
    if section != "":
        section = "<span class='section_heading'>Details (Functions)</span>" + \
                    "<br /><br />" + section + "<br /> "
    return section

def create_attributes_section(attributes):
    section = ""
    for a in attributes:
        section = section + "<span class='separator'>[</span><span class='attribute_name'>" + \
        a[0] + "</span><span class='separator'>] </span>"
    if section != "":
         section = "</pre><code><span class='section_heading'>Attributes</span><br /><br />" + \
          section + "<br /><br /><br /><br /></code><pre>"
    return section

def create_page(item):
    modules, classes, methods, functions, attributes = inspect_members(item)
    trace = ""
    parts = item.split(".")
    if len(parts) > 1:
        for cnt, p in enumerate(parts[:-1]):
            if cnt > 0:
                link = "<a href='" + ".".join(parts[:cnt + 1]) + ".html'>" + parts[cnt]
            else:
                link = "<a href='" + p + ".html'>" + parts[cnt]
            trace = trace + link + "</a>" + "."
    title = "<span class='title'>" + trace + parts[-1] + "</span>"
    title = title + "<br />"
    doc = eval(item).__doc__
    if doc is None:
        doc = ""
    doc = format_doc(doc)
    doc = doc.lstrip()
    doc = doc.replace("\n    ", "\n")
    file_path = os.path.split(os.path.abspath(__file__))[0]
    p = os.path.abspath('{0}/../../CHANGES.md'.format(file_path))
    version_nr = "{0}"
    with open(p) as f:
        for line in f:
            if line[0:8].lower() == "upcoming":
                 version_nr += "+"
            if line[0:7] == "Version":
                version_nr = version_nr.format(line[8:13])
                break
    page = """
<html>
<head>
<link rel="shortcut icon" href="favicon.ico" type="image/x-icon" />
<title>API reference for {0} ({1})</title>
{2}
</head>
<pre>
{3}
<span class='definition'>{4}</span><br />
{5}{6}{7}{8}{9}
<hr >
{10}{11}{12}
</pre>
</html>""".format(item, version_nr, css, title, doc,
                  create_module_section(modules, item),
                  create_classes_section(classes, item),
                  create_methods_section(methods),
                  create_functions_section(functions),
                  create_attributes_section(attributes),
                  create_classes_details_section(classes, item),
                  create_methods_details_section(methods),
                  create_functions_details_section(functions))

    p = os.path.abspath("{0}/{1}.html".format(os.path.split(os.path.abspath(__file__))[0],
                        item))
    print("create", p)
    with open(p, 'w') as f:
        f.write(page)
    if modules:
        for m in modules:
            create_page(item + "." + m[0])

    if classes:
        for c in classes:
            create_page(item + "." + c[0])


if __name__ == "__main__":
    css = """
body {font-size:100%; color: #393333}
a {text-decoration:none; color:blue;}
a:visited {text-decoration:none;}
a:hover {text-decoration: underline;}
hr {color: #cccccc; background-color: #cccccc;}
.title {font-size:1.5em; font-weight:bold;}
.title_call {font-size:1.5em; font-weight:normal; font-style:italic;}
.definition {font-size:1em; color:#555555}
.section_heading {font-size:1.5em; font-weight:bold; color: #d14836;}
.separator {color:#777777;}
.module_name {font-size:1em; font-weight:bold;}
.class_name {font-size:1em; font-weight:bold;}
.class_call {font-size:1em; font-weight:normal; font-style: italic;}
.method_name {font-size:1em; font-weight:bold;}
.method_call {font-size:1em; font-weight:normal; font-style:italic;}
.function_name {font-size:1em; font-weight:bold;}
.function_call {font-size:1em; font-weight:normal; font-style:italic;}
.attribute_name {font-weight:bold;}"""

    css = "<style TYPE='text/css'>\n<!--\n" + css + "\n--!>\n</style>"

    cmd_folder = os.path.dirname(os.path.abspath(__file__+"/../../"))
    if cmd_folder not in sys.path:
        sys.path.insert(0, cmd_folder)
        import expyriment
        import expyriment.io.extras
        import expyriment.design.extras
        import expyriment.stimuli.extras
        import expyriment.misc.extras
        sys.path.remove(cmd_folder)
    create_page("expyriment")

    p = os.path.abspath("{0}/index.html".format(os.path.split(os.path.abspath(__file__))[0]))
    print("create", p)
    with open(p, 'w') as f:
        content = """<html><head><meta http-equiv="refresh" content="0; URL=expyriment.html"></head>"""
        f.write(content)
