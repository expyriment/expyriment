"""
Importer functions.

This module contains helper function needed for importing plugins (extras) and
for reading config file while import

"""
from __future__ import print_function

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import os
import sys

try:
    import android
except ImportError:
    android = None


def import_plugins(init_filename):
    """Return the code to import all plugins of extra package as dict.

    Parameters
    ----------
    init_filename : string
        fullpath to the __init__ file of the particular extra package

    Returns
    -------
    out : string

    """

    code = {}
    for filename in os.listdir(os.path.dirname(init_filename)):
        if filename.endswith(".py") and not (filename.startswith("__") or\
                                             filename.endswith("defaults.py")):
            f = open(os.path.dirname(init_filename) + os.sep + filename)
            try:
                for line in f:
                    if line[0:6] == "class ":
                        tmp = line[6:].lstrip()
                        name = tmp[:len(filename[:-4])]
                        break
                code[filename] = "from .{0} import {1}\n".format(filename[:-3],
                                                                name)
            except:
                print("Warning: Could not import {0}!".format(
                    os.path.dirname(init_filename) + os.sep + filename))
    return code

def import_plugin_defaults(init_filename):
    """Return the code to import all defaults of extra package as list.

    Parameters
    ----------
    init_filename : string
        fullpath to the __init__ file of the particular extra package

    Returns
    -------
    out : string

    """

    # extra defaults
    code = []
    for _filename in os.listdir(os.path.dirname(init_filename)):
        if _filename.endswith("_defaults.py"):
            code.append("execfile(r'{0}')\n".format(os.path.dirname(
                init_filename) + os.sep + os.sep + _filename))
    return code


def get_settings_folder():
    """Return for expyriment setting folder in $HOME"""
    home = os.getenv('USERPROFILE')
    if home is None:
        if android is not None:
            home = "/storage/sdcard0/"
        else:
            home = os.getenv('HOME')
    for expy_homefolder in [".expyriment", "~expyriment"]:
        path = home + os.sep + expy_homefolder
        if os.path.isdir(path):
            return path
    return None

def import_plugins_from_settings_folder(init_filename):
    """Return the code to import all plugins from the settings folder as dict.

    Includes the module folder in $home to the path.

    Returns
    -------
    out : string

    """

    module = init_filename.split(os.sep)[1]
    folder = get_settings_folder()
    if folder is None:
        return ""

    folder = folder + os.sep + module + os.sep
    code = {}
    sys.path.append(folder)
    try:
        for filename in os.listdir(os.path.dirname(folder)):
            if filename.endswith(".py") and\
                                not (filename.startswith("__") or\
                                filename.endswith("defaults.py")):
                f = open(os.path.dirname(folder) + os.sep + filename)
                try:
                    for line in f:
                        if line[0:6] == "class ":
                            tmp = line[6:].lstrip()
                            name = tmp[:len(filename[:-4])]
                            break
                    code[filename] = "from .{0} import {1}\n".format(filename[:-3],
                                                                    name)
                    print("import .{0}.extras.{1} (from homefolder)".format(
                                                        module, name))
                except:
                    print("Could not import {0}!".format(
                        os.path.dirname(folder) + os.sep + filename))
    except:
        pass
    return code

def import_plugin_defaults_from_home(init_filename):
    """Return the code to import all defaults of extra package as list.

    Parameters
    ----------
    init_filename : string
        fullpath to the __init__ file of the particular extra package

    """

    module = init_filename.split(os.sep)[1]
    folder = get_settings_folder()
    if folder is None:
        return ""

    folder = folder + os.sep + module + os.sep
    code = []
    try:
        for _filename in os.listdir(os.path.dirname(folder)):
            if _filename.endswith("_defaults.py"):
                code.append("execfile(r'{0}')\n".format(os.path.dirname(
                    folder) + os.sep + os.sep + _filename))
    except:
        pass
    return code

def post_import_hook():
    """Execute post import file."""

    home = get_settings_folder()
    if home is None:
        return ""

    filename = home + os.sep + "post_import.py"
    if os.path.isfile(filename):
        print("process {0}".format(filename))
        return "execfile(r'{0}')\n".format(filename)
    else:
        return ""
