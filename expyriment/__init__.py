"""Python library for cognitive and neuroscientific experiments.

Expyriment is an open-source and platform independent light-weight Python
library for designing and conducting timing-critical behavioural and
neuroimaging experiments. The major goal is to provide a well-structured
Python library for a script-based experiment development with a high priority
on the readability of the resulting programme code. Due to the availability of
an Android runtime environment, Expyriment is also suitable for the
development of experiments running on tablet PCs or smart-phones.

Expyriment has been tested extensively under Linux and Windows and is an
all-in-one solution, as it handles stimulus presentation, the recording of
input/output events, communication with other devices, and the collection
and preprocessing of data. Furthermore, it offers a hierarchical design
structure, which allows for an intuitive transition from the experimental
design to a running program. It is therefore also suited for students, as well
as for experimental psychologists and neuroscientists with little programming
experience.

Website: http://www.expyriment.org

To cite Expyriment in publications, please refer to the following article:

  Krause, F., & Lindemann, O. (2014). Expyriment: A Python library for cognitive
  and neuroscientific experiments. *Behavior Research Methods*, 46(2), 416-428.

  see http://dx.doi.org/10.3758/s13428-013-0390-6

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import sys as _sys
from ._internals import get_version, import_all_extras
from ._internals import PYTHON3 as _PYTHON3

if not( (_sys.version_info[0] == 2 and _sys.version_info[1] >= 6) or
        (_PYTHON3 and _sys.version_info[1] >= 3) ):
    raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with Python {0}.{1}.".format(
                                                    _sys.version_info[0],
                                                    _sys.version_info[1]) +
                      "\nPlease use Python 2.6+ or Python 3.3+.")
else:
    print("Expyriment {0} ".format(get_version()))

# Check if local 'test.py{c|o|d}' shadows 'test' package of standard library
try:
    import imp as _imp
    import os as _os
    import sys as _sys
    for _package in ["test"]:
        _tf = _os.path.abspath(_imp.find_module(_package)[1])
        _mf = _os.path.abspath(_os.path.abspath(_sys.argv[0]))
        if _os.path.split(_tf)[0] == _os.path.split(_mf)[0] or \
                _os.path.split(_tf)[0] == _os.path.abspath(_os.path.curdir):
                    _m = "Warning: "
                    _m += "'{0}' is shadowing package '{1}'!"
                    print(_m.format(_tf, _package))
except:
    pass

try:
    import future as _future
    if int(_future.__version__.split(".")[1]) < 15:
      raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with Future {0}".format(
                        _future.__version__) +
                      "\nPlease install Future >= 0.15.")
except ImportError:
    raise ImportError("Expyriment {0} ".format(__version__) +
                      "needs the package 'Future')." +
                      "\nPlease install Future >= 0.15.")

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

from . import _internals
from . import design
from . import misc
from . import stimuli
from . import io
from . import control

if not misc.is_android_running():
    from ._api_reference_tool import show_documentation

# add extras folder if it exists
if _internals.get_plugins_folder() is not None:
    _sys.path.append(_internals.get_plugins_folder())

# post import hook
exec(_internals.post_import_hook())

