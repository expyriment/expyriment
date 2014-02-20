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

    def __init__(self, button_fields,
                stimuli=[], background_stimulus=None):
        """Initialize a touchscreen button box.

        Parameters
        ----------
        button_fields : visual Expyriment stimulus or list of stimuli
            The button fields defines the area on which a click action will be
            registered.
        stimuli : visual Expyriment stimulus or list of stimuli, optional
            Additonal visual stimuli that will be presented together with the button
            fields. Stimuli are plotted ontop of the button_fields.
        background_stimulus : visual Expyriment stimulus, optional
            The background stimulus on which the the touschscreen button fields
            are presented. Importantly, background_stimulus has to have the size of
            the screen.

        Notes
        -----
        Every visual Expyriment stimulus can serve as a touchscreen button field.
        If the TouchScreenButtonBox is presented, it can be checked for events
        using the methods 'check' and 'wait'.

        """

        #FIXME: What to do if the backgorund stimulus has not the size of the screen

        Input.__init__(self)

        if type(button_fields) is not list:
            button_fields = [button_fields]
        if type(stimuli) is not list:
            stimuli = [stimuli]

        self._mouse = None
        self._canvas = None
        self._button_fields = []
        self._stimuli = []
        self.background_stimulus = background_stimulus
        map(self.add_button_field, button_fields)
        map(self.add_stimulus, stimuli)

    def add_button_field(self, button_field):
        """Add a touchscreen button fields.

        Parameters
        ----------
        button_field : visual expyriment stimulus

        """

        if not isinstance(button_field, expyriment.stimuli._visual.Visual):
            raise TypeError("Button field has to a visual Expyriment stimulus")
        self._button_fields.append(button_field)
        self._canvas = None

    def add_stimulus(self, stimulus):
        """Add additonal stimulus that will be presented together with the button
        fields.

        Parameters
        ----------
        stimulus : visual expyriment stimulus

        """
        if not isinstance(stimulus, expyriment.stimuli._visual.Visual):
            raise TypeError("Additional stimuli has to a visual Expyriment stimulus")
        self._stimuli.append(stimulus)
        self._canvas = None

    @property
    def button_field(self):
        """getter of button fields (list of visual Expyriment stimuli)"""
        return self._button_fields

    @property
    def stimuli(self):
        """getter of additonal stimuli (list of visual Expyriment stimuli)"""
        return self._stimuli

    @property
    def background_stimulus(self):
        """Getter of background stimulus.

        Background stimulus, on which the button fields and the addtional stimuli
        will be presented. (visual Expyriment stimuli)

        """
        return self._background_stimulus

    @background_stimulus.setter
    def background_stimulus(self, stimulus):
        """Setter background stimulus"""
        if stimulus is None:
            self._background_stimulus = expyriment.stimuli.BlankScreen()
        elif not isinstance(stimulus, expyriment.stimuli._visual.Visual):
            raise TypeError("Background stimulus has to be be a " +\
                            "visual Expyriment stimulus")
        else:
            self._background_stimulus = stimulus
        self._canvas = None

    def clear_event_buffer(self):
        """Clear the event buffer of the touchscreen/mouse input device."""

        if self._mouse is not None:
            self._mouse.clear()

    def preload(self):
        """Prepare and preload the button fields and addtional stimuli for
        presentation.

        """

        self._canvas = self._background_stimulus.copy()
        if len(self._button_fields)<1:
            raise RuntimeError("No button field defined!")
        map(lambda x:x.plot(self._canvas), self._button_fields)
        map(lambda x:x.plot(self._canvas), self._stimuli)
        self._canvas.preload()

    def unload(self):
        if self._canvas is not None:
            self._canvas.unload()
        self._canvas = None

    def present(self, show_cursor=True):
        """Present touchscreen buttons.

        Parameters
        ----------
        show_cursor : bool, optional
            shows mouse cursor (default = True)

        """

        if self._canvas is None:
            self.preload()
        if self._mouse is None:
            self._mouse = expyriment.io.Mouse()
            self._mouse.set_logging(False)
        if show_cursor:
            self._mouse.show_cursor()
        else:
            self._mouse.hide_cursor()
        self._mouse.clear()
        self._canvas.present()

    def check(self, button_fields=None, check_for_control_keys=True):
        """Check if a button field is clicked.

        Parameters
        ----------
        button_fields : Expyriment stimulus or list of stimuli, optional
            The button fields that will be checked for.
        check_for_control_keys : bool, optional
            checks if control key has been pressed (default=True)

        Returns
        -------
        pressed_button_field : int
            id of the clicked button field
            (i.e., position in button field list)

        Notes
        -----
        Don't forget to present the TouchScreenButtonBox before checking for
        events.

        """

        # TODO: return also touch coordinate (xy)

        if button_fields is not None and type(button_fields) is not list:
            button_fields = [button_fields]
        if self._mouse is None:
            raise RuntimeError("Wait or check touchscreen buttonbox " + \
                                "before present.")
        if check_for_control_keys:
            expyriment.io.Keyboard.process_control_keys()

        pressed_button_field = None
        if self._mouse.get_last_button_down_event() is not None:
            pressed_button_field = self._get_button_field(self._mouse.position,
                    button_fields)

            if self._logging and pressed_button_field is not None:
                expyriment._active_exp._event_file_log(
                                "{0},received,{1},check".format(
                                    self.__class__.__name__, pressed_button_field))
        return pressed_button_field

    def _get_button_field(self, position, button_fields):
        """ helper function return the button field of the position"""
        if button_fields is None:
            button_fields = self._button_fields
        for bf in button_fields:
            if bf.overlapping_with_position(position):
                return bf
        return None


    def wait(self, duration=None, button_fields=None,
                check_for_control_keys=True):
        """Wait for a touchscreen button box click.

        Parameters
        ----------
        button_fields : Expyriment stimulus or list of stimuli, optional
            The button fields that will be checked for.
        duration : int, optional
            maximal time to wait in ms
        wait_for_buttonup : bool, optional
            if True it waits for button-up

        Returns
        -------
        pressed_button_field : Expyriment stimulus or None
            the button field defined by a stimulus that has been pressed
        rt : int
            reaction time

        Notes
        -----
        Don't forget to present the TouchScreenButtonBox before waiting for
        events.

        """

        # TODO: return also touch coordinate (xy)

        start = get_time()
        self.clear_event_buffer()
        while True:
            expyriment._active_exp._execute_wait_callback()
            pressed_button_field = self.check(button_fields,
                        check_for_control_keys)
            rt = int((get_time() - start) * 1000)
            if pressed_button_field is not None:
                break
            elif (duration is not None and rt>= duration):
                pressed_button_field, rt = None, None
                break
        return pressed_button_field, rt
