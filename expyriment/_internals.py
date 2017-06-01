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

def run_py_file_command(path):
    # helper function to generate import command for extras that is Python2/3 compatible
    if PYTHON3:
        return "compile(open('{0}', 'rb').read(), '{0}', 'exec')\n".format(path)
    else:
        return "execfile(r'{0}')\n".format(path)


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

def get_plugins_folder():
    """Return for expyriment plugin folder in $HOME if it exists"""

    settings_folder = get_settings_folder()
    if settings_folder is None:
        return None
    path = os.path.join(settings_folder, "extras")
    if os.path.isdir(path):
        return path
    else:
        return None


def import_plugins_code(submodule):
    """Return the code to import all plugins from the settings folder as dict.

    Includes the module folder in $home to the path.

    Parameters
    ----------
    submodule : submodule name

    Returns
    -------
    out : string

    """

    code = {}
    extras_folder = get_plugins_folder()
    if extras_folder is None:
        return code
    module_folder = os.path.abspath(os.path.join(extras_folder, submodule))

    if os.path.isdir(module_folder):
        sys.path.append(get_settings_folder())
        for filename in os.listdir(module_folder):
            if filename.endswith(".py") and\
                                not (filename.startswith("__") or\
                                filename.endswith("defaults.py")):
                f = open(os.path.join(module_folder, filename))
                try:
                    for line in f:
                        if line[0:6] == "class ":
                            tmp = line[6:].lstrip()
                            name = tmp[:len(filename[:-4])]
                            break
                    code[name] = "from extras.{0}.{1} import {2}\n".format(submodule,
                                                            filename[:-3], name)
                except:
                    print("Could not find a class in {0} !".format(
                                        os.path.join(module_folder, filename)))
    if len(code) >0:
        txt = "Plugins " + submodule + ": "
        for x in code.keys():
            txt += x + ", "
    return code

def import_plugins_defaults_code(submodule):
    """Return the code to import all defaults of extra package as list.

    Parameters
    ----------
    submodule : submodule name

     Returns
    -------
    out : string

    """

    code = []
    extras_folder = get_plugins_folder()
    if extras_folder is None:
        return code
    module_folder = os.path.abspath(os.path.join(extras_folder, submodule))
    if os.path.isdir(module_folder):
        for filename in os.listdir(module_folder):
            if filename.endswith("_defaults.py"):
                code.append(run_py_file_command(os.path.join(module_folder, filename)))
    return code

def post_import_hook():
    """Execute post import file."""

    home = get_settings_folder()
    if home is None:
        return ""

    filename = home + os.sep + "post_import.py"
    if os.path.isfile(filename):
        print("process {0}".format(filename))
        return run_py_file_command(filename)
    else:
        return ""

