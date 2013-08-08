"""
Keyboard input.

This module contains a class implementing pygame keyboard input.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import time, sys

import pygame
try:
    import android
except ImportError:
    android = None

import defaults
import expyriment
from expyriment.misc import Clock

from  _input_output import Input


quit_key = None
pause_key = None
end_function = None
pause_function = None

class Keyboard(Input):
    """A class implementing a keyboard input.

    Calling `expyriment.control.intialize(exp)` will automatically create a
    keyboard instance and will reference it in exp.keyboard for easy access.

    """

    @staticmethod
    def process_control_keys(key_event=None):
        """Check if quit_key or pause_key has been pressed.

        Reads pygame event cue if no key_event is specified.

        Parameters
        ----------
        key_event : int, optional
            key event to check

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
                    confirm = end_function(confirmation=True)
                    if confirm:
                        sys.exit()
                    return True
                elif key_event.key == pause_key and \
                        pause_function is not None:
                    pause_function()
                    return True
        else:
            for event in pygame.event.get(pygame.KEYDOWN):
                return Keyboard.process_control_keys(event) # recursive
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


    def clear(self):
        """Clear the event queue from keyboard events."""

        pygame.event.clear(pygame.KEYDOWN)
        pygame.event.clear(pygame.KEYUP)

        if self._logging:
            expyriment._active_exp._event_file_log("Keyboard,cleared", 2)

    def read_out_buffered_keys(self):
        """Reads out all keydown events and clears queue."""

        pygame.event.pump()
        pygame.event.clear(pygame.KEYUP)
        rtn = []
        for event in pygame.event.get(pygame.KEYDOWN):
            Keyboard.process_control_keys(event)
            rtn.append(event.key)
        return rtn


    def check(self, keys=None, check_for_control_keys=True):
        """Check if keypress is in event queue.

        Parameters
        ----------
        default_keys : int or list, optional
            a specific key or list of keys to check
        check_for_control_keys : bool, optional
            checks if control key has been pressed (default=True)

        Returns
        -------
        key : int
            pressed key or None. Only the first occurence is returned!

        """

        if keys is None:
            keys = self.default_keys
        if type(keys) is not list and keys is not None:
            keys = [keys]
        pygame.event.pump()
        pygame.event.clear(pygame.KEYUP)
        for event in pygame.event.get(pygame.KEYDOWN):
            if check_for_control_keys:
                Keyboard.process_control_keys(event)
            if keys:
                if event.key in keys:
                    if self._logging:
                        expyriment._active_exp._event_file_log(
                            "Keyboard,received,{0},check".format(event.key))
                    return event.key
            else:
                if self._logging:
                    expyriment._active_exp._event_file_log(
                        "Keyboard,received,{0},check".format(event.key), 2)
                return event.key
        return None

    def wait(self, keys=None, duration=None, wait_for_keyup=False,
             check_for_control_keys=True):
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
            if True it waits for key-up
        check_for_control_keys : bool, optional
            checks if control key has been pressed (default=True)

        """

        if android is not None:
            android.show_keyboard()
        start = Clock._cpu_time()
        rt = None
        found_key = None
        self.clear()
        if keys is None:
            keys = self.default_keys
        if keys is not None and type(keys) is not list:
            keys = [keys]
        if wait_for_keyup:
            target_event = pygame.KEYUP
        else:
            target_event = pygame.KEYDOWN
        pygame.event.pump()
        done = False
        while not done:
            expyriment._active_exp._execute_wait_callback()
            for event in pygame.event.get():
                if check_for_control_keys and Keyboard.process_control_keys(event):
                    done = True
                elif event.type == target_event:
                    if keys is not None:
                        if event.key in keys:
                            rt = int((Clock._cpu_time() - start) * 1000)
                            found_key = event.key
                            done = True
                    else:
                        rt = int((Clock._cpu_time() - start) * 1000)
                        found_key = event.key
                        done = True
            if duration and not done:
                done = int((Clock._cpu_time() - start) * 1000) >= duration
            time.sleep(0.0005)
        if self._logging:
            expyriment._active_exp._event_file_log("Keyboard,received,{0},wait"\
                                              .format(found_key))
        if android is not None:
            android.hide_keyboard()
        return found_key, rt

    def wait_char(self, char, duration=None, check_for_control_keys=True):
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
        check_for_control_keys : bool, optional
            checks if control key has been pressed (default=True)

        Returns
        -------
        found : char
            pressed charater
        rt : int
            reaction time in ms

        """

        start = Clock._cpu_time()
        rt = None
        found_char = None
        self.clear()
        if type(char) is not list:
            char = [char]
        pygame.event.pump()
        done = False
        while not done:
            expyriment._active_exp._execute_wait_callback()
            for event in pygame.event.get():
                if check_for_control_keys and Keyboard.process_control_keys(event):
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.unicode in char:
                        rt = int((Clock._cpu_time() - start) * 1000)
                        found_char = event.unicode
                        done = True
            if duration and not done:
                done = int((Clock._cpu_time() - start) * 1000) >= duration
            time.sleep(0.0005)
        if self._logging:
            expyriment._active_exp._event_file_log(
                        "Keyboard,received,{0},wait_char".format(found_char))
        return found_char, rt
