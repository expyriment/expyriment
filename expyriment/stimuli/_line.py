#!/usr/bin/env python

"""
A Line stimulus.

This module contains a class implementing a line stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import math

import pygame

from . import defaults
from ._visual import Visual
from .. import _internals
from .. import misc
from ..misc._timer import get_time


class Line(Visual):
    """A class implementing a line stimulus."""

    def __init__(self, start_point, end_point, line_width, colour=None,
                 anti_aliasing=None):
        """Create a line between two points.

        Parameters
        ----------
        start_point : (int, int)
            start point of the line (x,y)
        end_point : (int, int)
            end point of the line (x,y)
        line_width : int
            width of the plotted line
        colour : (int, int, int), optional
            line colour (int, int, int)
        anti_aliasing : int, optional
            anti aliasing parameter (good anti_aliasing with 10)

        """

        self._start_point = list(start_point)
        self._end_point = list(end_point)
        self._line_width = line_width
        Visual.__init__(self, position=[0,0]),
        if colour is None:
            colour = defaults.line_colour
            if colour is None:
                colour = _internals.active_exp.foreground_colour
        self._colour = colour
        if anti_aliasing is not None:
            self._anti_aliasing = anti_aliasing
        else:
            self._anti_aliasing = defaults.line_anti_aliasing

        s = misc.geometry.XYPoint(start_point)
        e = misc.geometry.XYPoint(end_point)
        d = misc.geometry.XYPoint(e.x - s.x, e.y - s.y)
        self._position[0] = s.x + (d.x // 2)
        self._position[1] = s.y + (d.y // 2)

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def start_point(self):
        """Getter for start_point."""
        return self._start_point

    @property
    def end_point(self):
        """Getter for end_point."""
        return self._end_point

    @property
    def line_width(self):
        """Getter for line_width."""
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        """Setter for line_width."""

        if self.has_surface:
            raise AttributeError(Line._getter_exception_message.format(
                "line_width"))
        else:
            self._line_width = value

    @property
    def colour(self):
        """Getter for colour."""
        return self._colour

    @colour.setter
    def colour(self, value):
        """Setter for colour."""

        if self.has_surface:
            raise AttributeError(Line._getter_exception_message.format(
                "colour"))
        else:
            self._colour = value

    @property
    def anti_aliasing(self):
        """Getter for anti_aliasing."""

        return self._anti_aliasing

    @anti_aliasing.setter
    def anti_aliasing(self, value):
        """Setter for anti_aliasing."""

        if self.has_surface:
            raise AttributeError(Line._getter_exception_message.format(
                "anti_aliasing"))
        self._anti_aliasing = value

    @property
    def position(self):
        """Getter for position."""
        return self._position

    @position.setter
    def position(self, value):
        """Setter for position."""

        offset_x = value[0] - self._position[0]
        offset_y = value[1] - self._position[1]
        self._position = list(value)
        self._start_point[0] = self._start_point[0] + offset_x
        self._start_point[1] = self._start_point[1] + offset_y
        self._end_point[0] = self._end_point[0] + offset_x
        self._end_point[1] = self._end_point[1] + offset_y

    def move(self, offset):
        """Moves the stimulus in 2D space.

        Parameters
        ----------
        offset : list, optional
            translation along x and y axis

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        -----
        When using OpenGL, this can take longer then 1ms!

        """

        start = get_time()
        moved = False
        x = offset[0]
        y = offset[1]
        if x > 0 or x < 0:
            self._position[0] = self._position[0] + x
            moved = True
        if y > 0 or y < 0:
            self._position[1] = self._position[1] + y
            moved = True
        if moved and self._ogl_screen is not None:
            self._ogl_screen.refresh_position()
        self._start_point[0] = self._start_point[0] + x
        self._start_point[1] = self._start_point[1] + y
        self._end_point[0] = self._end_point[0] + x
        self._end_point[1] = self._end_point[1] + y
        return int((get_time() - start) * 1000)

    def _create_surface(self):
        """Create the surface of the stimulus."""

        s = misc.geometry.XYPoint(self._start_point)
        e = misc.geometry.XYPoint(self._end_point)
        d = misc.geometry.XYPoint(e.x - s.x, e.y - s.y)
        aa_scaling = int((self._anti_aliasing / 5.0) + 1)
        if self._anti_aliasing > 0:
           surface = pygame.surface.Surface((s.distance(e)*aa_scaling,
                self._line_width*aa_scaling), pygame.SRCALPHA).convert_alpha()
        else:
            surface = pygame.surface.Surface((s.distance(e),
                self._line_width), pygame.SRCALPHA).convert_alpha()
        surface.fill(self._colour)
        surface = pygame.transform.rotate(surface, math.atan2(d.y, d.x) * 180 / math.pi)
        if self._anti_aliasing > 0:
            size = surface.get_size()
            surface = pygame.transform.smoothscale(surface,
                                                   (int(size[0] / aa_scaling),
                                                    int(size[1] / aa_scaling)))
        return surface


if __name__ == "__main__":
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    p1 = (-180, 15)
    p2 = (200, 0)
    line = Line(p1, p2, 2)
    line.present()
    exp.clock.wait(1000)
