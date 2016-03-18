"""
A text input box.

This module contains a class implementing a text input box for user input.

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from builtins import chr
from builtins import range


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
from expyriment.misc import find_font, unicode2byte, constants, \
                 numpad_digit_code2ascii
import expyriment
from ._input_output import Input


class TextInput(Input):
    """A class implementing a text input box."""

    def __init__(self, message="", position=None, ascii_filter=None,
                 length=None, message_text_size=None, message_colour=None,
                 message_font=None, message_bold=None, message_italic=None,
                 user_text_size=None, user_text_bold=None, user_text_font=None,
                 user_text_colour=None, background_colour=None,
                 frame_colour=None, gap=None, screen=None,
                 background_stimulus=None):
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
            the length of the text input frame in number of charaters
        ascii_filter : list, optional
            list of ASCII codes to filter for
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
        user_text_size : int, optional
            text size of the user input
        user_text_font : str, optional
            text font of the user input
        user_text_colour : (int, int ,int), optional
            text colour of the user input
        user_text_bold : bool, optional
            True if user text should be bold
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

        if not expyriment._active_exp.is_initialized:
            raise RuntimeError(
                "Cannot create TextInput before expyriment.initialize()!")
        Input.__init__(self)
        self._message = message
        if position is not None:
            self._position = position
        else:
            self._position = defaults.textinput_position
        if ascii_filter is not None:
            self._ascii_filter = ascii_filter
        else:
            self._ascii_filter = defaults.textinput_ascii_filter
        if length is not None:
            self._length = length
        else:
            self._length = defaults.textinput_length
        if message_text_size is None:
            message_text_size = defaults.textinput_message_text_size
        if message_text_size is not None:
            self._message_text_size = message_text_size
        else:
            self._message_text_size = expyriment._active_exp.text_size
        if message_colour is None:
            message_colour = defaults.textinput_message_colour
        if message_colour is not None:
            self._message_colour = message_colour
        else:
            self._message_colour = expyriment._active_exp.foreground_colour
        if message_font is None:
            message_font = defaults.textinput_message_font
        if message_font is not None:
            self._message_font = find_font(message_font)
        else:
            self._message_font = find_font(expyriment._active_exp.text_font)
        try:
            _font = pygame.font.Font(
                unicode2byte(self._message_font, fse=True), 10)
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
        if user_text_size is None:
            user_text_size = defaults.textinput_user_text_size
        if user_text_size is not None:
            self._user_text_size = user_text_size
        else:
            self._user_text_size = expyriment._active_exp.text_size

        if user_text_bold is not None:
            self._user_text_bold = user_text_bold
        else:
            self._user_text_bold = defaults.textinput_user_text_bold
        if user_text_font is None:
            user_text_font = defaults.textinput_user_text_font
        if user_text_font is not None:
            self._user_text_font = find_font(user_text_font)
        else:
            self._user_text_font = find_font(expyriment._active_exp.text_font)
        try:
            _font = pygame.font.Font(
                unicode2byte(self._user_text_font, fse=True), 10)
        except:
            raise IOError("Font '{0}' not found!".format(user_text_font))
        if user_text_colour is None:
            user_text_colour = defaults.textinput_user_text_colour
        if user_text_colour is not None:
            self._user_text_colour = user_text_colour
        else:
            self._user_text_colour = expyriment._active_exp.foreground_colour
        if background_colour is None:
            background_colour = \
                defaults.textinput_background_colour
        if background_colour is not None:
            self._background_colour = background_colour
        else:
            self._background_colour = \
                expyriment._active_exp.background_colour
        if frame_colour is None:
            frame_colour = defaults.textinput_frame_colour
        if frame_colour is not None:
            self._frame_colour = frame_colour
        else:
            self._frame_colour = expyriment._active_exp.foreground_colour
        if gap is not None:
            self._gap = gap
        else:
            self._gap = defaults.textinput_gap
        if screen is not None:
            self._screen = screen
        else:
            self._screen = expyriment._active_exp.screen
        if background_stimulus is not None:
            # FIXME child of child of visual does not work as background stimulus, e.g. BlankScreen
            if background_stimulus.__class__.__base__ in \
                     [expyriment.stimuli._visual.Visual, expyriment.stimuli.Shape]:
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
    def ascii_code_filter(self):
        """Getter for filter"""
        return self._ascii_filter

    @ascii_code_filter.setter
    def ascii_code_filter(self, value):
        """Getter for filter"""
        self._ascii_filter = value

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

    def _get_key(self):
        """Get a key press."""

        while True:
            rtn_callback = expyriment._active_exp._execute_wait_callback()
            if isinstance(rtn_callback, expyriment.control.CallbackQuitEvent):
                return rtn_callback

            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                return event.key, event.unicode

    def _create(self):
        """Create the input box."""

        tmp = expyriment.stimuli.TextLine(text=self._length * "X",
                                          text_font=self.user_text_font,
                                          text_size=self.user_text_size,
                                          text_bold=self.user_text_bold)
        expyriment.stimuli._stimulus.Stimulus._id_counter -= 1
        self._max_size = tmp.surface_size
        message_text = expyriment.stimuli.TextLine(
            text=self._message, text_font=self.message_font,
            text_size=self.message_text_size, text_bold=self.message_bold,
            text_italic=self.message_italic, text_colour=self.message_colour,
            background_colour=self._background_colour)
        expyriment.stimuli._stimulus.Stimulus._id_counter -= 1
        self._message_surface_size = message_text.surface_size

        self._canvas = expyriment.stimuli.Canvas(size=(
            max(self._max_size[0] + 12, self._message_surface_size[0]),
            self._message_surface_size[1] + self._max_size[1] + self._gap + 5),
            colour=self._background_colour, position=self._position)

        #self._canvas = expyriment.stimuli.BlankScreen()

        expyriment.stimuli._stimulus.Stimulus._id_counter -= 1
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
                    self._canvas._get_surface().blit(
                        message_text._get_surface(),
                        (self._canvas.surface_size[0] // 2 -
                         self._message_surface_size[0] // 2, 0))
        background = expyriment.stimuli.BlankScreen(
            colour=self._background_colour)
        if self._background_stimulus is not None:
            self._background_stimulus.plot(background)
        self._canvas.plot(background)
        background.present()
        background.present()  # for flipping with double buffer
        background.present()  # for flipping with tripple buffer

    def _update(self):
        """Update the input box."""

        user_canvas = expyriment.stimuli.Canvas(
            size=self._max_size, colour=self._background_colour)
        expyriment.stimuli._stimulus.Stimulus._id_counter -= 1
        user_canvas._set_surface(user_canvas._get_surface())
        user_canvas_size = user_canvas.surface_size
        offset = 2 + user_canvas_size[1] % 2
        user_canvas.position = (self._canvas.absolute_position[0],
                                self._canvas.absolute_position[1] +
                                self._canvas_size[1] // 2 -
                                user_canvas_size[1] // 2 -
                                self._message_surface_size[1] -
                                self._gap - offset)
        user_text = expyriment.stimuli.TextLine(
            text="".join(self._user),
            text_font=self.user_text_font, text_size=self.user_text_size,
            text_bold=self.user_text_bold, text_colour=self.user_text_colour,
            background_colour=self.background_colour)
        expyriment.stimuli._stimulus.Stimulus._id_counter -= 1
        self._user_text_surface_size = user_text.surface_size
        user_canvas._get_surface().blit(user_text._get_surface(), (0, 2))
        user_canvas.present(clear=False)

    def get(self, default_input=""):
        """Get input from user.

        Notes
        -----
        This displays and updates the input box automatically. Pressing ENTER
        returns the user input. Pressing ESC quits, returning an empty string.

        Parameters
        ----------
        default_input : str, optional
            default input in the textbox

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
        if self._ascii_filter is None:
            ascii_filter = list(range(0, 256)) + constants.K_ALL_KEYPAD_DIGITS
        else:
            ascii_filter = self._ascii_filter
        while True:
            inkey, string = self._get_key()
            if inkey == pygame.K_BACKSPACE:
                self._user = self._user[0:-1]
            elif inkey == pygame.K_RETURN or inkey == pygame.K_KP_ENTER:
                break
            elif inkey != pygame.K_LCTRL or inkey != pygame.K_RCTRL:
                if not self._user_text_surface_size[0] >= self._max_size[0]:
                    if android is not None:
                        if inkey in ascii_filter:
                            if inkey in constants.K_ALL_KEYPAD_DIGITS:
                                inkey = numpad_digit_code2ascii(inkey)
                            self._user.append(chr(inkey))
                    else:
                        if inkey in constants.K_ALL_KEYPAD_DIGITS:
                            self._user.append(chr(numpad_digit_code2ascii(
                                inkey)))
                        elif string and ord(string) in ascii_filter:
                            self._user.append(string)
            self._update()
        got = "".join(self._user)
        if self._logging:
            expyriment._active_exp._event_file_log("TextInput,entered,{0}"
                                                   .format(unicode2byte(got)))
        if android_hide_keyboard is not None:
            android_hide_keyboard()
        return got


if __name__ == '__main__':
    from expyriment import control
    control.set_develop_mode(True)
    defaults.event_logging = 0
    exp = control.initialize()
    textinput = TextInput(message="Subject Number:",
                          message_colour=(160, 70, 250),
                          user_text_size=30,
                          user_text_colour=(255, 150, 50),
                          frame_colour=(70, 70, 70))
    print(textinput.get())
