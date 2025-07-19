"""
The control package of expyriment.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

from .._internals import CallbackQuitEvent
from . import defaults
from ._experiment_control import end, initialise, pause, start
from ._experiment_control import initialise as initialize
from ._miscellaneous import (
                             get_audiosystem_is_playing,
                             get_defaults,
                             register_wait_callback_function,
                             set_develop_mode,
                             start_audiosystem,
                             stop_audiosystem,
                             unregister_wait_callback_function,
                             wait_end_audiosystem,
)
from ._test_suite import run_test_suite
