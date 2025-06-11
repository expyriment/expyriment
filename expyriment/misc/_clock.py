"""The expyriment clock.

This module contains an experimental clock.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'



import time
from types import FunctionType

import pygame

from .. import _internals
from ._timer import get_time


class Clock :
    """Basic timing class.

    Unit of time is milliseconds.

    """


    def __init__(self, sync_clock=None):
        """Create a clock.

        Parameters
        ----------
        sync_clock : misc.Clock, optional
            synchronise clock with existing one

        """

        if (sync_clock.__class__.__name__ == "Clock"):
            self.__init_time = sync_clock.init_time / 1000
        else:
            self.__init_time = get_time()

        self._init_localtime = time.localtime()
        self.__start = get_time()


    @staticmethod
    def monotonic_time():
        """Returns the time of the high-resolution monotonic timer that is
        used by Expyriment internally.

        """
        return get_time()

    @property
    def init_time(self):
        """Getter for init time in milliseconds."""

        return self.__init_time * 1000

    @property
    def time(self):
        """Getter for current time in milliseconds since clock init."""

        return int((get_time() - self.__init_time) * 1000)

    @property
    def cpu_time(self):
        """OBSOLETE property: Please use monotonic_time()."""
        # TODO: make deprecated with 1.0

        return get_time()

    @property
    def stopwatch_time(self):
        """Getter for time in milliseconds since last reset_stopwatch.

        The use of the stopwatch does not affect the clock time.
        """

        return int((get_time() - self.__start) * 1000)

    @property
    def init_localtime(self):
        """Getter for init time in local time"""

        return self._init_localtime

    def reset_stopwatch(self):
        """"Reset the stopwatch.

        The use of the stopwatch does not affect the clock time.
        """

        self.__start = get_time()

    def wait(self, waiting_time, callback_function=None,
             process_control_events=False, low_performance=False):
        """Wait for a certain amount of milliseconds.

        Parameters
        ----------
        waiting_time : int
            time to wait in milliseconds
        function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = False)
        low_performance : bool, optional
            reduce CPU performance (and allow potential threads to run) while
            waiting at the cost of less timing accuracy (default = False)

        Returns
        -------
        quit_event : expyriment.control.CallbackQuitEvent object
           the callback quit even in case a wait function has been registered

        See Also
        --------
        expyriment.design.Experiment.register_wait_callback_function

        """

        if _internals.skip_wait_methods:
            return None
        start = self.time
        if low_performance or isinstance(callback_function, FunctionType) or \
           (process_control_events or \
             _internals.active_exp.is_callback_registered):
            while (self.time < start + waiting_time):
                if isinstance(callback_function, FunctionType):
                    rtn_callback = callback_function()
                    if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                        return rtn_callback
                if _internals.active_exp.is_initialized:
                    rtn_callback = _internals.active_exp._execute_wait_callback()
                    if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                        return rtn_callback
                    if process_control_events:
                        if _internals.active_exp.keyboard.process_control_keys():
                            break
                        _internals.active_exp.mouse.process_quit_event()
                    else:
                        pygame.event.pump()
                if low_performance:
                    _internals.low_performance_sleep()

        else:
            looptime = 200
            if (waiting_time > looptime):
                if _internals.active_exp.is_initialized:
                    while (self.time < start + (waiting_time - looptime)):
                        if process_control_events:
                            if _internals.active_exp.mouse.process_quit_event() or \
                               _internals.active_exp.keyboard.process_control_keys():
                                break
                        else:
                            pygame.event.pump()
                else:
                    time.sleep((waiting_time - looptime) // 1000)
            while (self.time < start + waiting_time):
                pass

    def wait_seconds(self, time_sec, callback_function=None,
                     process_control_events=False, low_performance=False):
        """Wait for a certain amount of seconds.

        Parameters
        ----------
        time_sec : int
            time to wait in seconds
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = False)
        low_performance : bool, optional
            reduce CPU performance (and allow potential threads to run) while
            waiting at the cost of less timing accuracy (default = False)

        Returns
        -------
        quit_event : expyriment.control.CallbackQuitEvent object
           the callback quit even in case a wait function has been registered

        See Also
        --------
        wait
        expyriment.design.Experiment.register_wait_callback_function

        """

        return self.wait(time_sec * 1000, callback_function,
                         process_control_events, low_performance)

    def wait_minutes(self, time_minutes, callback_function=None,
                     process_control_events=False, low_performance=False):
        """Wait for a certain amount of minutes.

        Parameters
        ----------
        time_minutes : int
            time to wait in minutes
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = False)
        low_performance : bool, optional
            reduce CPU performance (and allow potential threads to run) while
            waiting at the cost of less timing accuracy (default = False)

        Returns
        -------
        quit_event : expyriment.control.CallbackQuitEvent object
           the callback quit even in case a wait function has been registered

        See Also
        --------
        wait
        expyriment.design.Experiment.register_wait_callback_function

        """

        return self.wait_seconds(time_minutes * 60, callback_function,
                                 process_control_events, low_performance)
