#!/usr/bin/env python

"""
A Rectangle stimulus.

This module contains a class implementing a rectangle stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import pygame

from .. import _internals
from . import defaults
from ._visual import Visual


class Rectangle(Visual):
    """A class implementing a rectangle stimulus."""

    def __init__(self, size, colour=None, line_width=None,
                 corner_rounding=None, corner_anti_aliasing=None,
                 position=None):
        """Create a rectangle.

        Parameters
        ----------
        size : (int, int)
            size (width, height) of the rectangle
        colour : (int, int, int), optional
            colour of the rectangle
        line_width : int, optional
            line width in pixels; 0 will result in a filled rectangle,
            as does a value < 0 or >= min(size)
        corner_rounding : float or (float, float, float, float), optional
            radius of the corners in percent of 0.5 * min(size);
        corner_anti_aliasing : int, optional
            anti aliasing parameter for rounded corners
            (good anti_aliasing with 10)
        position : (int, int), optional
            position of the stimulus

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
            self._colour = _internals.active_exp.foreground_colour
        if line_width is None:
            line_width = defaults.rectangle_line_width
        elif line_width < 0 or line_width >= min(self._size):
            line_width = 0
        self._line_width = line_width
        if corner_rounding is None:
            corner_rounding = defaults.rectangle_corner_rounding
        elif corner_rounding < 0 or corner_rounding > 100:
            raise AttributeError("corner_rounding must be >= 0 and < 100!")
        self._corner_rounding = corner_rounding
        if corner_anti_aliasing is not None:
            self._corner_anti_aliasing = corner_anti_aliasing
        else:
            self._corner_anti_aliasing = defaults.rectangle_corner_anti_aliasing

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

    @property
    def corner_rounding(self):
        """Getter for corner_rounding."""
        return self._corner_rounding

    @corner_rounding.setter
    def corner_rounding(self, value):
        """Setter for corner_rounding."""

        if self.has_surface:
            raise AttributeError(Rectangle._getter_exception_message.format(
                "corner_rounding"))
        else:
            self._corner_rounding = value

    @property
    def corner_anti_aliasing(self):
        """Getter for corner_anti_aliasing."""
        return self._corner_anti_aliasing

    @corner_anti_aliasing.setter
    def corner_anti_aliasing(self, value):
        """Setter for corner_anti_aliasing."""

        if self.has_surface:
            raise AttributeError(Rectangle._getter_exception_message.format(
                "anti_aliasing"))
        else:
            self._anti_aliasing = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        def create_rounded_rectangle(rectangle_size, inverted=False):
            """Helper function to create (uncoloured) rounded rectangles."""

            if self._corner_anti_aliasing > 0:
                aa_scaling = (self._corner_anti_aliasing / 5.0) + 1
            else:
                aa_scaling = 1

            if inverted:
                scaled_size = [x * aa_scaling for x in rectangle_size]
                surface = pygame.surface.Surface(scaled_size,
                                             pygame.SRCALPHA).convert_alpha()
                rounding = self._corner_rounding * 0.5 * \
                           min(surface.get_size()) // 100
                size = [2 * rounding,
                        2 * rounding]
                tmp = pygame.surface.Surface(scaled_size)
                rect1 = pygame.surface.Surface(
                    (surface.get_size()[0] - 2 * rounding,
                     surface.get_size()[1]))
                rect2 = pygame.surface.Surface(
                    (surface.get_size()[0],
                     surface.get_size()[1] - 2 * rounding))
                tmp.fill((0, 0, 0))
                rect1.fill((255, 255, 255))
                rect2.fill((255, 255, 255))
                tmp.blit(rect1, (rounding, 0))
                tmp.blit(rect2, (0, rounding))
                circle = pygame.surface.Surface(
                    size)
                pygame.draw.ellipse(circle, (255, 255, 255),
                                    pygame.Rect((0, 0), size))
                tmp.blit(circle, (0, 0), special_flags=pygame.BLEND_RGB_MAX)
                tmp.blit(circle, (surface.get_size()[0] - rounding * 2, 0),
                         special_flags=pygame.BLEND_RGB_MAX)
                tmp.blit(circle, (0,
                                  surface.get_size()[1] - rounding * 2),
                         special_flags=pygame.BLEND_RGB_MAX)
                tmp.blit(circle, (surface.get_size()[0] - rounding * 2,
                                  surface.get_size()[1] - rounding * 2),
                         special_flags=pygame.BLEND_RGB_MAX)
                tmp.set_colorkey((255, 255, 255))
                surface.blit(tmp, (0, 0))

                if aa_scaling != 1:
                    surface = pygame.transform.smoothscale(
                        surface, (int(surface.get_size()[0] / aa_scaling),
                                  int(surface.get_size()[1] / aa_scaling)))

            else:
                surface = pygame.surface.Surface(
                    rectangle_size, pygame.SRCALPHA).convert_alpha()
                rounding = self._corner_rounding * 0.5 * min(surface.get_size()) // 100
                size = [(2 * rounding) * aa_scaling,
                        (2 * rounding) * aa_scaling]
                rect1 = pygame.surface.Surface(
                    (surface.get_size()[0] - 2 * rounding,
                     surface.get_size()[1]))
                rect2 = pygame.surface.Surface(
                    (surface.get_size()[0],
                     surface.get_size()[1] - 2 * rounding))
                rect1.fill((0, 0, 0))
                rect2.fill((0, 0, 0))
                surface.blit(rect1, (rounding, 0))
                surface.blit(rect2, (0, rounding))
                circle = pygame.surface.Surface(
                    size, pygame.SRCALPHA).convert_alpha()
                pygame.draw.ellipse(circle, (0, 0, 0),
                                    pygame.Rect((0, 0), size))

                if aa_scaling != 1:
                    circle = pygame.transform.smoothscale(
                        circle, (int(size[0] / aa_scaling),
                                 int(size[1] / aa_scaling)))

                surface.blit(circle, (0, 0))
                surface.blit(circle, (surface.get_size()[0] - rounding * 2,
                                      0))
                surface.blit(circle, (0,
                                      surface.get_size()[1] - rounding * 2))
                surface.blit(circle, (surface.get_size()[0] - rounding * 2,
                                      surface.get_size()[1] - rounding * 2))

            return surface

        if self._line_width == 0:
            if self._corner_rounding == 0:
                surface = pygame.surface.Surface(
                    self._size, pygame.SRCALPHA).convert_alpha()
                surface.fill(self._colour)
            else:
                surface = create_rounded_rectangle(self._size)
                surface.fill(self._colour, special_flags=pygame.BLEND_RGB_MAX)

        else:
            if self._line_width % 2 == 0:
                surface_size = [x + self._line_width for x in self._size]
                hole_size = [x - self._line_width for x in self._size]
            else:
                surface_size = [x + self._line_width - 1 for x in self._size]
                hole_size = [x - (self._line_width + 1) for x in self._size]
            surface = pygame.surface.Surface(
                surface_size,  #[x + self._line_width for x in self._size],
                pygame.SRCALPHA).convert_alpha()
            if self._corner_rounding == 0:
                surface.fill((0, 0, 0))
                hole = pygame.surface.Surface(
                    hole_size,  #[x - self._line_width for x in self._size],
                    pygame.SRCALPHA).convert_alpha()
                surface.blit(hole, (self._line_width, self._line_width),
                             special_flags=pygame.BLEND_RGBA_MIN)
                surface.fill(self._colour, special_flags=pygame.BLEND_RGB_MAX)
            else:
                surface = create_rounded_rectangle(
                    surface_size)  #[x + self._line_width for x in self._size])
                hole = create_rounded_rectangle(
                    hole_size,  #[x - self._line_width for x in self._size],
                    inverted=True)
                surface.blit(hole, (self._line_width, self._line_width),
                             special_flags=pygame.BLEND_RGBA_MIN)
                surface.fill(self._colour, special_flags=pygame.BLEND_RGB_MAX)

        return surface

    def is_point_inside(self, point_xy):
        """"OBSOLETE METHOD: Please use 'overlapping_with_position'."""

        raise DeprecationWarning("is_point_inside is an obsolete method. Please use overlapping_with_position")

    @staticmethod
    def _demo(exp=None):
        if exp is None:
            from .. import control
            control.set_develop_mode(True)
            control.defaults.event_logging = 0
            exp_ = control.initialize()
        rect = Rectangle((20, 200), colour=(255, 0, 255))
        rect.present()
        if exp is None:
            exp_.clock.wait(1000)
