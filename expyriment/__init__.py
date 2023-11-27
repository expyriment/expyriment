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

__version__ = '0.10.dev0'

import sys as _sys

if _sys.version_info[0] != 3 or _sys.version_info[1] < 6:

    raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with Python {0}.{1}.".format(
                                                    _sys.version_info[0],
                                                    _sys.version_info[1]) +
                      "\n\n  Please use Python 3.6+. Note, the last major "
                      "release compatible with Python 2.7\n"
                      "  is Expyriment 0.10.")

try:
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame as _pygame
    if _pygame.vernum < (1, 9, 1) or _pygame.vernum >= (3, 0, 0):
        raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with Pygame {0}.{1}.{2}.".format(
                          _pygame.vernum[0], _pygame.vernum[1],
                          _pygame.vernum[2]) +
                      "\nPlease install Pygame(>=1.9,<3)).")
except ImportError:
    raise ImportError("Expyriment {0} ".format(__version__) +
                      "needs the package 'Pygame')." +
                      "\nPlease install Pygame(>=1.9,<3).")

try:
    import OpenGL as _OpenGL
    if not int(_OpenGL.version.__version__[0]) == 3:
        raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with PyOpenGL {0}.{1}.{2}.".format(
                        int(_OpenGL.version.__version__[0]),
                        int(_OpenGL.version.__version__[2]),
                        int(_OpenGL.version.__version__[4]),
                          ) +
                      "\nPlease install PyOpenGL(>=3,<4).")
except ImportError:
    print("No OpenGL support!" +
                    "\nExpyriment {0} ".format(__version__) +
                      "needs the package 'PyOpenGL'."
                      "\nPlease install PyOpenGL(>=3,<4) for OpenGL functionality.")


from ._internals import get_version, import_all_extras
print("Expyriment {0} ".format(get_version()))


# Check if local 'test.py{c|o}' shadows 'test' package of standard library
try:
    from importlib.util import find_spec as _find_spec
    for _package in ["test"]:
        if _find_spec(_package).submodule_search_locations is None:
            _m = "Warning: '{0}.py' is shadowing package '{1}'!"
            print(_m.format(_package, _package))
except Exception:
    pass

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

