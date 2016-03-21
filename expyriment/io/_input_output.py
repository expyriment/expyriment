"""
The base module of io.

This module contains the base classes for input and output.

All classes in this module should be called directly via expyriment.io.*.

"""
from __future__ import absolute_import, print_function, division

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

from . import defaults
from .. import _Expyriment_object

class Input(_Expyriment_object):
    """A class implementing a general input."""

    def __init__(self):
        """Create an input."""
        _Expyriment_object.__init__(self)


class Output(_Expyriment_object):
    """A class implementing a general output."""

    def __init__(self):
        """Create an output."""
        _Expyriment_object.__init__(self)


def set_skip_wait_functions(onoff):
    """Switch on/off skip wait function.
    If skip-wait-functions is switch on (True) all wait functions in the
    experiment (i.e.  all wait function in expyriment.io and the clock) will
    be omitted.

    Notes
    -----
    CAUTION!: This functions is only usefull for experiment test runs. Do not use
    skip-wait-function while real experiments.

    Parameters
    ----------
    onoff : bool
        set skip-wait-function on (True) or off (False)

    """

    defaults._skip_wait_functions = onoff