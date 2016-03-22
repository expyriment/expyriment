
"""MIDI input.

This module contains a class implementing a MIDI input device.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from . import _midiin_defaults as defaults
from ... import _internals
from ...misc._timer import get_time
from ...io._keyboard import Keyboard
from ...io._input_output import Input
from ..defaults import _skip_wait_functions


import time

try:
    from pygame import midi as _midi
    _midi.init()
except:
    _midi = None


class MidiIn(Input):
    """A class implementing a MIDI input.

    **EXPERIMENTAL!**

    Due to a bug in Pygame's midi module, closing a MidiIn (or the programme)
    will cause an error message. Until this is fixed in Pygame, MidiIn will
    stay in extras.

    """
    @staticmethod
    def get_devices():
        """Get a list of all MIDI input devices connected to the system."""

        if _midi is None:
            return
        indevices = []
        all_ids = _midi.get_count()
        for device_id in all_ids:
            info = _midi.get_device_info(device_id)
            if info[2] == 1:
                indevices.add([device_id, info[1]])
        return indevices

    def __init__(self, device, buffer_size=None):
        """Create a MIDI input.

        Parameters
        ----------
        device : int or str
            id or name of the MIDI device
        buffer_size : int, optional
            number of events to be buffered

        """

        import types
        if type(_midi) is not types.ModuleType:
            raise ImportError("""Sorry, MIDI input is not supported on this computer.""")

        if not _internals.active_exp.is_initialized:
            raise RuntimeError(
                "Cannot create MidiIn before expyriment.initialize()!")
        _midi.init()
        Input.__init__(self)
        self._id = device
        if buffer_size is None:
            buffer_size = defaults.midiin_buffer_size
        self._buffer_size = buffer_size
        self.input = _midi.Input(device, buffer_size)

    @property
    def id(self):
        """Getter for id."""

        return self._id

    @property
    def buffer_size(self):
        """Getter for buffer_size."""

        return self._buffer_size

    def read(self, num_events=1):
        """Read MIDI events from device.

        Parameters
        ----------
        num_events : int, optional
            number of events to read (default=1)

        Returns
        -------
        out : timestpamed
            A timestpamed midi event will look like this:
            [status, data1, data2, data3], timestamp]

        """

        if self.input.poll():
            if self._logging:
                _internals.active_exp._event_file_log(
                    "MIDI In ({0}),received".format(self.id), 2)
            return self.input.read(num_events)

    def clear(self):
        """Clear the input buffer.

        This can take more than 1 ms!

        """

        for _i in range(self._buffer_size):
            self.input.read(1)
            if self._logging:
                _internals.active_exp._event_file_log(
                "MIDI In ({0}),cleared".format(self.id), 2)

    def wait(self, events, duration=None):
        """Wait for (a) certain event(s).

        Events to wait for are in the form of a list with 4 elements and do
        not include a timestamp: [status, data1, data2, data3]

        Parameters
        ----------
        events : int or list
            event(s) to wait for
        duration : int, optional
            maximal time to wait in ms

        Returns
        -------
        evt : int
            found event
        rt : int
            reaction time in ms

        See Also
        --------
        design.experiment.register_wait_callback_function

        """

        if _skip_wait_functions:
            return None, None
        start = get_time()
        rt = None
        _event = None
        self.clear()
        if type(events) is list and \
           len(events) == 4 and \
           type(events[0]) is int and \
           type(events[1]) is int and \
           type(events[2]) is int and \
           type(events[3]) is int:
            events = [events]
        done = False
        while not done:
            rtn_callback = _internals.active_exp._execute_wait_callback()
            if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                return rtn_callback, int((get_time() - start) * 1000)
            event = self.read(1)
            if event is not None and event[0][0] in events:
                rt = int((get_time() - start) * 1000)
                _event = event[0][0]
                done = True
                break
            if Keyboard.process_control_keys():
                done = True
                break
            if duration:
                if int((get_time() - start) * 1000) >= duration:
                    done = True
                    break

            time.sleep(0.0005)

        if self._logging:
            _internals.active_exp._event_file_log(
                "MIDI In ({0}),received,{1},wait".format(self.id, _event), 2)
        return _event, rt
