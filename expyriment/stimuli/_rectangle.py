#!/usr/bin/env python

"""
A Rectangle stimulus.

This module contains a class implementing a rectangle stimulus.

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


class Rectangle(Visual):
    """A class implementing a rectangle stimulus."""

    def __init__(self, size, colour=None, line_width=None, position=None):
        """Create a rectangle.

        Parameters
        ----------
        size : (int, int)
            size (width, height) of the rectangle
        line_width : int, optional
            line width in pixels; 0 will result in a filled rectangle,
            as does a value < 0 or >= min(size)
        position : (int, int), optional
            position of the stimulus
        colour : (int, int, int), optional
            colour of the rectangle

        """

        if position is None:
            position = defaults.rectangle_position
        Visual.__init__(self, position=position)
        self._size = size
        if colour is None:
            colour = defaults.rectangle_colour
        if colour is not None:
            self._colour = colour
        else:
            self._colour = expyriment._active_exp.foreground_colour
        if line_width is None:
            line_width = defaults.rectangle_line_width
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
            raise AttributeError(Rectangle._getter_exception_message.format(
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
            raise AttributeError(Rectangle._getter_exception_message.format(
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
            raise AttributeError(Rectangle._getter_exception_message.format(
                "line_width"))
        else:
            self._line_width = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        if self._line_width == 0:
            surface = pygame.surface.Surface(self._size,
                                         pygame.SRCALPHA).convert_alpha()
            surface.fill(self._colour)

        else:
            # Invert colours and use it as colourkey for a temporal surface,
            # fill the surface and draw a smaller rectangle with colourkey
            # colour
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
            pygame.draw.rect(tmp, self._colour, pygame.Rect(
                (0, 0), [x + self._line_width for x in self._size]))
            pygame.draw.rect(tmp, colour, pygame.Rect(
                (self._line_width, self._line_width),
                [x - self._line_width for x in self._size]))
            surface.blit(tmp, (0, 0))

        return surface

    def is_point_inside(self, point_xy):
        """"DEPRECATED METHOD: Please use 'overlapping_with_position'."""

        return self.overlapping_with_position(point_xy)

if __name__ == "__main__":
    from expyriment import control, design
    control.set_develop_mode(True)
    exp = design.Experiment(log_level=0)
    control.initialize(exp)
    rect = Rectangle((20, 200), colour=(255, 0, 255))
    rect.present()
    exp.clock.wait(1000)
