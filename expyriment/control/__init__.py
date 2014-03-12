"""
The control package of expyriment.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import defaults
from _miscellaneous import start_audiosystem, stop_audiosystem, \
        get_audiosystem_is_playing, wait_end_audiosystem, \
        set_develop_mode, get_defaults, register_wait_callback_function, \
        unregister_wait_callback_function, is_idle_running, is_ipython_running, \
        is_android_running
from _experiment_control import initialize, start, pause, end
from _test_suite import run_test_suite
