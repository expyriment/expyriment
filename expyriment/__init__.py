"""A Python library for cognitive and neuroscientific experiments.

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

Website: https://expyriment.org

To cite Expyriment in publications, please refer to the following article:

  Krause, F., & Lindemann, O. (2014). Expyriment: A Python library for cognitive
  and neuroscientific experiments. *Behavior Research Methods*, 46(2), 416-428.

  see https://doi.org/10.3758/s13428-013-0390-6

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

__version__ = '1.0.0.dev2'

import sys as _sys

if _sys.version_info[0] != 3 or _sys.version_info[1] < 9:

    raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with Python {0}.{1}.".format(
                                                    _sys.version_info[0],
                                                    _sys.version_info[1]) +
                      "\n\n  Please use Python 3.9+. Note, the last major "
                      "release compatible with Python 2.7\n"
                      "  is Expyriment 0.10.")

try:
    import os as _os
    _os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

    import pygame as _pygame
    if _pygame.vernum < (2, 5, 2) or _pygame.vernum >= (3, 0, 0):
        raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with Pygame {0}.{1}.{2}.".format(
                          _pygame.vernum[0], _pygame.vernum[1],
                          _pygame.vernum[2]) +
                      "\nPlease install Pygame(>=2.5.2,<3)).")
except ImportError:
    raise ImportError("Expyriment {0} ".format(__version__) +
                      "needs the package 'Pygame')." +
                      "\nPlease install Pygame(>=2.5.2,<3).")

try:
    import logging as _logging
    _logging.basicConfig(level=_logging.INFO)
    _logging.getLogger('OpenGL.plugins').setLevel(_logging.ERROR)
    _logging.getLogger('OpenGL.acceleratesupport').setLevel(_logging.ERROR)

    import OpenGL as _OpenGL
    _pyopengl_version = tuple(map(int, (_OpenGL.__version__.split("."))))

    if not _pyopengl_version[0] == 3:
        raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with PyOpenGL {0}.{1}.{2}.".format(
                        int(_OpenGL.version.__version__[0]),
                        int(_OpenGL.version.__version__[2]),
                        int(_OpenGL.version.__version__[4]),
                          ) +
                      "\nPlease install PyOpenGL(>=3,<4).")

    # Try patching PyOpenGL <= 3.1.7 for Python >= 3.12:
    # https://github.com/mcfletch/pyopengl/pull/100
    try:
      if _pyopengl_version <= (3, 1, 7) and _sys.version_info >= (3, 12):
          _OpenGL.FormatHandler.by_name("ctypesparameter").check.append(
              "_ctypes.CArgObject")
    except Exception:
      pass

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

from . import _internals, control, design, io, misc, stimuli

if not misc.is_android_running():
    from ._internals import show_documentation

# add extras folder if it exists
if _internals.get_plugins_folder() is not None:
    _sys.path.append(_internals.get_plugins_folder())

# post import hook
exec(_internals.post_import_hook())

