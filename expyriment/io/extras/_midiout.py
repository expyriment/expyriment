"""MIDI output.

This module contains a class implementing a MIDI output device.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from types import ModuleType
from . import _midiout_defaults as defaults
from ... import _internals
from ...io._input_output import Output

try:
    from pygame import midi as _midi
    _midi.init()
except:
    _midi = None

class MidiOut(Output):
    """A class implementing a MIDI output.

    **EXPERIMENTAL!**

    Due to a bug in Pygame's midi module, closing a MidiOut (or the programme)
    will cause an error message. Until this is fixed in Pygame, MidiOut will
    stay in extras.

    """

    @staticmethod
    def get_devices():
        """Get a list of all MIDI output devices connected to the system."""

        if _midi is None:
            return
        outdevices = []
        all_ids = _midi.get_count()
        for device_id in all_ids:
            info = _midi.get_device_info(device_id)
            if info[3] == 1:
                outdevices.add([device_id, info[1]])
        return outdevices

    def __init__(self, device, latency=None, buffer_size=None):
        """Create a MIDI output.

        Parameters
        ----------
        device : int or str
            id or name of the MIDI device
        latency : int, optional
            delay in ms applied to timestamp
        buffer_size : int, optional
            number of events to be buffered

        """

        if not isinstance(_midi,ModuleType):
            raise ImportError("""Sorry, MIDI output is not supported on this computer.""")

        if not _internals.active_exp.is_initialized:
            raise RuntimeError(
                "Cannot create MidiOut before expyriment.initialize()!")
        _midi.init()
        Output.__init__(self)
        self._id = device
        if buffer_size is None:
            buffer_size = defaults.midiout_buffer_size
        self._buffer_size = buffer_size
        if latency is None:
            latency = defaults.midiout_latency
        self._latency = latency
        self.output = _midi.Output(device, latency, buffer_size)

    @property
    def id(self):
        """Getter for id."""

        return self._id

    @property
    def buffer_size(self):
        """Getter for buffer_size."""

        return self._buffer_size

    @property
    def latency(self):
        """Getter for latency."""

        return self._latency

    def close(self, abort=False):
        """Close the MIDI interface.

        Parameters
        ----------
        abort : bool, optional
            abort messages in the buffer (default=True)

        """

        if abort:
            self.output.abort()
        self.output.close()

    def abort(self):
        """Terminates outgoing messages immediately."""

        self.output.abort()

    def send(self, event_list):
        """Send a list of MIDI events.

        Each event should have the following format:
            [status, data1, data2, data3], timestamp]

        Notes
        -----
        The data fields are optional.

        Parameters
        ----------
        event_list : list
            list of events to send

        """

        self.output.write(event_list)

    def send_short(self, status, data1=0, data2=0):
        """Send MIDI events of 3 bytes or less.

        Parameters
        ----------
        status : int
            status of the event to send
        data1 : int, optional
            data1 of the event to send
        data2 : int, optional
            data2 of the event to send

        """

        self.output.write_short(status, data1, data2)


    def send_sysex(self, timestamp, message):
        """Send a System Exlusive message.

        Parameters
        ----------
        timestamp : int
            when (in ms) to send the message
        message : sit or list
            message to send

        """

        self.output.wirte_sys_ex(timestamp, message)

    def select_instrument(self, instrument_id, channel=0):
        """Select an instrument.

        Parameters
        ----------
        instrument_id : int
            id (0-127) of the instrument
        channel : int, optional
            MIDI channel for the instrument (default=0)

        """

        self.output.set_instrument(instrument_id, channel)

    def send_note_on(self, note, velocity=None, channel=0):
        """Send a note-on event.

        Parameters
        ----------
        note : int
            note value
        velocity : int, optional
            velocity of the note
        channel : int, optional
            MIDI channel of the note (default=0)

        """

        self.output.note_on(note, velocity, channel)

    def send_note_off(self, note, velocity=None, channel=0):
        """Send a note-off event.

        Parameters
        ----------
        note : int
            note value
        velocity : int, optional
            velocity of the note
        channel : int, optional
            MIDI channel of the note (default=0)

        """

        self.output.note_off(note, velocity, channel)
