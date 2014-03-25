"""Python library for cognitive and neuroscientific experiments.

Expyriment is an open-source and platform independent light-weight Python
library for designing and conducting timing-critical behavioural and
neuroimaging experiments. The major goal is to provide a well-structured
Python library for a script-based experiment development with a high priority
on the readability of the resulting programme code. It has been tested
extensively under Linux and Windows.

Expyriment is an all-in-one solution, as it handles the stimulus presentation,
recording of I/O events, communication with other devices and the collection
and preprocessing of data. It offers furthermore a hierarchical design
structure, which allows an intuitive transition from the experimental design
to a running programme. It is therefore also suited for students as well as
experimental psychologists and neuroscientists with little programming
experience.

Website: http://www.expyriment.org

To cite Expyriment in publications, please refer to the following article:

  Krause, F. & Lindemann, O. (2013). Expyriment: A Python library for cognitive
  and neuroscientific experiments. Behavior Research Methods.

  see http://dx.doi.org/10.3758/s13428-013-0390-6

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import sys as _sys
import os as _os
from hashlib import sha1 as _sha1



class _Expyriment_object(object):
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


def get_version():
    """
    Return version information about Expyriment and Python.

    Returns
    -------
    version_info : str

    Notes
    -----
    For more detailed information see expyriment.get_system_info().

    """

    pv = "{0}.{1}.{2}".format(_sys.version_info[0],
                              _sys.version_info[1],
                              _sys.version_info[2])
            #no use of .major, .minor to ensure MacOS compatibility
    return "{0} (Revision {1}; Python {2})".format(__version__, \
                               __revision__, pv)

_secure_hash = ""
def get_experiment_secure_hash():
    """Returns the fingerprint, that is, the first six places of the secure
    hash (sha1) of the main file of the current experiment.

    Returns
    -------
    hash: string or None
        first six places of the experiment secure hash or None, if no main
        file can be found

    Notes
    -----
    Fingerprints of experiments help to ensure that the correct version is
    running in the lab. Hash codes are written to all output files and
    printed in the command line output. If you want to check post hoc the
    version of your experiment, create the secure hash (sha1) of your
    expyriment .py-file and compare the first six place with the code in the
    output file.

    """

    global _secure_hash
    if _secure_hash != "":
        return _secure_hash

    try:
        with open(_os.path.split(_sys.argv[0])[1]) as f:
            _secure_hash = _sha1(f.read()).hexdigest()[:6]
    except:
        _secure_hash = None
    return get_experiment_secure_hash()



if not(_sys.version_info[0] == 2 and (_sys.version_info[1] == 6 or
                                         _sys.version_info[1] == 7)):
    raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with Python {0}.{1}.".format(
                                                    _sys.version_info[0],
                                                    _sys.version_info[1]) +
                      "\nPlease use Python 2.6 or Python 2.7.")
else:
    print("Expyriment {0} ".format(get_version()))
    if get_experiment_secure_hash() is not None:
        print("File: {0} ({1})".format(_os.path.split(_sys.argv[0])[1],
                    get_experiment_secure_hash()))
try:
    import pygame as _pygame
    if _pygame.vernum < (1, 9, 1):
        raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with Pygame {0}.{1}.{2}.".format(
                                                    _pygame.vernum) +
                      "\nPlease install Pygame 1.9.")
except ImportError:
    raise ImportError("Expyriment {0} ".format(__version__) +
                      "needs the package 'Pygame')." +
                      "\nPlease install Pygame 1.9.")

try:
    import OpenGL as _OpenGL
    if int(_OpenGL.version.__version__[0]) < 3:
        raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with PyOpenGL {0}.{1}.{2}.".format(
                        int(_OpenGL.version.__version__[0]),
                        int(_OpenGL.version.__version__[2]),
                        int(_OpenGL.version.__version__[4]),
                          ) +
                      "\nPlease install PyOpenGL 3.0.")
except ImportError:
    print("No OpenGL support!" +
                    "\nExpyriment {0} ".format(__version__) +
                      "needs the package 'PyOpenGL'."
                      "\nPlease install PyOpenGL 3.0 for OpenGL functionality.")

import design
_active_exp = design.Experiment("None")
import control
import stimuli
import io
import misc
misc.add_fonts(misc.str2unicode(_os.path.abspath(
    _os.path.join(_os.path.dirname(__file__),
                  "_fonts"))))

try:
    import android
except ImportError:
    from _api_reference_tool import show_documentation
from _get_system_info import get_system_info
import _importer_functions


exec(_importer_functions.post_import_hook())
