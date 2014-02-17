"""
A touchscreen button box.

This module contains a class implementing a text input box for user input.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import defaults
import expyriment
from expyriment.misc._timer import get_time
from _input_output import Input

class TouchScreenButtonBox(Input):
    """A class implementing a TouchScreenButton."""

    def __init__(self, button_fields):
        """Initialize a touchscreen button box.

        Parameters
        ----------
        button_field : visual Expyriment stimulus or list of stimuli

        Notes
        -----
        Every visual Expyriment stimulus can serve as a touchscreen button field.
        If the TouchScreenButtonBox is presented, it can be checked for events
        using the methods 'check' and 'wait'. Methods return the id of the
        button field. Added field will be numbered starting with 0.

        """

        Input.__init__(self)

        if type(button_fields) is not list:
            button_fields = [button_fields]

        self._button_fields = []
        self._mouse = None
        map(self.add_button_field, button_fields)

    def add_button_field(self, button_field):
        """Add a touchscreen button fields.

        Parameters
        ----------
        button_field : visual expyriment stimulus

        Notes
        -----
        First add field get the id=0, the second the id=1 and so on...

        """

        if not isinstance(button_field, expyriment.stimuli._visual.Visual):
            raise TypeError("Button field has to a visual Expyriment stimulus")
        self._button_fields.append(button_field)


    @property
    def button_field(self):
        """getter of button fields (list of visual Expyriment stimuli)"""
        return self._button_fields

    def clear(self):
        """Clear the event buffer of the touchscreen/mouse input device."""

        if self._mouse is not None:
            self._mouse.clear()

    def present(self, background_stimulus=None, show_cursor=True):
        """Present touchscreen buttons.

        Parameters
        ----------
        background_stimulus : visual Expyriment stimulus, optional
            The background stimulus on which the the touschscreen button fields
            are presented
        show_cursor : bool, optional
            shows mouse cursor (default = True)

        """

        if background_stimulus is None:
            stim = expyriment.stimuli.BlankScreen()
        elif not isinstance(background_stimulus,
                                expyriment.stimuli._visual.Visual):
            raise TypeError("Background stimulus has to be be a " +\
                            "visual Expyriment stimulus")
        else:
            stim = background_stimulus.copy()
        if len(self._button_fields)<1:
            raise RuntimeError("No button field defined!")

        map(lambda x:x.plot(stim), self._button_fields)
        self._mouse = expyriment.io.Mouse(show_cursor=show_cursor)
        self._mouse.set_logging(False)
        self._mouse.clear()
        stim.present()

    def check(self, button_field_ids=None, check_for_control_keys=True):
        """Check if a button field is clicked.

        Parameters
        ----------
        button_field_ids : int or list, optional
            a specific button_field_ids or list of button_field_ids to
            check for
        check_for_control_keys : bool, optional
            checks if control key has been pressed (default=True)

        Returns
        -------
        pressed_button : int
            id of the clicked button field
            (i.e., position in button field list)

        Notes
        -----
        Don't forget to present the TouchScreenButtonBox before checking for
        events.

        """

        if button_field_ids is not None and \
                type(button_field_ids) is not list:
            button_field_ids = [button_field_ids]
        if self._mouse is None:
            raise RuntimeError("Wait or check touchscreen buttonbox " + \
                                "before present.")
        if check_for_control_keys:
            expyriment.io.Keyboard.process_control_keys()

        pressed_button = None
        if self._mouse.get_last_button_down_event() is not None:
            pressed_button = self._get_button_field(self._mouse.position,
                    button_field_ids)

            if self._logging and pressed_button is not None:
                expyriment._active_exp._event_file_log(
                                "{0},received,{1},check".format(
                                    self.__class__.__name__, pressed_button))
        return pressed_button

    def _get_button_field(self, position, button_field_ids=None):
        """ helper function return the button field of the position"""
        if button_field_ids is None:
            button_field_ids = range(len(self._button_fields))
        for x in button_field_ids:
            if x>=0 and x<len(self._button_fields) and \
                   self._button_fields[x].overlapping_with_position(position):
                return x
        return None


    def wait(self, duration=None, button_field_ids=None,
                check_for_control_keys=True):
        """Wait for a touchscreen button box click.

        Parameters
        ----------
        button_field_ids : int or list, optional
            a specific button_field_ids or list of button_field_ids to
            check for
        duration : int, optional
            maximal time to wait in ms
        wait_for_buttonup : bool, optional
            if True it waits for button-up

        Returns
        -------
        pressed_button : int
            id of the clicked button field
            (i.e., position in button field list)
        rt : int
            reaction time

        Notes
        -----
        Don't forget to present the TouchScreenButtonBox before waiting for
        events.

        """

        start = get_time()
        self.clear()
        while True:
            expyriment._active_exp._execute_wait_callback()
            pressed_button = self.check(button_field_ids,
                        check_for_control_keys)
            rt = int((get_time() - start) * 1000)
            if pressed_button is not None:
                break
            elif (duration is not None and rt>= duration):
                pressed_button, rt = None, None
                break
        return pressed_button, rt
