"""
A marker output.

This module contains a class implementing a marker output

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from . import defaults
from  ._input_output  import Output
from ..misc._timer import get_time
from .. import _internals

class MarkerOutput(Output):
    """A class implementing a marker output."""

    def __init__(self, interface, default_code=None, default_duration=None):
        """Create a marker output.

        If a default code is specified, it will automatically be applied when
        send() is called without a code.
        If a default duration is specified, a 0 is sent automatically after
        the specifed duration when send() is called without a duration.

        Notes
        -----
        EEG/MEG systems:
        If the system is receiving the markers on a parallel port, the
        duration between sending a code an the subsequent 0 should be at least
        1000/samplerate!

        Parameters
        ----------
        interface : ``expyriment.io.SerialPort`` or ``expyriment.io.ParallelPort``
            the interface to use
        default_code : int, optional
            default code
        default_duration : int, optional
            default duration (in ms) for sending 0 after a code

        """

        Output.__init__(self)
        self._interface = interface
        if default_code is not None:
            self._default_code = default_code
        else:
            self._default_code = defaults.markeroutput_default_code
        if default_duration is not None:
            self._default_duration = default_duration
        else:
            self._default_duration = defaults.markeroutput_default_duration

    @property
    def interface(self):
        """Getter for interface"""
        return self._interface

    @property
    def default_code(self):
        """Getter for default_code"""
        return self._default_code

    @default_code.setter
    def default_code(self, value):
        """Getter for default_code"""
        self._default_code = value

    @property
    def default_duration(self):
        """Getter for default_duration"""
        return self._default_duration

    @default_duration.setter
    def default_duration(self, value):
        """Getter for default_duration"""
        self._default_duration = value


    def send(self, code=None, duration=None):
        """Send a marker.

        This sends a marker via the specified interface.
        If a duration is given, a 0 will be sent automatically after each
        code.

        Note for EEG/MEG systems:
        If the system is receiving the markers on a parallel port, the
        duration between sending a code an the subsequent 0 should be at least
        1000/samplerate!

        Parameters
        ----------
        code : int, optional
            a specific code
        duration : int, optional
            duration (in ms) for sending a 0 after a code

        """

        if not code:
            code = self.default_code
        if not duration:
            duration = self.default_duration
        self._interface.send(code)
        if duration:
            start = get_time()
            while (get_time() - start) * 1000 < duration:
                pass
        self._interface.send(0)
        if self._logging:
            _internals.active_exp._event_file_log(
                                        "MarkerOutput,sent,{0}".format(code))
