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
