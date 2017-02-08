
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

from types import ModuleType, FunctionType
from . import _midiin_defaults as defaults
from ... import _internals
from ..._internals import CallbackQuitEvent
from ...misc._timer import get_time
from ...io._keyboard import Keyboard
from ...io._input_output import Input


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

        if not isinstance(_midi, ModuleType):
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

    def wait(self, events, duration=None, callback_function=None,
             process_control_events=True):
        """Wait for (a) certain event(s).

        Events to wait for are in the form of a list with 4 elements and do
        not include a timestamp: [status, data1, data2, data3]

        Parameters
        ----------
        events : int or list
            event(s) to wait for
        duration : int, optional
            maximal time to wait in ms
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = True)

        Returns
        -------
        evt : int
            found event
        rt : int
            reaction time in ms

        Notes
        -----
        This will also by default process control events (quit and pause).
        Thus, keyboard events will be cleared from the cue and cannot be
        received by a Keyboard().check() anymore!

        See Also
        --------
        design.experiment.register_wait_callback_function

        """

        if _internals.skip_wait_methods:
            return None, None
        start = get_time()
        rt = None
        _event = None
        self.clear()
        if isinstance(events, (list, tuple)) and \
           len(events) == 4 and \
           isinstance(events[0], int) and \
           isinstance(events[1], int) and \
           isinstance(events[2], int) and \
           isinstance(events[3], int):
            events = [events]
        done = False
        while not done:
            if isinstance(callback_function, FunctionType):
                callback_function()
            if _internals.active_exp is not None and \
               _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    _event = rtn_callback
                    rt = int((get_time() - start) * 1000)
                    break
                if process_control_events:
                    if _internals.active_exp.mouse.process_quit_event() or \
                       _internals.active_exp.keyboard.process_control_keys():
                        break
                else:
                    _internals.pump_pygame_events()
            event = self.read(1)
            if event is not None and event[0][0] in events:
                rt = int((get_time() - start) * 1000)
                _event = event[0][0]
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
