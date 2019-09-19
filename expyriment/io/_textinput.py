"""
A text input box.

This module contains a class implementing a text input box for user input.

"""
from __future__ import absolute_import, print_function, division
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, pow, range, round,
                      str, super, zip)  # without open, because
                       # pygame.font.Font needs old file object under PY2


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import pygame
try:
    import android
except ImportError:
    android = None

try:
    import android.show_keyboard as android_show_keyboard
    import android.hide_keyboard as android_hide_keyboard
except ImportError:
    android_show_keyboard = android_hide_keyboard = None

from . import defaults
from .. import _internals, stimuli
from ..misc import find_font, unicode2byte, constants, \
                 numpad_digit_code2ascii
from .._internals import CallbackQuitEvent
from ._input_output import Input


class TextInput(Input):
    """A class implementing a text input box."""

    def __init__(self, message="", position=None, character_filter=None,
                 length=None, message_text_size=None, message_colour=None,
                 message_font=None, message_bold=None, message_italic=None,
                 message_right_to_left=None, user_text_size=None,
                 user_text_bold=None, user_text_font=None,
                 user_text_colour=None, user_right_to_left=None,
                 background_colour=None, frame_colour=None, gap=None,
                 screen=None, background_stimulus=None, **kwargs):

        """Create a text input box.

        Notes
        -----
        This stimulus is not optimized for timing accurate presentation!

        Parameters
        ----------
        message : str, optional
            message to show
        position : (int, int), optional
            position of the TextInput canvas
        length : int, optional
            the length of the text input frame in number of characters
        character_filter : list, optional
            list of character codes to filter for
        message_text_size : int, optional
            text size of the message
        message_colour : (int, int, int), optional
            text colour of the message
        message_font : str, optional
            text font of the message
        message_bold : bool, optional
            True if message text should be bold
        message_italic : bool, optional
            True if message text should be italic
        message_right_to_left : bool, optional
            whether or not the message text should be presented right-to-left
        user_text_size : int, optional
            text size of the user input
        user_text_font : str, optional
            text font of the user input
        user_text_colour : (int, int ,int), optional
            text colour of the user input
        user_text_bold : bool, optional
            True if user text should be bold
        user_right_to_left : bool, optional
            whether or not the user text should be presented right-to-left
        background_colour : (int, int, int), optional
        frame_colour : (int, int, int)
            colour of the frame
        gap : int, optional
            gap between message and user input
        screen : io.Screen, optional
            screen to present on
        background_stimulus : visual Expyriment stimulus, optional
            The background stimulus is a second stimulus that will be presented
            together with the TextInput. For both stimuli overlap TextInput
            will appear on top of the background_stimulus

        """

        if not _internals.active_exp.is_initialized:
            raise RuntimeError(
                "Cannot create TextInput before expyriment.initialize()!")
        Input.__init__(self)
        self._message = message
        if position is not None:
            self._position = position
        else:
            self._position = defaults.textinput_position
        if character_filter is not None:
            self._character_filter = character_filter
        else:
            self._character_filter = defaults.textinput_character_filter
        if "ascii_filter" in kwargs:
            self._character_filter = kwargs["ascii_filter"]
        if length is not None:
            self._length = length
        else:
            self._length = defaults.textinput_length
        if message_text_size is None:
            message_text_size = defaults.textinput_message_text_size
        if message_text_size is not None:
            self._message_text_size = message_text_size
        else:
            self._message_text_size = _internals.active_exp.text_size
        if message_colour is None:
            message_colour = defaults.textinput_message_colour
        if message_colour is not None:
            self._message_colour = message_colour
        else:
            self._message_colour = _internals.active_exp.foreground_colour
        if message_font is None:
            message_font = defaults.textinput_message_font
        if message_font is None:
            message_font = _internals.active_exp.text_font
        if message_font is None:
            message_font = "FreeSans"
        self._message_font = find_font(message_font)
        try:
            with open(self._message_font, 'rb') as f:
                pygame.font.Font(f, 10)
        except:
            raise IOError("Font '{0}' not found!".format(message_font))
        if message_bold is not None:
            self._message_bold = message_bold
        else:
            self._message_bold = defaults.textinput_message_bold
        if message_italic is not None:
            self._message_italic = message_italic
        else:
            self._message_italic = defaults.textinput_message_italic
        if message_right_to_left is not None:
            self._message_right_to_left = message_right_to_left
        else:
            self._message_right_to_left = defaults.textinput_message_right_to_left
        if user_text_size is None:
            user_text_size = defaults.textinput_user_text_size
        if user_text_size is not None:
            self._user_text_size = user_text_size
        else:
            self._user_text_size = _internals.active_exp.text_size

        if user_text_bold is not None:
            self._user_text_bold = user_text_bold
        else:
            self._user_text_bold = defaults.textinput_user_text_bold
        if user_text_font is None:
            user_text_font = defaults.textinput_user_text_font
        if user_text_font is None:
            user_text_font = _internals.active_exp.text_font
        if user_text_font is None:
            user_text_font = "FreeSans"
        self._user_text_font = find_font(user_text_font)
        try:
            with open(self._user_text_font, 'rb') as f:
                pygame.font.Font(f, 10)
        except:
            raise IOError("Font '{0}' not found!".format(user_text_font))
        if user_text_colour is None:
            user_text_colour = defaults.textinput_user_text_colour
        if user_text_colour is not None:
            self._user_text_colour = user_text_colour
        else:
            self._user_text_colour = _internals.active_exp.foreground_colour
        if user_right_to_left is not None:
            self._user_right_to_left = user_right_to_left
        else:
            self._user_right_to_left = defaults.textinput_user_right_to_left
        if background_colour is None:
            background_colour = \
                defaults.textinput_background_colour
        if background_colour is not None:
            self._background_colour = background_colour
        else:
            self._background_colour = \
                _internals.active_exp.background_colour
        if frame_colour is None:
            frame_colour = defaults.textinput_frame_colour
        if frame_colour is not None:
            self._frame_colour = frame_colour
        else:
            self._frame_colour = _internals.active_exp.foreground_colour
        if gap is not None:
            self._gap = gap
        else:
            self._gap = defaults.textinput_gap
        if screen is not None:
            self._screen = screen
        else:
            self._screen = _internals.active_exp.screen
        if background_stimulus is not None:
            if background_stimulus.__class__.__bases__[0] == stimuli._visual.Visual:
                self._background_stimulus = background_stimulus
            else:
                raise TypeError("{0} ".format(type(background_stimulus)) +
                                     "is not a valid background stimulus. " +
                                     "Use an expyriment visual stimulus.")
        else:
            self._background_stimulus = None

        self._user = []
        self._user_text_surface_size = None
        self._max_size = None
        self._message_surface_size = None
        self._canvas = None
        self._canvas_size = None

    @property
    def message(self):
        """Getter for message"""
        return self._message

    @property
    def position(self):
        """Getter for position"""
        return self._position

    @property
    def character_filter(self):
        """Getter for character filter"""

        return self._character_filter

    @character_filter.setter
    def character_filter(self, value):
        """Getter for character filter"""

        self._character_filter = value

    @property
    def message_text_size(self):
        """Getter for message_text_size"""
        return self._message_text_size

    @property
    def length(self):
        """Getter for length"""
        return self._length

    @property
    def message_colour(self):
        """Getter for message_colour"""
        return self._message_colour

    @property
    def message_font(self):
        """Getter for message_font"""
        return self._message_font

    @property
    def message_bold(self):
        """Getter for message_bold"""
        return self._message_bold

    @property
    def message_italic(self):
        """Getter for message_italic"""
        return self._message_italic

    @property
    def message_right_to_left(self):
        """getter for message_right_to_left"""
        return self._message_right_to_left

    @property
    def user_text_size(self):
        """Getter for user_text_size"""
        return self._user_text_size

    @property
    def user_text_bold(self):
        """Getter for user_text_bold"""
        return self._user_text_bold

    @property
    def user_text_font(self):
        """Getter for user_text_font"""
        return self._user_text_font

    @property
    def user_text_colour(self):
        """Getter for user_text_colour"""
        return self._user_text_colour

    @property
    def user_right_to_left(self):
        """Getter for user_right_to_left"""
        return self._user_right_to_left

    @property
    def background_colour(self):
        """Getter for background_colour"""
        return self._background_colour

    @property
    def frame_colour(self):
        """Getter for frame_colour"""
        return self._frame_colour

    @property
    def gap(self):
        """Getter for gap"""
        return self._gap

    @property
    def screen(self):
        """Getter for screen"""
        return self._screen

    @property
    def background_stimulus(self):
        """Getter for background_stimulus"""
        return self._background_stimulus

    def _get_key(self, process_control_events):
        """Get a key press."""

        while True:
            rtn_callback = _internals.active_exp._execute_wait_callback()
            if isinstance(rtn_callback, CallbackQuitEvent):
                return rtn_callback, None

            if process_control_events:
                _internals.active_exp.mouse.process_quit_event()

            events = pygame.event.get(pygame.KEYDOWN)
            for event in events:
                if process_control_events:
                    if _internals.active_exp.keyboard.process_control_keys(event):
                        self._create()
                        self._update()
                        return None, None
                return event.key, event.unicode

    def _create(self):
        """Create the input box."""

        tmp = stimuli.TextLine(text=self._length * "X",
                               text_font=self.user_text_font,
                               text_size=self.user_text_size,
                               text_bold=self.user_text_bold)
        stimuli._stimulus.Stimulus._id_counter -= 1
        self._max_size = tmp.surface_size
        text = self._message
        if self._message_right_to_left:
            text = self._message[::-1]
        message_text = stimuli.TextLine(
            text=text, text_font=self.message_font,
            text_size=self.message_text_size, text_bold=self.message_bold,
            text_italic=self.message_italic, text_colour=self.message_colour,
            background_colour=self._background_colour)
        stimuli._stimulus.Stimulus._id_counter -= 1
        self._message_surface_size = message_text.surface_size

        self._canvas = stimuli.Canvas(size=(
            max(self._max_size[0] + 12, self._message_surface_size[0]),
            self._message_surface_size[1] + self._max_size[1] + self._gap + 5),
            colour=self._background_colour, position=self._position)

        #self._canvas = expyriment.stimuli.BlankScreen()

        stimuli._stimulus.Stimulus._id_counter -= 1
        self._canvas._set_surface(self._canvas._get_surface())
        self._canvas_size = self._canvas.surface_size
        pygame.draw.rect(self._canvas._get_surface(), self._background_colour,
                         (self._canvas_size[0] // 2 - self._max_size[0] // 2 - 6,
                          self._message_surface_size[1] + self._gap,
                          self._max_size[0] + 12, self._max_size[1] + 5), 0)
        pygame.draw.rect(self._canvas._get_surface(), self._frame_colour,
                         (self._canvas_size[0] // 2 - self._max_size[0] // 2 - 6,
                          self._message_surface_size[1] + self._gap,
                          self._max_size[0] + 12, self._max_size[1] + 5), 1)
        if len(self._message) != 0:
            if self._message_right_to_left:
                self._canvas._get_surface().blit(
                    message_text._get_surface(),
                    (self._canvas.surface_size[0] -
                    self._message_surface_size[0], 0))
            else:
                self._canvas._get_surface().blit(
                    message_text._get_surface(),
                    (self._canvas.surface_size[0] // 2 -
                    self._message_surface_size[0] // 2, 0))
        background = stimuli.BlankScreen(
            colour=self._background_colour)
        if self._background_stimulus is not None:
            self._background_stimulus.plot(background)
        self._canvas.plot(background)
        background.present()
        background.present()  # for flipping with double buffer
        background.present()  # for flipping with tripple buffer

    def _update(self):
        """Update the input box."""

        user_canvas = stimuli.Canvas(
            size=self._max_size, colour=self._background_colour)
        stimuli._stimulus.Stimulus._id_counter -= 1
        user_canvas._set_surface(user_canvas._get_surface())
        user_canvas_size = user_canvas.surface_size
        offset = 2 + user_canvas_size[1] % 2
        user_canvas.position = (self._canvas.absolute_position[0],
                                self._canvas.absolute_position[1] +
                                self._canvas_size[1] // 2 -
                                user_canvas_size[1] // 2 -
                                self._message_surface_size[1] -
                                self._gap - offset)
        text = "".join(self._user)
        if self._user_right_to_left:
            text = "".join(self._user)[::-1]
        user_text = stimuli.TextLine(
            text=text,
            text_font=self.user_text_font, text_size=self.user_text_size,
            text_bold=self.user_text_bold, text_colour=self.user_text_colour,
            background_colour=self.background_colour)
        stimuli._stimulus.Stimulus._id_counter -= 1
        self._user_text_surface_size = user_text.surface_size
        if self._user_right_to_left:
            user_canvas._get_surface().blit(
                user_text._get_surface(),
                (user_canvas.surface_size[0] -
                 self._user_text_surface_size[0], 2))
        else:
            user_canvas._get_surface().blit(user_text._get_surface(), (0, 2))
        user_canvas.present(clear=False)

    def get(self, default_input="", process_control_events=True):
        """Get input from user.

        Notes
        -----
        This displays and updates the input box automatically. Pressing ENTER
        returns the user input.

        Parameters
        ----------
        default_input : str, optional
            default input in the textbox
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = True)

        Returns
        -------
        text_input: str or None
            returns the entered text string. If get() is interrupted by a
            CallbackQuitEvent from a registered wait-callback-function get()
            returns None.

        See Also
        --------
        design.experiment.register_wait_callback_function

        """

        if android_show_keyboard is not None:
            android_show_keyboard()
        self._user = []
        for char in default_input:
            self._user.append(char)
        self._create()
        self._update()
        if self._character_filter is None:
            filter = list(range(0, 256)) + constants.K_ALL_KEYPAD_DIGITS
        else:
            filter = self._character_filter

        while True:
            inkey, string = self._get_key(process_control_events)
            if isinstance(inkey, CallbackQuitEvent):
                return None
            elif inkey == pygame.K_BACKSPACE:
                self._user = self._user[0:-1]
            elif inkey == pygame.K_RETURN or inkey == pygame.K_KP_ENTER:
                break
            elif inkey not in (pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_TAB):
                if not self._user_text_surface_size[0] >= self._max_size[0]:
                    if android is not None:
                        if inkey in filter:
                            if inkey in constants.K_ALL_KEYPAD_DIGITS:
                                inkey = numpad_digit_code2ascii(inkey)
                            self._user.append(chr(inkey))
                    else:
                        if inkey in constants.K_ALL_KEYPAD_DIGITS:
                            self._user.append(chr(numpad_digit_code2ascii(
                                inkey)))
                        elif string and ord(string) in filter:
                            self._user.append(string)
            self._update()
        got = "".join(self._user)
        if self._logging:
            _internals.active_exp._event_file_log("TextInput,entered,{0}"
                                                   .format(unicode2byte(got)))
        if android_hide_keyboard is not None:
            android_hide_keyboard()
        return got


    @staticmethod
    def _demo(exp=None):
        if exp is None:
            from .. import control
            control.set_develop_mode(True)
            control.defaults.event_logging = 0
            exp_ = control.initialize()
        textinput = TextInput(message="Subject Number:",
                              message_colour=(160, 70, 250),
                              user_text_size=30,
                              user_text_colour=(255, 150, 50),
                              frame_colour=(70, 70, 70))
        print(textinput.get())
