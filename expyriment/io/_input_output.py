"""
The base module of io.

This module contains the base classes for input and output.

All classes in this module should be called directly via expyriment.io.*.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import expyriment

class Input(expyriment._Expyriment_object):
    """A class implementing a general input."""

    def __init__(self):
        """Create an input."""
        expyriment._Expyriment_object.__init__(self)


class Output(expyriment._Expyriment_object):
    """A class implementing a general output."""

    def __init__(self):
        """Create an output."""
        expyriment._Expyriment_object.__init__(self)
