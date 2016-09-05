"""Expyriment internal function and variables

This module also contains the currently active experiment:
            active_exp
"""

from builtins import object

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import sys
import os

import pygame

try:
    import android
except ImportError:
    android = None


def get_version():
    """
    Return version information about Expyriment and Python.

    Returns
    -------
    version_info : str

    Notes
    -----
    For more detailed information see expyriment.misc.get_system_info().

    """

    pv = "{0}.{1}.{2}".format(sys.version_info[0],
                              sys.version_info[1],
                              sys.version_info[2])
            #no use of .major, .minor to ensure MacOS compatibility
    return "{0} (Python {1})".format(__version__, pv)


# GLOBALLY NEEDED STUFF

PYTHON3 = (sys.version_info[0] == 3)

active_exp = None  # expyriment.design.__init__ sets active_exp to
                   # design.Experiment("None")
                   # Provides the access to the currently active experiment
                   # import ._internals to read and write _active.exp

skip_wait_methods = False  # global toggle, can be changed by set_develop_mode

def is_base_string(s):
    if PYTHON3:
        return isinstance(s, (str, bytes))
    else:
        return isinstance(s, (unicode, str))

def is_unicode_string(s):
    if PYTHON3:
        return isinstance(s, str)
    else:
        return isinstance(s, unicode)

def is_byte_string(s):
    if PYTHON3:
        return isinstance(s, bytes)
    else:
        return isinstance(s, str)

def pump_pygame_events():
    pygame.event.pump()

class Expyriment_object(object):
    """A class implementing a general Expyriment object.
       Parent of all stimuli and IO objects

    """

    def __init__(self):
        """Create an Expyriment object."""
        self._logging = True

    def set_logging(self, onoff):
        """Set logging of this object on or off

        Parameters
        ----------
        onoff : bool
            set logging on (True) or off (False)

        Notes
        -----
        See also design.experiment.set_log_level fur further information about
        event logging.

        """

        self._logging = onoff

    @property
    def logging(self):
        """Getter for logging."""

        return self._logging

class CallbackQuitEvent(object):
    """A CallbackQuitEvent

    If a callback function returns a CallbackQuitEvent object the currently processed
    the wait or event loop function will be quited.
    """

    def __init__(self, data=None):
        """Init CallbackQuitEvent

        Parameter
        ---------
        data: any data type, optional
            You might use this variable to return data or values from your callback
            function to your main function, since the quited wait or event loop function
            will return this CallbackQuitEvent.

        See Also
        --------
        experiment.register_wait_callback_function()

        """

        self.data = data

    def __str__(self):
        return "CallbackQuitEvent: data={0}".format(self.data)


# IMPORTER FUNCTIONS

def import_command(path):
    # helper function to generate import command for extras that is Python2/3 compatible
    if PYTHON3:
        return "compile(open('{0}', 'rb').read(), '{0}', 'exec')\n".format(path)
    else:
        return "execfile(r'{0}')\n".format(path)


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
    folder = os.path.dirname(init_filename)
    for _filename in os.listdir(folder):
        if _filename.endswith("_defaults.py"):
            code.append( import_command(folder + os.sep +  _filename) )
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
                code.append( import_command(folder + os.sep + _filename) )
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
        return import_command(filename)
    else:
        return ""

