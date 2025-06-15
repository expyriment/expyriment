"""
The base module of io.

This module contains the base classes for input and output.

All classes in this module should be called directly via expyriment.io.*.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from abc import ABC

from .._internals import ExpyrimentObject


class Input(ExpyrimentObject, ABC):
    """A class implementing a general input."""

    def __init__(self):
        """Create an input."""
        ExpyrimentObject.__init__(self)


class Output(ExpyrimentObject, ABC):
    """A class implementing a general output."""

    def __init__(self):
        """Create an output."""
        ExpyrimentObject.__init__(self)
