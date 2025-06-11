"""
A streaming button box.

This module contains a class implementing a streaming button box.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from types import FunctionType

import pygame

from .. import _internals
from .._internals import CallbackQuitEvent
from ..misc import compare_codes
from ..misc._timer import get_time
from . import defaults
from ._input_output import Input, Output


class StreamingButtonBox(Input, Output):
    """A class implementing a streaming button box input."""

    def __init__(self, interface, baseline):
        """Create a streaming button box input.

        Parameters
        ----------
        interface : ``expyriment.io.SerialPort`` or ``expyriment.io.ParallelPort``
            the interface to use
        baseline : int
            code that is sent when nothing is pressed (int)

        """

        Input.__init__(self)
        Output.__init__(self)
        self._interface = interface
        if baseline is not None:
            self._baseline = baseline
        else:
            self._baseline = defaults.streamingbuttonbox_baseline

    @property
    def interface(self):
        """Getter for interface."""
        return self._interface

    @property
    def baseline(self):
        """Getter for baseline."""
        return self._baseline

    @baseline.setter
    def baseline(self, value):
        """Setter for baseline"""
        self._baseline = value

    def clear(self):
        """Clear the receive buffer (if available)."""

        self._interface.clear()
        if self._logging:
            _internals.active_exp._event_file_log("{0},cleared".format(
            self.__class__.__name__), 2)

    def check(self, codes=None, bitwise_comparison=False):
        """Check for response codes.

        If bitwise_comparison = True, the function performs a bitwise
        comparison (logical and) between codes and received input.

        Parameters
        ----------
        codes : int or list, optional
            certain bit pattern or list of bit pattern to wait for,
            if codes is not set (None) the function returns
            for any event that differs from the baseline
        bitwise_comparison : bool, optional
            make a bitwise comparison (default=False)

        Returns
        -------
        key : int
            key code or None

        """

        while True:
            read = self._interface.poll()
            if read is not None:
                if codes is None and read != self._baseline:
                    if self._logging:
                        _internals.active_exp._event_file_log(
                        "{0},received,{1},check".format(
                            self.__class__.__name__,
                            read), 2)
                    return read
                elif compare_codes(read, codes, bitwise_comparison):
                    if self._logging:
                        _internals.active_exp._event_file_log(
                        "{0},received,{1},check".format(
                            self.__class__.__name__,
                            read))
                    return read
            else:
                return None

    def wait(self, codes=None, duration=None, no_clear_buffer=False,
             bitwise_comparison=False, callback_function=None,
             process_control_events=True, low_performance=False):
        """Wait for responses defined as codes.

        If bitwise_comparison = True, the function performs a bitwise
        comparison (logical and) between codes and received input and waits
        until a certain bit pattern is set.

        Parameters
        ----------
        codes : int or list, optional
            bit pattern to wait for
            if codes is not set (None) the function returns for any
            event that differs from the baseline
        duration : int, optional
            maximal time to wait in ms
        no_clear_buffer : bool, optional
            do not clear the buffer (default = False)
        bitwise_comparison : bool, optional
            make a bitwise comparison (default = False)
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = True)
        low_performance : bool, optional
            reduce CPU performance (and allow potential threads to run) while
            waiting at the cost of less timing accuracy (default = False)

        Returns
        -------
        key : int
            key code (or None) that quit waiting
        rt : int
            reaction time

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
        rt = None
        if not no_clear_buffer:
            self.clear()
        while True:
            if isinstance(callback_function, FunctionType):
                rtn_callback = callback_function()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    found = rtn_callback
                    rt = int((get_time() - start) * 1000)
                    break
            if _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    found = rtn_callback
                    rt = int((get_time() - start) * 1000)
                    break
                if process_control_events:
                    if _internals.active_exp.mouse.process_quit_event() or \
                       _internals.active_exp.keyboard.process_control_keys():
                        break
                else:
                    pygame.event.pump()
            if duration is not None:
                if int((get_time() - start) * 1000) > duration:
                    return None, None
            found = self.check(codes, bitwise_comparison)
            if found is not None:
                rt = int((get_time() - start) * 1000)
                break
            if low_performance:
                _internals.low_performance_sleep()

        if self._logging:
            _internals.active_exp._event_file_log(
                                "{0},received,{1},wait".format(
                                                self.__class__.__name__,
                                                found))
        return found, rt
