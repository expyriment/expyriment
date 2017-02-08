"""
An event button box.

This module contains a class implementing an event button box.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from ._streamingbuttonbox import StreamingButtonBox


class EventButtonBox(StreamingButtonBox):
    """A class implementing an event button box input."""

    def __init__(self, interface):
        """Create an event button box input.

        Compared to a StreamingButtonBox, an EventButtonBox has no baseline
        (baseline=None). The methods wait() and check() are therefore
        responsive to every incomming interface event.

        Parameters
        ----------
        interface : ``expyriment.io.SerialPort`` or ``expyriment.io.ParallelPort``
            the interface to use

        """

        StreamingButtonBox.__init__(self, interface, None)

    @property
    def baseline(self):
        """Getter for baseline"""
        return self._baseline

    @baseline.setter
    def baseline(self, value):
        """Setter for baseline."""
        print("Warning: A baseline cannot be defined for an EventButtonBox!")
        self._baseline = None
