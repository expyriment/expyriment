"""
A Trigger input

This module contains a class implementing a trigger input.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from types import FunctionType

from . import defaults
from .. import _internals
from ..misc import compare_codes
from .._internals import CallbackQuitEvent
from ..misc._timer import get_time
from ._keyboard import Keyboard
from  ._input_output import Input


class TriggerInput(Input):
    """A class implementing a trigger input."""

    def __init__(self, interface, default_code=None):
        """Create a trigger input.

        Parameters
        ----------
        interface : ``expyriment.io.SerialPort`` or ``expyriment.io.ParallelPort``
            the interface to use
        default_code : int, optional
            the default code of the trigger

        """

        Input.__init__(self)
        self._interface = interface
        if default_code is not None:
            self._default_code = default_code
        else:
            self._default_code = defaults.triggerinput_default_code

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

    def wait(self, code=None, bitwise_comparison=False, callback_function=None,
             process_control_events=True):
        """Wait for a trigger.

        Returns the code received and the reaction time [code, rt].

        If bitwise_comparison = True, the function performs a bitwise
        comparison (logical and) between code and received input and waits
        until a certain bit pattern is set.

        Parameters
        ----------
        code : int, optional
            a specific code to wait for
        bitwise_comparison : bool, optional
            make a bitwise comparison (default = False)
        function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = True)

        Notes
        -----
        This will also by default process control events (quit and pause).
        Thus, keyboard events will be cleared from the cue and cannot be
        received by a Keyboard().check() anymore!

        See Also
        --------
        expyriment.design.Experiment.register_wait_callback_function

       """

        if _internals.skip_wait_methods:
            return None, None
        start = get_time()
        found = None
        rt = None
        if code is None:
            code = self._default_code
        self.interface.clear()
        while True:
            if isinstance(callback_function, FunctionType):
                callback_function()
            if _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    return rtn_callback, int((get_time() - start) * 1000)
                if process_control_events:
                    if _internals.active_exp.mouse.process_quit_event() or \
                       _internals.active_exp.keyboard.process_control_keys():
                        break
                else:
                    _internals.pump_pygame_events()
            read = self.interface.poll()
            if read is not None:
                if code is None: #return for every event
                    rt = int((get_time() - start) * 1000)
                    found = read
                    break
                elif compare_codes(read, code, bitwise_comparison):
                    rt = int((get_time() - start) * 1000)
                    found = read
                    break
            if Keyboard.process_control_keys():
                    break
        if self._logging:
            _internals.active_exp._event_file_log(
                            "TriggerInput,received,{0},wait".format(found))
        return found, rt

    def get_triggers(self, code=None, bitwise_comparison=False):
        """Get list of received triggers.

        For not missing any triggers the history has to be updated regularly
        (e.g. by calling this method)!
        Returns None if no history is used.

        If bitwise_comparision = True, the function performs a bitwise
        comparison (logical and) between code and received input and waits
        until a certain bit pattern is set.

        Parameters
        ----------
        code : int, optional
            a specific code to get
        bitwise_comparison : bool, optional
            make a bitwise comparison (default = False)

        """

        if self.interface.has_input_history:
            self.interface.clear()
            counter_list = []
            if code is None:
                code = self._default_code
            for event in self.interface.input_history.get_whole_buffer():
                if code is None: #get them all
                    counter_list.append(event)
                elif compare_codes(event, code, bitwise_comparison):
                    counter_list.append(event)
            return counter_list
        else:
            return None

    @property
    def trigger_count(self, code=None, bitwise_comparison=False):
        """Get the number of received triggers.

        For not missing any triggers the history has to be updated regularly
        (e.g. by calling this method)!
        Returns None if no history is used.

        If bitwise_comparision = True, the function performs a bitwise
        comparison (logical and) between code and received input and waits
        until a certain bit pattern is set.

        Parameters
        ----------
        code : int, optional
            a specific code to count
        bitwise_comparison : bool, optional
            make a bitwise comparison (default = False)

        """

        if self.interface.has_input_history:
            self.interface.clear()
            counter = 0
            if code is None:
                code = self._default_code
            for event in self.interface.input_history.get_whole_buffer():
                if code is None: #count all
                    counter += 1
                elif compare_codes(event, code, bitwise_comparison):
                    counter += 1
            return counter
        else:
            return None
