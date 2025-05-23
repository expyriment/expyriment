"""
Keyboard input.

This module contains a class implementing pygame keyboard input.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


import time, sys
from types import FunctionType

import pygame

try:
    import android.show_keyboard as android_show_keyboard
    import android.hide_keyboard as android_hide_keyboard
except ImportError:
    android_show_keyboard = android_hide_keyboard = None

from . import defaults

from ..misc._timer import get_time
from ..misc import unicode2byte
from  ._input_output import Input
from .. import  _internals

quit_key = None
end_function = None

class Keyboard(Input):
    """A class implementing a keyboard input.

    Calling `expyriment.control.initialize(exp)` will automatically create a
    keyboard instance and will reference it in exp.keyboard for easy access.

    """

    @staticmethod
    def process_control_keys(key_event=None, event_detected_function=None,
                             quit_confirmed_function=None,
                             quit_denied_function=None):
        """Check if quit_key has been pressed.

        Reads pygame event cue if no key_event is specified.

        Parameters
        ----------
        key_event : int, optional
            key event to check. If not defined, the Pygame event queue will be
            checked for key down events.
        event_detected_function : function, optional
            function to be called when key event is detected.
        quit_confirmed_function : function, optional
            function to be called if quitting has been confirmed.
        quit_denied_function : function, optional
            function to be called if quitting has been denied.

        Returns
        -------
        out : bool
            True if quitting or pause screen has been displayed,
            False otherwise

        """

        if key_event:
            if key_event.type == pygame.KEYDOWN:
                if key_event.key == quit_key and \
                   end_function is not None:
                    if event_detected_function is not None:
                        event_detected_function()
                    confirm = end_function(
                        confirmation=True,
                        pre_quit_function=quit_confirmed_function)
                    if confirm:
                        sys.exit()
                    else:
                        if quit_denied_function is not None:
                            quit_denied_function()
                    return True
        else:
            # Clear keyup events to prevent limit on unicode field storage:
            # https://github.com/pygame/pygame/issues/3229
            pygame.event.get(pygame.KEYUP)

            # process all key-down events
            for event in pygame.event.get(pygame.KEYDOWN):
                if Keyboard.process_control_keys(event,
                                                 event_detected_function,
                                                 quit_confirmed_function,
                                                 quit_denied_function):
                    return True
            return False

        return False


    def __init__(self, default_keys=None):
        """Create a keyboard input.

        Parameters
        ----------
        default_keys : int or list, optional
            a default key or list of default keys

        """

        if default_keys is not None:
            self._default_keys = default_keys
        else:
            self._default_keys = defaults.keyboard_default_keys
        Input.__init__(self)

    @property
    def default_keys(self):
        """Getter for default keys"""

        return self._default_keys

    @default_keys.setter
    def default_keys(self, value):
        """Setter for default keys"""

        self._default_keys = value

    @staticmethod
    def get_quit_key():
        """Returns the currently defined quit key """

        return quit_key


    @staticmethod
    def set_quit_key(value):
        """Set the currently defined quit key"""

        global quit_key
        quit_key = value

    def clear(self):
        """Clear the event queue from keyboard events."""

        pygame.event.clear(pygame.KEYDOWN)
        pygame.event.clear(pygame.KEYUP)

        if self._logging:
            _internals.active_exp._event_file_log("Keyboard,cleared", 2)

    def read_out_buffered_keys(self):
        """Reads out all keydown events and clears queue."""

        pygame.event.pump()
        pygame.event.clear(pygame.KEYUP)
        rtn = []
        for event in pygame.event.get(pygame.KEYDOWN):
            Keyboard.process_control_keys(event)
            rtn.append(event.key)
        return rtn

    def check(self, keys=None, check_for_keyup=False,
              check_for_control_keys=True):
        """Check if keypress is in event queue.

        Parameters
        ----------
        keys : int or list, optional
            a specific key or list of keys to check
        check_for_keyup : bool, optional
            if True checks for key-up (default = False)
        check_for_control_keys : bool, optional
            checks if control key has been pressed (default = True)

        Returns
        -------
        key : int
            pressed key or None. Only the first occurrence is returned!

        Notes
        -----
        Keys are defined by keyboard constants (please see misc.constants).

        When checking for key-down (default), all key-up events are first
        cleared, and when checking for key-up events, all key-down events are
        first cleared!

        Unlike the wait method, events are only logged on loglevel 2 when no
        keys are specified. this is to prevent excesive default logging when
        used repeatedly in a loop.

        """

        # TODO for 1.0: Check should not return None. Think about the
        #               introduction of QuitAttemptEvent!

        if keys is None:
            keys = self.default_keys
        else:
            try:
                keys = list(keys)
            except Exception:
                keys = [keys]

        pygame.event.pump()

        if check_for_keyup:
            target_event = pygame.KEYUP
            if check_for_control_keys:
                self.check(keys=None, check_for_keyup=False,
                           check_for_control_keys=True)
                check_for_control_keys = False
        else:
            target_event = pygame.KEYDOWN
            pygame.event.clear(pygame.KEYUP)

        for event in pygame.event.get(target_event):
            if check_for_control_keys:
                Keyboard.process_control_keys(event)
            if keys:
                if event.key in keys:
                    if self._logging:
                        _internals.active_exp._event_file_log(
                            "Keyboard,received,{0},check".format(event.key))
                    return event.key
            else:
                if self._logging:
                    _internals.active_exp._event_file_log(
                        "Keyboard,received,{0},check".format(event.key), 2)
                return event.key
        return None

    def wait(self, keys=None, duration=None, wait_for_keyup=False,
             callback_function=None, process_control_events=True,
             low_performance=False):
        """Wait for keypress(es) (optionally for a certain amount of time).

        This function will wait for a keypress and returns the found key as
        well as the reaction time.
        (This function clears the event queue!)

        Parameters
        ----------
        keys : int or list, optional
            a specific key or list of keys to wait for
        duration : int, optional
            maximal time to wait in ms
        wait_for_keyup : bool, optional
            if True it waits for key-up (default=False)
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = True)
        low_performance : bool, optional
            reduce CPU performance while waiting at the cost of less timing
            accuracy (default = False)

        Returns
        -------
        found : char
            pressed character
        rt : int
            reaction time in ms

        Notes
        -----
        Keys are defined by keyboard constants (please see misc.constants).

        See Also
        --------
        expyriment.design.Experiment.register_wait_callback_function

        """

        if _internals.skip_wait_methods:
            return None, None
        if android_show_keyboard is not None:
            android_show_keyboard()
        start = get_time()
        rt = None
        found_key = None
        self.clear()
        if keys is None:
            keys = self.default_keys
        else:
            try:
                keys = list(keys)
            except Exception:
                keys = [keys]
        if wait_for_keyup:
            target_event = pygame.KEYUP
        else:
            target_event = pygame.KEYDOWN
        pygame.event.pump()
        done = False
        while not done:
            if isinstance(callback_function, FunctionType):
                rtn_callback = callback_function()
                if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                    done = True
                    found_key = rtn_callback
                    rt = int((get_time() - start) * 1000)
            if _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                    done = True
                    found_key = rtn_callback
                    rt = int((get_time() - start) * 1000)
                if process_control_events and \
                    _internals.active_exp.mouse.process_quit_event():
                    done = True
            for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
                if _internals.active_exp.is_initialized and \
                   process_control_events and \
                   Keyboard.process_control_keys(event):
                    done = True
                elif event.type == target_event:
                    if keys is not None:
                        if event.key in keys:
                            rt = int((get_time() - start) * 1000)
                            found_key = event.key
                            done = True
                    else:
                        rt = int((get_time() - start) * 1000)
                        found_key = event.key
                        done = True
            if duration and not done:
                done = int((get_time() - start) * 1000) >= duration
            if not done and low_performance:
                time.sleep(0.0005)
        if self._logging:
            _internals.active_exp._event_file_log("Keyboard,received,{0},wait"\
                                              .format(found_key))
        if android_hide_keyboard is not None:
            android_hide_keyboard()
        return found_key, rt

    def wait_char(self, char, duration=None, callback_function=None,
                  process_control_events=True, low_performance=False):
        """Wait for character(s) (optionally for a certain amount of time).

        This function will wait for one or more characters and returns the
        found character as well as the reaction time.
        (This function clears the event queue!)

        Parameters
        ----------
        char : int or list
            a specific character or list of characters to wait for
        duration : int, optional
            maximal time to wait in ms
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = True)
        low_performance : bool, optional
            reduce CPU performance while waiting at the cost of less timing
            accuracy (default = False)

        Returns
        -------
        found : char
            pressed character
        rt : int
            reaction time in ms

        See Also
        --------
        expyriment.design.Experiment.register_wait_callback_function

        """

        if _internals.skip_wait_methods:
            return None, None
        start = get_time()
        rt = None
        found_char = None
        self.clear()
        try:
            char = list(char)
        except Exception:
            char = [char]
        pygame.event.pump()
        done = False

        while not done:
            if isinstance(callback_function, FunctionType):
                rtn_callback = callback_function()
                if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                    done = True
                    rt = int((get_time() - start) * 1000)
                    found_char = rtn_callback
            if _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                    done = True
                    rt = int((get_time() - start) * 1000)
                    found_char = rtn_callback
                if process_control_events and  \
                        _internals.active_exp.mouse.process_quit_event():
                    done = True
            for event in pygame.event.get([pygame.KEYUP, pygame.KEYDOWN]):
                if _internals.active_exp.is_initialized and \
                   process_control_events and \
                   Keyboard.process_control_keys(event):
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.unicode in char:
                        rt = int((get_time() - start) * 1000)
                        found_char = event.unicode
                        done = True
            if duration and not done:
                done = int((get_time() - start) * 1000) >= duration
            if not done and low_performance:
                time.sleep(0.0005)
        if self._logging:
            if found_char is not None:
                _internals.active_exp._event_file_log(
                    u"Keyboard,received,{0},wait_char".format(
                        found_char))
            else:
                _internals.active_exp._event_file_log(
                    "Keyboard,received,None,wait_char")
        return found_char, rt
