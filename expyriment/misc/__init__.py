"""The misc package.

This package contains miscellaneous classes, modules and functions.

See also expyriment.misc.extras for more misc.

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
              Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import constants
import defaults
from _miscellaneous import compare_codes, list_fonts, find_font
from _buffer import  Buffer, ByteBuffer
from _clock import Clock
from _old_clock import OldClock
import geometry
import data_preprocessing
import statistics
import extras
