#!/usr/bin/env python

"""
A text screen stimulus.

This module contains a class implementing a text screen stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import pygame

from . import defaults
from ._stimulus import Stimulus
from ._visual import Visual
from ._textline import TextLine
from ._textbox import TextBox
from ..misc import find_font, unicode2byte
from .. import _internals


class TextScreen(Visual):
    """A class implementing a screen with heading and text."""

    def __init__(self, heading, text, position=None, heading_font=None,
                 heading_size=None, heading_bold=None, heading_italic=None,
                 heading_underline=None, heading_colour=None, text_font=None,
                 text_size=None, text_bold=None, text_italic=None,
                 text_underline=None, text_colour=None,
                 text_justification=None, background_colour=None, size=None):
        """Create a text screen.

        Parameters
        ----------
        heading : str
            heading of the text screen
        text : str
            text of the text screen
        position : (int, int), optional
            position of the stimulus
        heading_font : str, optional
            heading font to use
        heading_size : int, optional
            heading font size
        heading_bold : bool, optional
            heading should be bold
        heading_italic : bool, optional
            heading should be italic
        heading_underline : bool, optional
            heading should get an underline
        heading_colour : (int,int,int), optional
            heding colour
        text_font : str, optional
            text font to use
        text_size : int, optional
            text font size
        text_bold : bool, optional
            text should be bold
        text_italic : bool, optional
            text should be italic
        text_underline : bool, optional
            text should get an underline
        text_colour : (int,int,int), optional
            text colour
        text_justification : int, optional
            0 (Left), 1(center), 2(right) (int) (optional)
        background_colour : (int, int, int), optional
            background_colour
        size : (int, int), optional
            size of the text screen

        """

        if position is None:
            position = defaults.textscreen_position
        Visual.__init__(self, position, log_comment="text_screen")
        self._heading = heading
        self._text = text
        if heading_font is None:
            heading_font = defaults.textscreen_heading_font
        if heading_font is None:
            heading_font = _internals.active_exp.text_font
        if heading_font is None:
            heading_font = "FreeSans"
        self._heading_font = find_font(heading_font)
        try:
            with open(self._heading_font, 'rb') as f:
                pygame.font.Font(f, 10)
        except Exception:
            raise IOError("Font '{0}' not found!".format(heading_font))
        if heading_size is None:
            heading_size = defaults.textscreen_heading_size
        if heading_size:
            self._heading_size = heading_size
        else:
            self._heading_size = int(_internals.active_exp.text_size
                                     * 1.2)
        if heading_bold is not None:
            self._heading_bold = heading_bold
        else:
            self._heading_bold = defaults.textscreen_heading_bold
        if heading_italic is not None:
            self._heading_italic = heading_italic
        else:
            self._heading_italic = \
                defaults.textscreen_heading_italic
        if heading_underline is not None:
            self._heading_underline = heading_underline
        else:
            self._heading_underline = \
                defaults.textscreen_heading_underline
        if heading_colour is None:
            heading_colour = defaults.textscreen_heading_colour
        if heading_colour is not None:
            self._heading_colour = heading_colour
        else:
            self._heading_colour = _internals.active_exp.foreground_colour
        if text_font is None:
            text_font = defaults.textscreen_text_font
        if text_font is not None:
            self._text_font = find_font(text_font)
        else:
            self._text_font = find_font(_internals.active_exp.text_font)
        try:
            with open(self._text_font, 'rb') as f:
                pygame.font.Font(f, 10)
        except Exception:
            raise IOError("Font '{0}' not found!".format(text_font))
        if text_size is None:
            self._text_size = defaults.textscreen_text_size
        if text_size is not None:
            self._text_size = text_size
        else:
            self._text_size = _internals.active_exp.text_size
        if text_bold is not None:
            self._text_bold = text_bold
        else:
            self._text_bold = defaults.textscreen_text_bold
        if text_italic is not None:
            self._text_italic = text_italic
        else:
            self._text_italic = defaults.textscreen_text_italic
        if text_underline is not None:
            self._text_underline = text_underline
        else:
            self._text_underline = defaults.textscreen_text_underline
        if text_colour is None:
            text_colour = defaults.textscreen_text_colour
        if text_colour is not None:
            self._text_colour = text_colour
        else:
            self._text_colour = _internals.active_exp.foreground_colour
        if text_justification is not None:
            self._text_justification = text_justification
        else:
            self._text_justification = \
                defaults.textscreen_text_justification
        if size is not None:
            self._size = size
        else:
            size = defaults.textscreen_size
            if size is None:
                try:
                    self._size = (
                        _internals.active_exp.screen.surface.get_size()[0] -
                        _internals.active_exp.screen.surface.get_size()[0]
                        // 5,
                        _internals.active_exp.screen.surface.get_size()[1] -
                        _internals.active_exp.screen.surface.get_size()[1]
                        // 5)
                except Exception:
                    raise RuntimeError("Cannot get size of screen!")

        if background_colour is not None:
            self._background_colour = background_colour
        else:
            self._background_colour = \
                defaults.textscreen_background_colour

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def heading(self):
        """Getter for heading."""

        return self._heading

    @heading.setter
    def heading(self, value):
        """Setter for heading."""

        if self.has_surface:
            raise AttributeError(TextScreen._getter_exception_message.format(
                "heading"))
        else:
            self._heading = value

    @property
    def text(self):
        """Getter for text."""

        return self._text

    @text.setter
    def text(self, value):
        """Setter for text."""

        if self.has_surface:
            raise AttributeError(TextScreen._getter_exception_message.format(
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
            raise AttributeError(TextScreen._getter_exception_message.format(
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
            raise AttributeError(TextScreen._getter_exception_message.format(
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
            raise AttributeError(TextScreen._getter_exception_message.format(
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
            raise AttributeError(TextScreen._getter_exception_message.format(
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
            raise AttributeError(TextScreen._getter_exception_message.format(
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
            raise AttributeError(TextScreen._getter_exception_message.format(
                "text_colour"))
        else:
            self._text_colour = value

    @property
    def heading_font(self):
        """Getter for heading_font."""

        return self._heading_font

    @heading_font.setter
    def heading_font(self, value):
        """Setter for heading_font."""

        if self.has_surface:
            raise AttributeError(TextScreen._getter_exception_message.format(
                "heading_font"))
        else:
            self._heading_font = value

    @property
    def heading_size(self):
        """Getter for heading_size."""

        return self._heading_size

    @heading_size.setter
    def heading_size(self, value):
        """Setter for heading_size."""

        if self.has_surface:
            raise AttributeError(TextScreen._getter_exception_message.format(
                "heading_size"))
        else:
            self._heading_size = value

    @property
    def heading_bold(self):
        """Getter for heading_bold."""

        return self._heading_bold

    @heading_bold.setter
    def heading_bold(self, value):
        """Setter for heading_bold."""

        if self.has_surface:
            raise AttributeError(TextScreen._getter_exception_message.format(
                "heading_bold"))
        else:
            self._heading_bold = value

    @property
    def heading_italic(self):
        """Getter for heading_italic."""

        return self._heading_italic

    @heading_italic.setter
    def heading_italic(self, value):
        """Setter for heading_italic."""

        if self.has_surface:
            raise AttributeError(TextScreen._getter_exception_message.format(
                "heading_italic"))
        else:
            self._heading_italic = value

    @property
    def heading_underline(self):
        """Getter for heading_underline."""

        return self._heading_underline

    @heading_underline.setter
    def heading_underline(self, value):
        """Setter for heading_underline."""

        if self.has_surface:
            raise AttributeError(TextScreen._getter_exception_message.format(
                "heading_underline"))
        else:
            self._heading_underline = value

    @property
    def heading_colour(self):
        """Getter for heading_colour."""

        return self._heading_colour

    @heading_colour.setter
    def heading_colour(self, value):
        """Setter for heading_colour."""

        if self.has_surface:
            raise AttributeError(TextScreen._getter_exception_message.format(
                "heading_colour"))
        else:
            self._heading_colour = value

    @property
    def background_colour(self):
        """Getter for background_colour."""

        return self._background_colour

    @background_colour.setter
    def background_colour(self, value):
        """Setter for background_colour."""

        if self.has_surface:
            raise AttributeError(TextScreen._getter_exception_message.format(
                "background_colour"))
        else:
            self._background_colour = value

    @property
    def size(self):
        """Getter for size."""

        return self._size

    @size.setter
    def size(self, value):
        """Setter for size."""

        if self.has_surface:
            raise AttributeError(TextScreen._getter_exception_message.format(
                "size"))
        else:
            self._size = value

    @property
    def text_justification(self):
        """Getter for text_justification."""

        return self._text_justification

    @text_justification.setter
    def text_justification(self, value):
        """Setter for text_justification."""

        if self.has_surface:
            raise AttributeError(TextScreen._getter_exception_message.format(
                "text_justification"))
        else:
            self._text_justification = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        surface = pygame.surface.Surface(self.size,
                                         pygame.SRCALPHA).convert_alpha()
        if self.background_colour is not None:
            surface.fill(self.background_colour)
        header = TextLine(text=self.heading, text_size=self.heading_size,
                          text_colour=self.heading_colour,
                          background_colour=self.background_colour,
                          text_font=self.heading_font,
                          text_bold=self.heading_bold,
                          text_italic=self.heading_italic,
                          text_underline=self.heading_underline)
        Stimulus._id_counter -= 1
        box = TextBox(text=self.text, text_font=self.text_font,
                      text_size=self.text_size, text_bold=self.text_bold,
                      text_italic=self.text_italic,
                      text_underline=self.text_underline,
                      text_colour=self.text_colour,
                      background_colour=self.background_colour,
                      size=(self.size[0], self.size[1] - self.size[1] // 5),
                      text_justification=self.text_justification)
        Stimulus._id_counter -= 1
        surface.blit(header._get_surface(),
                     (self.size[0] // 2 - header.surface_size[0] // 2,
                      0))
        surface.blit(box._get_surface(),
                     (self.size[0] // 2 - box.size[0] // 2, self.size[1] // 5))
        return surface

    @staticmethod
    def _demo(exp=None):
        if exp is None:
            from .. import control
            control.set_develop_mode(True)
            control.defaults.event_logging = 0
            exp_ = control.initialize()
        textscreen = TextScreen("Hello World",
                                "Line one.\nLine two.\nLine three.")
        textscreen.present()
        if exp is None:
            exp_.clock.wait(1000)
