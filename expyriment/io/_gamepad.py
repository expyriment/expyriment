"""A gamepad.

This module contains a class implementing a pygame gamepad.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import time
from types import FunctionType

import pygame

from .. import _internals
from ..misc._timer import get_time
from ._keyboard import Keyboard
from  ._input_output import Input, Output


pygame.joystick.init()


class GamePad(Input, Output):
    """A class for creating gamepad/joystick input."""

    @staticmethod
    def get_gampad_count():
        """Get the number of gamepads/joysticks connected to the system."""

        return pygame.joystick.get_count()

    def __init__(self, gamepad_id, track_button_events=True,
                 track_motion_events=False):
        """Create a gamepad/joystick input.

        Parameters
        ----------
        gamepad_id : int
            id of the gamepad
        track_button_events : bool, optional
            Track button events (default=True)
        track_motion_events : bool, optional
            Track motion events (default=False)

        """

        if not _internals.active_exp.is_initialized:
            raise RuntimeError(
                "Cannot create GamePad before expyriment.initialize()!")
        Input.__init__(self)
        Output.__init__(self)
        self.track_button_events = track_button_events
        self.track_motion_events = track_motion_events
        self._joystick = pygame.joystick.Joystick(gamepad_id)
        self._joystick.init()

    @property
    def track_button_events(self):
        """Getter for track_button_events."""

        return self._track_button_events

    @track_button_events.setter
    def track_button_events(self, value):
        """Setter for track_button_events.

        Switch on/off the processing of button events.

        """

        self._track_button_events = value
        if value:
            pygame.event.set_allowed(pygame.JOYBUTTONDOWN)
            pygame.event.set_allowed(pygame.JOYBUTTONUP)
        else:
            pygame.event.set_blocked(pygame.JOYBUTTONDOWN)
            pygame.event.set_blocked(pygame.JOYBUTTONUP)

    @property
    def track_motion_events(self):
        """Getter for track_motion_events."""

        return self._track_motion_events

    @track_motion_events.setter
    def track_motion_events(self, value):
        """Setter for track_motion_events.

        Switch on/off the processing of motion events.

        """

        self._track_motion_events = value
        if value:
            pygame.event.set_allowed(pygame.JOYAXISMOTION)
            pygame.event.set_allowed(pygame.JOYBALLMOTION)
            pygame.event.set_allowed(pygame.JOYHATMOTION)
        else:
            pygame.event.set_blocked(pygame.JOYAXISMOTION)
            pygame.event.set_blocked(pygame.JOYBALLMOTION)
            pygame.event.set_blocked(pygame.JOYHATMOTION)

    @property
    def id(self):
        """Getter for id."""

        return self._joystick.get_id()

    @property
    def name(self):
        """Getter for name."""

        return self._joystick.get_name()

    @property
    def joystick(self):
        """Getter for joystick."""

        return self._joystick

    def get_numaxes(self):
        """Get the number of axes."""

        return self._joystick.get_numaxes()

    def get_axis(self, axis):
        """Get current axis state.

        Parameters
        ----------
        axis : int
            axis to get the current state from

        """

        pygame.event.pump()
        return self._joystick.get_axis(axis)

    def get_numballs(self):
        """Get the number of balls."""

        return self._joystick.get_numballs()

    def get_ball(self, ball):
        """Get current ball state.

        Parameters
        ----------
        ball : int
            ball to get the current state from

        """

        pygame.event.pump()
        return self._joystick.get_ball(ball)

    def get_numbuttons(self):
        """Get the number of buttons."""

        return self._joystick.get_numbuttons()

    def get_button(self, button):
        """Get current button state.

        Parameters
        ----------
        button : int
            button to get the current state from

        """

        pygame.event.pump()
        return self._joystick.get_button(button)

    def get_numhats(self):
        """Get the number of hats."""

        return self._joystick.get_numhats()

    def get_hat(self, hat):
        """Get current hat state.

        Parameters
        ----------
        hat : int
            hat to get the current state from

        """

        pygame.event.pump()
        return self._joystick.get_hat(hat)


    def clear(self):
        """Clear gamepad events from cue."""

        pygame.event.clear(pygame.JOYBUTTONDOWN)
        pygame.event.clear(pygame.JOYBUTTONUP)
        pygame.event.clear(pygame.JOYAXISMOTION)
        pygame.event.clear(pygame.JOYBALLMOTION)
        pygame.event.clear(pygame.JOYHATMOTION)
        if self._logging:
            _internals.active_exp._event_file_log("GamePad,cleared", 2)

    def wait_press(self, buttons=None, duration=None, callback_function=None,
                   process_control_events=True):
        """Wait for gamepad button press.

        Returns the found button and the reaction time.

        Parameters
        ----------
        buttons : int or list, optional
            specific buttons to wait for
        duration : int, optional
            maximal time to wait in ms
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = True)

        Returns
        -------
        button : int
            button _id of the pressed button
        rt : int
            reaction time in ms

        Notes
        ------
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
        _button = None
        self.clear()
        if buttons is None:
            buttons = list(range(self.get_numbuttons()))
        try:
            buttons = list(buttons)
        except:
            buttons = [buttons]
        done = False
        while not done:
            if isinstance(callback_function, FunctionType):
                rtn_callback = callback_function()
                if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                    _button = rtn_callback
                    rt = int((get_time() - start) * 1000)
                    done = True
            if _internals.active_exp is not None and \
               _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, _internals.CallbackQuitEvent):
                    _button = rtn_callback
                    rt = int((get_time() - start) * 1000)
                    done = True
                if process_control_events:
                    if _internals.active_exp.mouse.process_quit_event() or \
                       _internals.active_exp.keyboard.process_control_keys():
                        done = True
            for button in buttons:
                if self.get_button(button):
                    _button = button
                    rt = int((get_time() - start) * 1000)
                    done = True
                    break
                if _button is not None:
                    done = True
                    break
                if duration:
                    if int((get_time() - start) * 1000) >= duration:
                        done = True
                        break

            time.sleep(0.0005)

        if self._logging:
            _internals.active_exp._event_file_log(
                            "Gamepad,received,{0},wait_press".format(_button))
        return _button, rt
