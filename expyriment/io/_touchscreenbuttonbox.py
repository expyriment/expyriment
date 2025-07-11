"""
A touchscreen button box.

This module contains a class implementing a touchscreen button box.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

from types import FunctionType

import pygame

from .. import _internals, stimuli
from .._internals import CallbackQuitEvent
from ..misc._timer import get_time
from ._input_output import Input


class TouchScreenButtonBox(Input):
    """A class implementing a TouchScreenButtonBox."""

    def __init__(self, button_fields, stimuli=None, background_stimulus=None):
        """initialise a touchscreen button box.

        Parameters
        ----------
        button_fields : visual Expyriment stimulus or list of stimuli
            The button fields defines the area on which a click action will be
            registered.
        stimuli : visual Expyriment stimulus or list of stimuli, optional
            Additional visual stimuli that will be presented together with the
            button fields. Stimuli are plotted on top of the button_fields.
        background_stimulus : visual Expyriment stimulus, optional
            The background stimulus on which the touschscreen button fields
            are presented. Importantly, background_stimulus has to have
            size of the screen.

        Notes
        -----
        Every visual Expyriment stimulus can serve as a touchscreen button
        field.
        If the TouchScreenButtonBox is presented, it can be checked for events
        using the methods 'check' and 'wait'.

        """

        Input.__init__(self)

        try:
            button_fields = list(button_fields)
        except Exception:
            button_fields = [button_fields]

        if stimuli is None:
            stimuli = []
        else:
            try:
                stimuli = list(stimuli)
            except Exception:
                stimuli = [stimuli]

        self._mouse = _internals.active_exp.mouse
        self._last_touch_position = None
        self._canvas = None
        self._button_fields = []
        self._stimuli = []
        self.background_stimulus = background_stimulus

        for x in button_fields:
            self.add_button_field(x)
        for x in stimuli:
            self.add_stimulus(x)

    def add_button_field(self, button_field):
        """Add a touchscreen button fields.

        Parameters
        ----------
        button_field : visual Expyriment stimulus

        """

        if not isinstance(button_field, stimuli._visual.Visual):
            raise TypeError("Button field has to be a visual Expyriment stimulus")
        self._button_fields.append(button_field)
        self._canvas = None

    def add_stimulus(self, stimulus):
        """Add additional stimulus

        The added stimulus will be presented together with the button fields.

        Parameters
        ----------
        stimulus : visual Expyriment stimulus

        """
        if not isinstance(stimulus, stimuli._visual.Visual):
            raise TypeError("Additional stimuli has to be a visual Expyriment stimulus")
        self._stimuli.append(stimulus)
        self._canvas = None

    @property
    def last_touch_position(self):
        """getter for the last touch position (x,y)"""
        return self._last_touch_position

    @property
    def button_field(self):
        """getter of button fields (list of visual Expyriment stimuli)"""
        return self._button_fields

    @property
    def stimuli(self):
        """getter of additional stimuli (list of visual Expyriment stimuli)"""
        return self._stimuli

    @property
    def background_stimulus(self):
        """Getter of background stimulus.

        Background stimulus, on which the button fields and the additional
        stimuli will be presented. (visual Expyriment stimuli)

        """
        return self._background_stimulus

    @background_stimulus.setter
    def background_stimulus(self, stimulus):
        """Setter background stimulus"""
        if stimulus is None:
            self._background_stimulus = stimuli.BlankScreen()
        elif not isinstance(stimulus, stimuli._visual.Visual):
            raise TypeError("Background stimulus has to be a " +
                            "visual Expyriment stimulus")
        else:
            self._background_stimulus = stimulus
        self._canvas = None

    def clear_event_buffer(self):
        """Clear the event buffer of the touchscreen/mouse input device."""

        if self._mouse is not None:
            self._mouse.clear()

    def create(self):
        """Create the touchscreen buttonbox.

        Prepares the button fields and additional stimuli for fast
        presentation.

        """

        self._canvas = self._background_stimulus.copy()
        print(self._canvas)
        if len(self._button_fields) < 1:
            raise RuntimeError("No button field defined!")
        for x in self._button_fields:
            x.plot(self._canvas)
        for x in self._stimuli:
            x.plot(self._canvas)
        self._canvas.preload()

    def destroy(self):
        if self._canvas is not None:
            self._canvas.unload()
        self._canvas = None

    def show(self):
        """Present touchscreen buttons."""

        if self._canvas is None:
            self.create()
        self._canvas.present()

    def check(self, button_fields=None):
        """Check if a button field is clicked.

        Parameters
        ----------
        button_fields : Expyriment stimulus or list of stimuli, optional
            The button fields that will be checked for.

        Returns
        -------
        pressed_button_field : Expyriment stimulus or list of stimuli, optional
            The button fields that will be checked for.
        touch_time : integer
            The time when the button was touched. Function might return delayed,
            because button field comparison (after touch) takes time. The
            return time is most accurate.


        Notes
        -----
        Don't forget to show the TouchScreenButtonBox.

        """

        if button_fields is not None:
            try:
                button_fields = list(button_fields)
            except Exception:
                button_fields = [button_fields]

        pressed_button_field = None
        touch_time = None
        if self._mouse.get_last_button_down_event() is not None:
            touch_time = get_time()
            self._last_touch_position = self._mouse.position
            pressed_button_field = self._get_button_field(self._last_touch_position,
                    button_fields)

            if self._logging and pressed_button_field is not None:
                _internals.active_exp._event_file_log(
                                "{0},received, button press,check".format(
                                    self.__class__.__name__))
        return pressed_button_field, touch_time

    def _get_button_field(self, position, button_fields):
        """ helper function return the button field of the position"""
        if button_fields is None:
            button_fields = self._button_fields
        for bf in button_fields:
            if bf.overlapping_with_position(position):
                return bf
        return None

    def wait(self, duration=None, button_fields=None, callback_function=None,
                process_control_events=True, low_performance=False):
        """Wait for a touchscreen button box click.

        Parameters
        ----------
        button_fields : Expyriment stimulus or list of stimuli, optional
            The button fields that will be checked for.
        duration : int, optional
            maximal time to wait in ms
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
        pressed_button_field : Expyriment stimulus or None
            the button field defined by a stimulus that has been pressed
        rt : int
            reaction time

        Notes
        -----
        This will also by default process control events (quit and pause).
        Thus, keyboard events will be cleared from the cue and cannot be
        received by a Keyboard().check() anymore!

        Don't forget to show the TouchScreenButtonBox.

        See Also
        --------
        expyriment.design.Experiment.register_wait_callback_function

        """

        if _internals.skip_wait_methods:
            return None, None
        start = get_time()
        self.clear_event_buffer()
        while True:
            if isinstance(callback_function, FunctionType):
                rtn_callback = callback_function()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    return rtn_callback, int((get_time()-start)*1000)
            if _internals.active_exp.is_initialised:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    return rtn_callback, int((get_time()-start)*1000)
                if process_control_events:
                    if _internals.active_exp.mouse.process_quit_event() or \
                       _internals.active_exp.keyboard.process_control_keys():
                        pressed_button_field, rt = None, None
                        break
                else:
                    pygame.event.pump()
            pressed_button_field, touch_time = self.check(button_fields)
            if pressed_button_field is not None:
                rt = int((get_time()-start)*1000)
                break
            elif (duration is not None and int((get_time()-start)*1000)>=duration):
                pressed_button_field, rt = None, None
                break
            if low_performance:
                _internals.low_performance_sleep()

        return pressed_button_field, rt
