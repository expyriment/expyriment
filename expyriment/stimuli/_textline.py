"""
A text line stimulus.

This module contains a class implementing a text line stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import os

import pygame

from . import defaults
from ._visual import Visual
from ..misc import find_font, byte2unicode
from .. import _internals


# Keep track of open file handles and previously loaded font objects
open_filehandles = []
fonts = {}


class TextLine(Visual):
    """A class implementing a single text line."""

    def __init__(self, text, position=None, text_font=None, text_size=None,
                 text_bold=None, text_italic=None, text_underline=None,
                 text_colour=None, background_colour=None, max_width=None):
        """Create a text line stimulus.

        NOTE: text_font can be both, a name or path to a font file!
        When text_font is a name, Expyriment will try to find a font that
        best matches the given name.
        If no matching font can be found, or if the given font file cannot be
        found, the Pygame system default will be used.
        In any case the value of the attribute text_font will always
        resemble the font that is actually in use!

        Parameters
        ----------
        text : str
            text to show (str)
        position : (int, int), optional
            position of the stimulus
        text_font : str, optional
            font to use as name or as path to a font file
        text_size : int, optional
            text size
        text_bold : bool, optional
            font should be bold
        text_italic : bool, optional
            font should be italic
        text_underline : bool, optional
            font should get an underline
        text_colour : (int, int, int), optional
            text colour
        background_colour : (int, int, int), optional
            background colour
        max_width: int, optional
            maximum surface width of the text line stimulus
            if this parameter is defined, text lines that exceed this
            surface width will be trimmed (indicated by a '~' as last letter)

        """

        pygame.font.init()
        if position is None:
            position = defaults.textline_position
        Visual.__init__(self, position, log_comment=text)
        self._text = text
        self._max_width = max_width
        if text_size is None:
            text_size = defaults.textline_text_size
        if text_size is not None:
            self._text_size = text_size
        else:
            self._text_size = _internals.active_exp.text_size
        if text_font is None:
            text_font = defaults.textline_text_font
        if text_font is None:
            text_font = _internals.active_exp.text_font
        if text_font is None:
            text_font = "FreeSans"
        self._text_font = find_font(text_font)
        try:
            with open(self._text_font, 'rb') as f:
                pygame.font.Font(f, 10)
        except Exception:
            raise OSError("Font '{0}' not found!".format(text_font))
        if text_bold is not None:
            self._text_bold = text_bold
        else:
            self._text_bold = defaults.textline_text_bold
        if text_italic is not None:
            self._text_italic = text_italic
        else:
            self._text_italic = defaults.textline_text_italic
        if text_underline is not None:
            self._text_underline = text_underline
        else:
            self._text_underline = defaults.textline_text_underline
        if text_colour is None:
            text_colour = defaults.textline_text_colour
        if text_colour is not None:
            self._text_colour = text_colour
        else:
            self._text_colour = _internals.active_exp.foreground_colour
        if background_colour is not None:
            self._background_colour = background_colour
        else:
            self._background_colour = \
                defaults.textline_background_colour

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def text(self):
        """Getter for text."""

        return self._text

    @text.setter
    def text(self, value):
        """Setter for text."""

        if self.has_surface:
            raise AttributeError(TextLine._getter_exception_message.format(
                "text"))
        else:
            self._text = value

    @property
    def text_font(self):
        """Getter for text_font."""

        return self._text_font

    @text_font.setter
    def text_font(self, value):
        """Setter for text_font."""

        if self.has_surface:
            raise AttributeError(TextLine._getter_exception_message.format(
                "text_font"))
        else:
            self._text_font = value

    @property
    def text_size(self):
        """Getter for text_size."""

        return self._text_size

    @text_size.setter
    def text_size(self, value):
        """Setter for text_size."""

        if self.has_surface:
            raise AttributeError(TextLine._getter_exception_message.format(
                "text_size"))
        else:
            self._text_size = value

    @property
    def text_bold(self):
        """Getter for text_bold."""

        return self._text_bold

    @text_bold.setter
    def text_bold(self, value):
        """Setter for text_bold."""

        if self.has_surface:
            raise AttributeError(TextLine._getter_exception_message.format(
                "text_bold"))
        else:
            self._text_bold = value

    @property
    def text_italic(self):
        """Getter for text_italic."""

        return self._text_italic

    @text_italic.setter
    def text_italic(self, value):
        """Setter for text_italic."""

        if self.has_surface:
            raise AttributeError(TextLine._getter_exception_message.format(
                "text_italic"))
        else:
            self._text_italic = value

    @property
    def text_underline(self):
        """Getter for text_underline."""

        return self._text_underline

    @text_underline.setter
    def text_underline(self, value):
        """Setter for text_underline."""

        if self.has_surface:
            raise AttributeError(TextLine._getter_exception_message.format(
                "text_underline"))
        else:
            self._text_underline = value

    @property
    def text_colour(self):
        """Getter for text_colour."""

        return self._text_colour

    @text_colour.setter
    def text_colour(self, value):
        """Setter for text_colour."""

        if self.has_surface:
            raise AttributeError(TextLine._getter_exception_message.format(
                "text_colour"))
        else:
            self._text_colour = value

    @property
    def background_colour(self):
        """Getter for background_colour."""

        return self._background_colour

    @background_colour.setter
    def background_colour(self, value):
        """Setter for background_colour."""

        if self.has_surface:
            raise AttributeError(TextLine._getter_exception_message.format(
                "background_colour"))
        else:
            self._background_colour = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        # Due to a bug in handling file names in PyGame 1.9.2, we pass a file
        # handle to PyGame. See also:
        # https://github.com/expyriment/expyriment/issues/81
        if os.path.isfile(self._text_font):
            # We preserve previously created fonts, so that we don't open the
            # same font over and over again.
            if (self._text_font, self._text_size) in fonts:
                _font = fonts[(self._text_font, self._text_size)]
            else:
                f = open(self._text_font, 'rb')
                open_filehandles.append(f)
                _font = pygame.font.Font(f, self._text_size)
                fonts[(self._text_font, self._text_size)] = _font
        else:
            _font = pygame.font.Font(self._text_font, self._text_size)

        _font.set_bold(self.text_bold)
        _font.set_italic(self.text_italic)
        _font.set_underline(self.text_underline)
        if not isinstance(self.text, str):
            # Pygame wants latin-1 encoding here for character strings
            _text = byte2unicode(self.text).encode('latin-1')
        else:
            _text = self.text
        if self.background_colour:
            surface = _font.render(_text, True, self.text_colour,
                                   self.background_colour)
        else:
            surface = _font.render(_text, True, self.text_colour)
        surface = surface.convert_alpha()

        if self._max_width is not None and self._max_width > 0 and surface.get_size()[0] > self._max_width:
            # trim too long text lines
            self._text = self._text[:-2] + "~"
            surface = self._create_surface() # recursion

        return surface


    @staticmethod
    def _demo(exp=None):
        if exp is None:
            from .. import control
            control.set_develop_mode(True)
            control.defaults.event_logging = 0
            exp_ = control.initialize()
        textline = TextLine("abcde fghijk lmnopqrstuvwxyz 12 348 56789",
                            text_font="Helvetica",
                            text_size=20, text_bold=False)
        textline.present()
        if exp is None:
            exp_.clock.wait(1000)
