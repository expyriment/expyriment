#!/usr/bin/env python

"""
An ellipse stimulus.

This module contains a class implementing an ellipse stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import pygame

import defaults
from _visual import Visual
import expyriment


class Ellipse(Visual):
    """A class implementing a basic 2D ellipse."""

    def __init__(self, size, colour=None, line_width=None, position=None):
        """Create an ellipse.

        Parameters
        ----------
        size : (int, int)
            size of the ellipse (major and minor axis)
        colour : (int, int, int), optional
            colour of the ellipse
        line_width : int, optional
            line width in pixels; 0 will result in a filled ellipse
            (as does a value < 0 or >= min(size))
        position : (int, int), optional
            position of the stimulus

        """

        if position is None:
            position = defaults.circle_position
        Visual.__init__(self, position)
        self._size = size
        if colour is None:
            colour = defaults.circle_colour
        if colour is not None:
            self._colour = colour
        else:
            self._colour = expyriment._active_exp.foreground_colour
        if line_width is None:
            line_width = defaults.circle_line_width
        elif line_width < 0 or line_width >= min(self._size):
            line_width = 0
        self._line_width = line_width

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def size(self):
        """Getter for size."""
        return self._size

    @size.setter
    def size(self, value):
        """Setter for size."""

        if self.has_surface:
            raise AttributeError(Ellipse._getter_exception_message.format(
                "size"))
        else:
            self._size = value

    @property
    def colour(self):
        """Getter for colour."""
        return self._colour

    @colour.setter
    def colour(self, value):
        """Setter for colour."""

        if self.has_surface:
            raise AttributeError(Ellipse._getter_exception_message.format(
                "colour"))
        else:
            self._colour = value

    @property
    def line_width(self):
        """Getter for line_width."""
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        """Setter for line_width."""

        if self.has_surface:
            raise AttributeError(Ellipse._getter_exception_message.format(
                "line_width"))
        else:
            self._line_width = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        if self._line_width == 0:
            surface = pygame.surface.Surface(
                self._size, pygame.SRCALPHA).convert_alpha()
            pygame.draw.ellipse(surface, self._colour, pygame.Rect(
                (0, 0), self._size))

        else:
            # Invert colours and use it as colourkey for a temporal surface,
            # fill the surface and draw a smaller ellipse with colourkey colour
            colour = [abs(self._colour[0] - 255),
                      abs(self._colour[1] - 255),
                      abs(self._colour[2] - 255)]
            surface = pygame.surface.Surface(
                [x + self._line_width for x in self._size],
                pygame.SRCALPHA).convert_alpha()
            tmp = pygame.surface.Surface(
                [x + self._line_width for x in self._size]).convert()
            tmp.set_colorkey(colour)
            tmp.fill(colour)
            pygame.draw.ellipse(tmp, self._colour, pygame.Rect(
                (0, 0), [x + self._line_width for x in self._size]))
            pygame.draw.ellipse(tmp, colour, pygame.Rect(
                (self._line_width, self._line_width),
                [x - self._line_width for x in self._size]))
            surface.blit(tmp, (0, 0))

        return surface


if __name__ == "__main__":
    from expyriment import control
    control.set_develop_mode(True)
    defaults.event_logging = 0
    exp = control.initialize()
    ellipse = Ellipse(size=[200, 100])
    ellipse.present()
    exp.clock.wait(1000)
