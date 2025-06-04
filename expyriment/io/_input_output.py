"""
The base module of io.

This module contains the base classes for input and output.

All classes in this module should be called directly via expyriment.io.*.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from .._internals import Expyriment_object


class Input(Expyriment_object):
    """A class implementing a general input."""

    def __init__(self):
        """Create an input."""
        Expyriment_object.__init__(self)


class Output(Expyriment_object):
    """A class implementing a general output."""

    def __init__(self):
        """Create an output."""
        Expyriment_object.__init__(self)
