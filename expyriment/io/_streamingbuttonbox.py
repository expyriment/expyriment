"""
A streaming button box.

This module contains a class implementing a streaming button box.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import defaults
import expyriment
from expyriment.misc import compare_codes
from expyriment.misc._timer import get_time
from _keyboard import Keyboard
from _input_output import Input, Output


class StreamingButtonBox(Input, Output):
    """A class implementing a streaming button box input."""

    def __init__(self, interface, baseline):
        """Create a streaming button box input.

        Parameters
        ----------
        interface : io.SerialPort or io.ParallelPort
            an interface object
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
            expyriment._active_exp._event_file_log("{0},cleared".format(
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
                        expyriment._active_exp._event_file_log(
                        "{0},received,{1},check".format(
                            self.__class__.__name__,
                            read), 2)
                    return read
                elif compare_codes(read, codes, bitwise_comparison):
                    if self._logging:
                        expyriment._active_exp._event_file_log(
                        "{0},received,{1},check".format(
                            self.__class__.__name__,
                            read))
                    return read
            else:
                return None

    def wait(self, codes=None, duration=None, no_clear_buffer=False,
             bitwise_comparison=False, check_for_control_keys=True):
        """Wait for responses defined as codes.

        Notes
        -----
        If bitwise_comparision = True, the function performs a bitwise
        comparison (logical and) between codes and received input and waits
        until a certain bit pattern is set.

        This will also by default check for control keys (quit and pause).
        Thus, keyboard events will be cleared from the cue and cannot be
        received by a Keyboard().check() anymore!

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
        check_for_control_keys : bool, optional
            checks if control key has been pressed (default=True)

        Returns
        -------
        key : int
            key code (or None) that quitted waiting
        rt : int
            reaction time

        See Also
        --------
        design.experiment.register_wait_callback_function

        """

        if expyriment.control.defaults._skip_wait_functions:
            return None, None
        start = get_time()
        rt = None
        if not no_clear_buffer:
            self.clear()
        while True:
            rtn_callback = expyriment._active_exp._execute_wait_callback()
            if isinstance(rtn_callback, expyriment.control.CallbackQuitEvent):
                found = rtn_callback
                rt = int((get_time() - start) * 1000)
                break
            if duration is not None:
                if int((get_time() - start) * 1000) > duration:
                    return None, None
            found = self.check(codes, bitwise_comparison)
            if found is not None:
                rt = int((get_time() - start) * 1000)
                break
            if check_for_control_keys:
                if Keyboard.process_control_keys():
                    break
        if self._logging:
            expyriment._active_exp._event_file_log(
                                "{0},received,{1},wait".format(
                                                self.__class__.__name__,
                                                found))
        return found, rt
