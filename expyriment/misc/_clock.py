"""The expyriment clock.

This module contains an experimental clock.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import sys
import time
import types
from ._timer import get_time
from .._expyriment_types import CallbackQuitEvent
from .. import _active

class Clock(object) :
    """Basic timing class.

    Unit of time is milliseconds.

    """

    if sys.platform == 'win32':
        _cpu_time = time.clock
    else:
        _cpu_time = time.time



    def __init__(self, sync_clock=None):
        """Create a clock.

        Parameters
        ----------
        sync_clock : misc.Clock, optional
            synchronise clock with existing one

        """

        from ..io.defaults import _skip_wait_functions
        if (sync_clock.__class__.__name__ == "Clock"):
            self.__init_time = sync_clock.init_time // 1000
        else:
            self.__init_time = get_time()

        self._init_localtime = time.localtime()
        self.__start = get_time()

        self._skip_wait_functions = _skip_wait_functions


    @staticmethod
    def monotonic_time():
        """Returns the time of the high-resolution monitonoic timer that is
        used by Expyriment interally.

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
        """Getter for CPU time."""

        return self._cpu_time()

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

    def wait(self, waiting_time, function=None):
        """Wait for a certain amout of milliseconds.

        Parameters
        ----------
        waiting_time : int
            time to wait in milliseconds
        function : function, optional
            function to repeatedly execute during waiting loop

        Returns
        -------
        quit_event : expyriment.control.CallbackQuitEvent object
           the callback quit even in case a wait function has been registered
            
        See Also
        --------
        design.experiment.register_wait_callback_function

        """

        if self._skip_wait_functions:
            return
        start = self.time
        if type(function) == types.FunctionType or\
                                 _active.exp.is_callback_registered:
            while (self.time < start + waiting_time):
                if type(function) == types.FunctionType:
                    function()
                rtn_callback = _active.exp._execute_wait_callback()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    return rtn_callback
        else:
            looptime = 200
            if (waiting_time > looptime):
                time.sleep((waiting_time - looptime) // 1000)
            while (self.time < start + waiting_time):
                pass

    def wait_seconds(self, time_sec, function=None):
        """Wait for a certain amout of seconds.

        Parameters
        ----------
        time_sec : int
            time to wait in seconds
        function : function, optional
            function to repeatedly execute during waiting loop

        Returns
        -------
        quit_event : expyriment.control.CallbackQuitEvent object
           the callback quit even in case a wait function has been registered
        
        See Also
        --------
        Clock.wait, design.experiment.register_wait_callback_function

        """

        return self.wait(time_sec * 1000, function)

    def wait_minutes(self, time_minutes, function=None):
        """Wait for a certain amount of minutes.

        Parameters
        ----------
        time_minutes : int
            time to wait in minutes
        function : function, optional
            function to repeatedly execute during waiting loop

        Returns
        -------
        quit_event : expyriment.control.CallbackQuitEvent object
           the callback quit even in case a wait function has been registered
            
        See Also
        --------
        Clock.wait, design.experiment.register_wait_callback_function

        """

        return self.wait_seconds(time_minutes * 60, function)
