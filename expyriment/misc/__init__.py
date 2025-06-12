"""The misc package.

This package contains miscellaneous classes, modules and functions.

See also expyriment.misc.extras for more misc.

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
              Oliver Lindemann <oliver@expyriment.org>'

from os import path as _path

from . import constants, data_preprocessing, defaults, geometry, statistics
from ._buffer import Buffer, ByteBuffer
from ._clock import Clock
from ._colour import Colour
from ._get_system_info import get_system_info
from ._miscellaneous import (
                  MediaTime,
                  add_fonts,
                  byte2unicode,
                  compare_codes,
                  create_colours,
                  download_from_stash,
                  find_font,
                  get_audio_devices,
                  get_display_info,
                  get_monitor_resolution,
                  has_internet_connection,
                  is_android_running,
                  is_idle_running,
                  is_interactive_mode,
                  is_ipython_running,
                  list_fonts,
                  numpad_digit_code2ascii,
                  round,
                  string_sort_array,
                  unicode2byte,
                  which,
)
from ._secure_hash import (
                  get_experiment_secure_hash,
                  get_module_hash_dictionary,
                  module_hashes_as_string,
)

add_fonts(byte2unicode(_path.abspath(_path.join(_path.dirname(__file__),
                  "..", "_fonts"))))
