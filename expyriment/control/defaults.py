"""
Default settings for the control package.

This module contains default values for all optional arguments in the init
function of all classes in this package.

"""

__author__ = 'Florian Krause <florian@expyriment.org, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from expyriment.misc import constants as _constants

initialize_delay = 10  # After approximately 10 seconds Python is timecritical
auto_create_subject_id = False
goodbye_text = "Ending experiment..."
goodbye_delay = 3000
fast_quit = False
quit_key = _constants.K_ESCAPE
pause_key = _constants.K_p

open_gl = True
window_mode = False
window_size = (800, 600)

stdout_logging = True

audiosystem_autostart = True
audiosystem_sample_rate = 44100
audiosystem_bit_depth = -16  # Negative values mean signed sample values
audiosystem_channels = 2
audiosystem_buffer_size = 2048

_mode_settings = None
_skip_wait_functions = False
_intensive_logging = None
