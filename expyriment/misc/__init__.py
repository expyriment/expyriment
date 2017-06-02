"""The misc package.

This package contains miscellaneous classes, modules and functions.

See also expyriment.misc.extras for more misc.

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
              Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from . import defaults
from ._miscellaneous import compare_codes, add_fonts, list_fonts, find_font
from ._miscellaneous import unicode2byte, byte2unicode, numpad_digit_code2ascii
from ._miscellaneous import get_monitor_resolution, is_idle_running, is_ipython_running, \
                            is_android_running, is_interactive_mode, create_colours, \
                            has_internet_connection, which, download_from_stash
from ._get_system_info import get_system_info
from ._secure_hash import get_module_hash_dictionary, get_experiment_secure_hash, module_hashes_as_string
from . import constants
from ._buffer import  Buffer, ByteBuffer
from ._clock import Clock
from ._hsv_colour import HSVColour
from . import geometry
from . import data_preprocessing
from . import statistics

from os import path as _path
add_fonts(byte2unicode(_path.abspath(_path.join(_path.dirname(__file__),
                  "_fonts"))))
