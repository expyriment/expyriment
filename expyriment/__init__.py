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
from __future__ import absolute_import
from builtins import object as _object

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from ._get_system_info import get_system_info, get_version, PYTHON3, \
                                _python_version_info

if not( (_python_version_info[0] == 2 and _python_version_info[1] >= 6) or
        (PYTHON3 and _python_version_info[1] >= 3) ):
    raise RuntimeError("Expyriment {0} ".format(__version__) +
                      "is not compatible with Python {0}.{1}.".format(
                                                    _python_version_info[0],
                                                    _python_version_info[1]) +
                      "\nPlease use Python 2.6+ or Python 3.3+.")
else:
    print("Expyriment {0} ".format(get_version()))
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

from . import _active
from . import design
from . import misc
from . import stimuli
from . import io
from . import control
try:
    import android
except ImportError:
    from ._api_reference_tool import show_documentation
from . import _importer_functions
exec(_importer_functions.post_import_hook())

