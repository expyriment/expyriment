#!/usr/bin/env python

"""
An ellipse stimulus.

This module contains a class implementing an ellipse stimulus.

"""
from __future__ import absolute_import

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import pygame

from . import defaults
from ._visual import Visual
import expyriment


class Ellipse(Visual):
    """A class implementing a basic 2D ellipse."""

    def __init__(self, radii, colour=None, line_width=None, position=None,
                 anti_aliasing=None):
        """Create an ellipse.

        Parameters
        ----------
        radii : (int, int)
            major and minor radii of the ellipse
        colour : (int, int, int), optional
            colour of the ellipse
        line_width : int, optional
            line width in pixels; 0 will result in a filled ellipse
            (as does a value < 0 or >= min(size))
        position : (int, int), optional
            position of the stimulus
        anti_aliasing : int, optional
            anti aliasing parameter (good anti_aliasing with 10)

        """

        if position is None:
            position = defaults.ellipse_position
        Visual.__init__(self, position)
        self._radii = radii
        self._size = [x * 2 for x in radii]
        if colour is None:
            colour = defaults.ellipse_colour
        if colour is not None:
            self._colour = colour
        else:
            self._colour = expyriment._active_exp.foreground_colour
        if line_width is None:
            line_width = defaults.ellipse_line_width
        elif line_width < 0 or line_width >= min(self._size):
            line_width = 0
        self._line_width = line_width
        if anti_aliasing is not None:
            self._anti_aliasing = anti_aliasing
        else:
            self._anti_aliasing = defaults.ellipse_anti_aliasing

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def radii(self):
        """Getter for radii."""
        return self._radii

    @radii.setter
    def radii(self, value):
        """Setter for radii."""

        if self.has_surface:
            raise AttributeError(Ellipse._getter_exception_message.format(
                "radii"))
        else:
            self._radii = value

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

    @property
    def anti_aliasing(self):
        """Getter for anti_aliasing."""

        return self._anti_aliasing

    @anti_aliasing.setter
    def anti_aliasing(self, value):
        """Setter for anti_aliasing."""

        if self.has_surface:
            raise AttributeError(Ellipse._getter_exception_message.format(
                "anti_aliasing"))
        self._anti_aliasing = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        if self._anti_aliasing > 0:
            aa_scaling = (self._anti_aliasing / 5.0) + 1
        else:
            aa_scaling = 1

        size = [(self._size[0]) * aa_scaling,
                (self._size[1]) * aa_scaling]

        if self._line_width == 0:
            surface = pygame.surface.Surface(
                size, pygame.SRCALPHA).convert_alpha()
            pygame.draw.ellipse(surface, (0, 0, 0), pygame.Rect(
                (0, 0), size))
            if aa_scaling != 1:
                surface = pygame.transform.smoothscale(surface,
                                (int(size[0] / aa_scaling),
                                 int(size[1] / aa_scaling)))
            surface.fill(self._colour, special_flags=pygame.BLEND_RGB_MAX)

        else:
            line_width = self._line_width * aa_scaling
            surface = pygame.surface.Surface(
                [x + line_width for x in size],
                pygame.SRCALPHA).convert_alpha()
            pygame.draw.ellipse(surface, (0, 0, 0), pygame.Rect(
                (0, 0),
                [x + line_width for x in size]))
            tmp = pygame.surface.Surface(
                [x - line_width for x in size])
            hole = pygame.surface.Surface(
                [x - line_width for x in size],
                pygame.SRCALPHA).convert_alpha()
            tmp.fill([0, 0, 0])
            pygame.draw.ellipse(tmp, (255, 255, 255), pygame.Rect(
                (0, 0), [x - line_width for x in size]))
            tmp.set_colorkey([255, 255, 255])
            hole.blit(tmp, (0, 0))
            surface.blit(hole, (line_width, line_width),
                         special_flags=pygame.BLEND_RGBA_MIN)
            if aa_scaling != 1:
                surface = pygame.transform.smoothscale(surface,
                                (int((size[0] + line_width) / aa_scaling),
                                 int((size[1] + line_width) / aa_scaling)))
            surface.fill(self._colour, special_flags=pygame.BLEND_RGB_MAX)

        return surface


if __name__ == "__main__":
    from expyriment import control
    control.set_develop_mode(True)
    defaults.event_logging = 0
    exp = control.initialize()
    ellipse = Ellipse(radii=[200, 100], anti_aliasing=10)
    ellipse.present()
    exp.clock.wait(1000)
