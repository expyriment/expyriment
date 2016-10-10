"""Cedrus XID response device.

This module contains a class implementing a Cedrus XID response device.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from types import ModuleType, FunctionType

try:
    import pyxid as _pyxid
except:
    _pyxid = None

from ...io._input_output import Input
from ... import _internals, stimuli, misc


class CedrusResponseDevice(Input):
    """A class implementing a Cedrus XID response device.

    Notes
    -----
    The CedrusResponseDevice class requires a free Python package for Cedrus
    devices called "pyxid".
    For installation instructions see Expyriment online documentation:
    http://docs.expyriment.org/Hardware.html.
    The class does not use the hardware timer, due to the known bug in the
    Cedrus hardware. Events will be time stamped by Expyriment. Thus, ensure
    constant polling / checking when not using the wait function.

    To install Cedrus resonse device under Linux, you have to set the USB product
    ID. To do so, edit the file /etc/modules and add the following line::

        ftdi_sio vendor=0403 product=f228

    """

    def __init__(self, device_ID=0, error_screen=True):
        """Create a Cedrus Device Input.

        Notes
        -----
        If no Cedrus device is connected, an error text screen will be
        presented informing that the device could not be found and suggesting
        to check the connection and to switch on the device. After keypress the
        class tries to reconnect with the device. Use <q> to quit this
        procedure.

        Parameters
        ----------
        device_id : int, optional
            device ID (default=0). Only required if more than one
            Cedrus Devices are connected.
        error_screen : bool, optional
            set False to switch off the 'device not found' error screen.
            An exception will be raise instead (default=True)

        """

        Input.__init__(self)
        if not isinstance(_pyxid, ModuleType):
            message = """CedrusDevice can not be initialized, because the Python package
            'pyxid' is not installed. See Expyriment online documentation."""
            raise ImportError(message)

        while True:
            devices = _pyxid.get_xid_devices()
            if len(devices) < 1:
                message = "Could not find a Cedrus Device. Please check the connection and \n"\
                + " ensure that the device is switch on."
            else:
                if not devices[device_ID].is_response_device():
                    message = "Cedrus Device #{0} is not a response device.".format(
                                                                    device_ID)
                else:
                    self._xid = devices[device_ID]
                    break
            if error_screen and _internals.active_exp.is_initialized:
                stimuli.TextScreen("Error", message +
                        " Press a key to reconnect to the device.").present()
                _internals.active_exp.keyboard.wait()
                stimuli.BlankScreen().present()
                _internals.active_exp.clock.wait(300)
            else:
                raise IOError(message)

        self._xid.reset_base_timer()
        self._xid.reset_rt_timer()
        self._device_ID = device_ID
        self._buffer = misc.Buffer(name="Cedrus Device {0}".format(
                                                        device_ID))


    def __str__(self):
        return self._xid.__str__()

    @property
    def id(self):
        """Getter for XID device id."""
        return self._device_ID

    @property
    def buffer(self):
        """Getter for buffer."""
        return self._buffer

    @property
    def xid_interface(self):
        """Getter for xid device interface."""
        return self._xid

    def poll_responses(self):
        """Poll the Cedrus response device and copies the available response
        in the buffer.

        Notes
        -----
        Release key events get a code larger 999 (1000 + key code).

        Returns
        -------
        out : bool
            True is a new response was available.

        """

        self._xid.poll_for_response()
        new_event = False

        # copy xid cue to _buffer and poll
        while self._xid.response_queue_size() > 0:
            new_event = True
            response = self._xid.get_next_response()
            if response['pressed'] == False:
                response['key'] = 1000 + response['key']
            self._buffer.add_event(response['key'])
            if self._logging:
                _internals.active_exp._event_file_log(
                        "CedrusResponseDevice {0},received,{1},poll".format(
                        self._device_ID, response['key']), 2)
            self._xid.poll_for_response()

        return new_event

    def clear(self):
        """Clear device and all events in the response cues."""

        self._xid.poll_for_response()
        while self._xid.response_queue_size() > 0:
            self._xid.clear_response_queue()
            self._xid.poll_for_response()
        self._buffer.clear()
        if self._logging:
            _internals.active_exp._event_file_log(
                                        "CedrusResponseDevice,cleared", 2)

    def check(self, codes=None):
        """Check for a specific response code occurred since last clear().

        The function polls the device and returns the first event
        found in the buffer (i.e., since last clear) or None.

        Parameters
        ----------
        codes : int or list, optional
            key codes to check for

        Returns
        -------
        key : int
            code of pressed key
        rt : int
            reaction time in ms

        """

        self.poll_responses()
        if self._buffer.get_size() > 0:
            if codes is None:
                return self._buffer.memory[0]
            else:
                if not isinstance(codes, (tuple, list)):
                    codes = [codes]
                for elem in self._buffer.memory:
                    if elem[0] in codes:
                        return elem
                return None
        return None

    def wait(self, codes=None, duration=None, no_clear_buffer=False,
             callback_function=None, process_control_events=True):
        """Wait for responses defined as codes.

        The functions returns the found key code and the reaction time, that
        is, the time relative to the called of wait. By default the buffer
        will be cleared() before waiting.

        Parameters
        ----------
        codes : int or list, optional
            codes to wait for
        duration : int, optional
            maximal time to wait in ms
        no_clear_buffer : bool, optional
            do not clear the buffer.  In this case RT could be negative,
            if the event is already in the buffer (default = False)
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = True)

        Returns
        -------
        key : int
            code of pressed key
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
        start = self._buffer.clock.time
        if not no_clear_buffer:
            self.clear()
        while True:
            if isinstance(callback_function, FunctionType):
                callback_function()
            if _internals.active_exp is not None and \
               _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                    return rtn_callback
                if process_control_events:
                    if _internals.active_exp.mouse.process_quit_event() or \
                       _internals.active_exp.keyboard.process_control_keys():
                        break
                else:
                    _internals.pump_pygame_events()
            if duration is not None:
                if int(self._buffer.clock.time - start) > duration:
                    return (None, None)
            found = self.check(codes)
            if found is not None:
                found = (found[0], found[1] - start)
                break

        if self._logging:
            _internals.active_exp._event_file_log(
                "CedrusResponseDevice,received,{0},wait".format(found))

        return found

    if isinstance(_pyxid, ModuleType):
        @staticmethod
        def _self_test(experiment):
            result = {}
            result['CedrusResponseDevice'] = ""  # TODO: Implement test!
            return result
