#!/usr/bin/env python

"""
A text box stimulus.

This module contains a class implementing a text box stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import os
import re

import pygame

from . import defaults
from .. import _active
from ..misc import find_font, unicode2byte, byte2unicode
from ._visual import Visual


class TextBox(Visual):
    """A class implementing a text box with wrapped text.

    This wraps a given multiline string into a formatted mutliline text box,
    strips of leading and trailing lines and gets rid of additional
    whitespaces at beginning of lines (indentation).

    """

    def __init__(self, text, size, position=None, text_font=None,
                 text_size=None, text_bold=None, text_italic=None,
                 text_underline=None, text_justification=None,
                 text_colour=None, background_colour=None,
                 do_not_trim_words=None):
        """Create a text box.

        Notes
        -----
        text_font can be both, a name or path to a font file!
        When text_font is a name, Expyriment will try to find a font that
        best matches the given name.
        If no matching font can be found, or if the given font file cannot be
        found, the Pygame system default will be used.
        In any case the value of the attribute text_font will always
        resemble the font that is actually in use!

        Parameters
        ----------
        text : str
            text to wrap
        size : (int, int)
            size of the text box
        position : (int, int), optional
            position of the stimulus
        text_font : str, optional
            text font to use as a name or as a path to a font file
        text_size : int, optional
            size of the text
        text_bold : bool, optional
            font should be bold
        text_italic : bool, optional
            font should be italic
        text_underline : bool, optional
            font should get an underline
        text_justification : int, optional
            text justification, 0 (left), 1 (center), 2 (right)
        text_colour : (int, int, int), optional
            colour of the text
        background_colour : (int, int, int), optional
            background colour
        do_not_trim_words: bool, optional
            if True, words that exceed the width of the text box
            will be not be trimmed and an exception is raise instead.
            default: False

        """

        pygame.font.init()

        if position is None:
            position = defaults.textbox_position
        Visual.__init__(self, position)
        self._text = text
        self._size = size
        if text_size is None:
            text_size = defaults.textbox_text_size
        if text_size is not None:
            self._text_size = text_size
        else:
            self._text_size = _active.exp.text_size

        if text_font is None:
            text_font = defaults.textbox_text_font
        if text_font is not None:
            self._text_font = find_font(text_font)
        else:
            self._text_font = find_font(_active.exp.text_font)
        try:
            _font = pygame.font.Font(unicode2byte(self._text_font, fse=True),
                                     10)
            _font = None
        except:
            raise IOError("Font '{0}' not found!".format(text_font))
        if text_bold is not None:
            self._text_bold = text_bold
        else:
            self._text_bold = defaults.textbox_text_bold
        if text_italic is not None:
            self._text_italic = text_italic
        else:
            self._text_italic = defaults.textbox_text_italic
        if text_underline is not None:
            self._text_underline = text_underline
        else:
            self._text_underline = defaults.textbox_text_underline
        if text_justification is not None:
            self._text_justification = text_justification
        else:
            self._text_justification = defaults.textbox_text_justification
        if text_colour is not None:
            self._text_colour = text_colour
        else:
            if defaults.textbox_text_colour is not None:
                self._text_colour = defaults.textbox_text_colour
            else:
                self._text_colour = _active.exp.foreground_colour
        if background_colour is not None:
            self._background_colour = background_colour
        else:
            self._background_colour = \
                defaults.textbox_background_colour
        if do_not_trim_words is not None:
            self._do_not_trim_words = do_not_trim_words
        else:
            self._do_not_trim_words = defaults.textbox_do_not_trim_words


    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def text(self):
        """Getter for text."""

        return self._text

    @text.setter
    def text(self, value):
        """Setter for text."""

        if self.has_surface:
            raise AttributeError(TextBox._getter_exception_message.format(
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
            raise AttributeError(TextBox._getter_exception_message.format(
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
            raise AttributeError(TextBox._getter_exception_message.format(
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
            raise AttributeError(TextBox._getter_exception_message.format(
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
            raise AttributeError(TextBox._getter_exception_message.format(
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
            raise AttributeError(TextBox._getter_exception_message.format(
                "text_underline"))
        else:
            self._text_underline = value

    @property
    def text_justification(self):
        """Getter for text_justification."""

        return self._text_justification

    @text_justification.setter
    def text_justification(self, value):
        """Setter for text_justification."""

        if self.has_surface:
            raise AttributeError(TextBox._getter_exception_message.format(
                "text_justification"))
        else:
            self._text_justification = value

    @property
    def text_colour(self):
        """Getter for text_colour."""

        return self._text_colour

    @text_colour.setter
    def text_colour(self, value):
        """Setter for text_colour."""

        if self.has_surface:
            raise AttributeError(TextBox._getter_exception_message.format(
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
            raise AttributeError(TextBox._getter_exception_message.format(
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
            raise AttributeError(TextBox._getter_exception_message.format(
                "size"))
        else:
            self._size = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        rect = pygame.Rect((0, 0), self.size)

        if os.path.isfile(self._text_font):
            _font = pygame.font.Font(unicode2byte(self._text_font, fse=True),
                                     self._text_size)
        else:
            _font = pygame.font.Font(self._text_font, self._text_size)

        _font.set_bold(self.text_bold)
        _font.set_italic(self.text_italic)
        _font.set_underline(self.text_underline)

        if type(self.text) is not str:
            # Pygame wants latin-1 encoding here for character strings
            _text = byte2unicode(self.text).encode('latin-1')
        else:
            _text = self.text
        surface = self.render_textrect(self.format_block(_text),
                                       _font, rect, self.text_colour,
                                       self.background_colour,
                                       self.text_justification)
        return surface

    # The following code is taken from the word-wrapped text display module by
    # David Clark (http://www.pygame.org/pcr/text_rect/index.php).
    def render_textrect(self, string, font, rect, text_colour,
                        background_colour, justification=0):
        """Return a surface with reformatted string.

        The given text string is reformatted to fit within the given rect,
        word-wrapping as necessary. The text will be anti-aliased.
        Returns a surface.

        Parameters
        ----------
        string : str
            text you wish to render, '\n' begins a new line
        font : pygame.Font object, optional
            Font object
        rect : bool
            rectstyle giving the size of requested surface
        text_colour : (int, int, int)
            text colour
        background_colour : (int, int, int)
            background colour
        justification : int, optional
            0 (Left), 1 (center), 2 (right) (int) (default = 0)

        """

        final_lines = []
        requested_lines = string.splitlines()

        # Create a series of lines that will fit on the provided
        # rect.
        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width:
                # Start a new line
                accumulated_line = ""
                for word in requested_line.split(' '):
                    if not self._do_not_trim_words:
                        while font.size(word)[0] >= rect.width:
                            word = word[:-2] + '~'
                    elif font.size(word)[0] >= rect.width:
                            raise Exception("The word " + word +
                                " is too long to fit in the rect passed.")

                    if len(accumulated_line) > 0:
                        test_line = accumulated_line + " " + word
                    else:
                        test_line = word

                    # Build the line if the words fit.
                    if font.size(test_line)[0] < rect.width:
                        accumulated_line = test_line
                    else:
                        if len(accumulated_line) > 0:
                            final_lines.append(accumulated_line)
                        accumulated_line = word

                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)

        # Let's try to write the text out on the surface.
        surface = pygame.surface.Surface(rect.size,
                                         pygame.SRCALPHA).convert_alpha()
        if background_colour is not None:
            surface.fill(background_colour)
        accumulated_height = 0
        for line in final_lines:
            # Changed from >= which led to crashes sometimes!
            if accumulated_height + font.size(line)[1] > rect.height:
                raise Exception(
                    "Once word-wrapped," +
                    "the text string was too tall to fit in the rect.")
            if line != "":
                tempsurface = font.render(line, 1, text_colour)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface,
                                 ((rect.width - tempsurface.get_width()) // 2,
                                  accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface,
                                 (rect.width - tempsurface.get_width(),
                                  accumulated_height))
                else:
                    raise Exception("Invalid justification argument: " +
                                    str(justification))
            accumulated_height += font.size(line)[1]
        return surface

    def format_block(self, block):
        """Format the given block of text.

        This function is trimming leading and trailing
        empty lines and any leading whitespace that is common to all lines.

        Parameters
        ----------
        block : str
            block of text to be formatted

        """

        # Separate block into lines
        #lines = str(block).split('\n')
        lines = block.split('\n')

        # Remove leading/trailing empty lines
        while lines and not lines[0]:
            del lines[0]
        while lines and not lines[-1]:
            del lines[-1]

        # Look at first line to see how much indentation to trim
        try:
            ws = re.match(r'\s*', lines[0]).group(0)
        except:
            ws = None
        if ws:
            lines = [x.replace(ws, '', 1) for x in lines]

        # Remove leading/trailing blank lines (after leading ws removal)
        # We do this again in case there were pure-whitespace lines
        while lines and not lines[0]:
            del lines[0]
        while lines and not lines[-1]:
            del lines[-1]
        return '\n'.join(lines) + '\n'
    # End of code taken from the word-wrapped text display module


if __name__ == "__main__":
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    textbox = TextBox("Line one.\nLine two.\nLine three.", size=(100, 100))
    textbox.present()
    exp.clock.wait(1000)
