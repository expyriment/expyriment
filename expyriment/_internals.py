"""Expyriment internal function and variables

This module also contains the currently active experiment:
            active_exp
"""

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'

import os
import sys

import pygame

from . import __version__


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

active_exp = None  # expyriment.design.__init__ sets active_exp to
                   # design.Experiment("None")
                   # Provides the access to the currently active experiment
                   # import ._internals to read and write _active.exp

skip_wait_methods = False  # global toggle, can be changed by set_develop_mode


class Expyriment_object:
    """A class implementing a general Expyriment object.

       Parent of all stimuli and IO objects.

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

        See Also
        --------
        expyriment.design.Experiment.set_log_level

        """

        self._logging = onoff

    @property
    def logging(self):
        """Getter for logging."""

        return self._logging


class CallbackQuitEvent:

    """A CallbackQuitEvent.

    If a callback function returns a CallbackQuitEvent object the currently processed
    the wait or event loop function will be quited.

    """

    def __init__(self, data=None):
        """Init CallbackQuitEvent.

        Parameters
        ----------
        data : any data type, optional
            you might use this variable to return data or values from your
            callback function to your main function, since the quited wait or
            event loop function will return this CallbackQuitEvent

        See Also
        --------
        expyriment.design.Experiment.register_wait_callback_function

        """

        self.data = data

    def __str__(self):
        return "CallbackQuitEvent: data={0}".format(self.data)


# IMPORTER FUNCTIONS

def _run_py_file_command(path):
    # helper function to generate import command
    return "compile(open('{0}', 'rb').read(), '{0}', 'exec')\n".format(path)

def is_venv():
    """Return if Exyriment is running in a virtual environment.

    Returns
    -------
    venv : bool
        whether or not running in virtual environment

    Note
    ----
    Only covers virual environments created with `virtualenv`, `venv`, and
    `pyvnenv`.

    """

    real_prefix = getattr(sys, "real_prefix", None)
    base_prefix = getattr(sys, "base_prefix", sys.prefix)

    return (base_prefix or real_prefix) != sys.prefix

def get_settings_folder():
    """Return Expyriment settings folder

    If running in a virtual environment, the Expyriment settings folder is
    `/path/to/environment/.expyriment/`, otherwise it is `$HOME/.expyriment`
    (or `$HOME/~expyriment/` if it exists).

    Returns
    -------
    settings_folder : str
        the Expyriment settings folder

    """

    home = os.getenv('USERPROFILE')
    if home is None:
        try:
            sys.getandroidapilevel()
            home = "/storage/sdcard0/"
        except AttributeError:
            home = os.getenv('HOME')
    if is_venv():
        home = sys.prefix
    if os.path.isdir(os.path.join(home, "~expyriment")):
        return os.path.join(home, "~expyriment")
    else:
        return os.path.join(home, ".expyriment")

def get_plugins_folder():
    """Return plugin folder in Expyriment settings folder, if it exists"""

    settings_folder = get_settings_folder()
    if not os.path.isdir(settings_folder):
        return None
    path = os.path.join(settings_folder, "extras")
    if os.path.isdir(path):
        return path
    else:
        return None

def import_plugins_code(package):
    """Return the code to import all plugins from the settings folder as dict.

    Includes the module folder in $home to the path.

    Parameters
    ----------
    package : submodule name

    Returns
    -------
    out : string

    """

    code = {}
    extras_folder = get_plugins_folder()
    if extras_folder is None:
        return code
    package = "expyriment_" + package + "_extras"
    module_folder = os.path.abspath(os.path.join(extras_folder, package))

    if os.path.isdir(module_folder):
        for entry in os.listdir(module_folder):
            init_file = os.path.join(module_folder, entry, "__init__.py")
            if os.path.isfile(init_file):
                # find name of first class --> class_name
                class_name = None
                with open(init_file) as init_fl:
                    for line in init_fl:
                        if line.strip().startswith("class "):
                            line = line[(line.find("class ")+6):]
                            e = (line.find("("), line.find(":"))
                            if e[1]>1:
                                if e[0]>1:
                                    e = min(e)
                                else:
                                    e = e[1]
                                class_name = line[:e]
                                break # file loop (for..)

                if class_name is not None:
                    code[class_name] = "from {0}.{1} import {2}\n".format(package,
                                                                          entry, class_name)
    return code

def post_import_hook():
    """Execute post import file."""

    home = get_settings_folder()
    if home is None:
        return ""

    filename = home + os.sep + "post_import.py"
    if os.path.isfile(filename):
        print("process {0}".format(filename))
        return _run_py_file_command(filename)
    else:
        return ""

def import_all_extras():
    """Import all extra plugins."""

    from .design import extras
    from .misc import extras
    from .io import extras
    from .stimuli import extras
