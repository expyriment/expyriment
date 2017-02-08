#!/usr/bin/env python

"""
A LCD symbol.

This module contains a class implementing a LCD symbol.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import math
import copy

import pygame

from . import defaults
from ... import _internals, stimuli
from ...stimuli._visual import Visual
from ...stimuli.extras._polygondot import PolygonDot


class LcdSymbol(Visual):
    """A LCD symbol class.

    IDs for points and line ::

        Point=      Lines =
        0---1         X-0-X
        |   |         1   2
        2---3         X-3-X
        |   |         4   5
        4---5         X-6-X

    Valid shapes are::

        '0','1','2','3','4','5','6','7','8','9'
        'A','C','E','F','U','H','L','P','h'

    """

    _shapes = {"0":(0, 1, 2, 4, 5, 6),
              "1":(2, 5),
              "2":(0, 2, 3, 4, 6),
              "3":(0, 2, 3, 5, 6),
              "4":(1, 2, 3, 5),
              "5":(0, 1, 3, 5, 6),
              "6":(0, 1, 3, 4, 5, 6),
              "7":(0, 2 , 5),
              "8":(0, 1, 2 , 3 , 4 , 5 , 6),
              "9":(0, 1 , 2 , 3 , 5, 6),
              "A":(0, 1, 2, 3, 4, 5),
              "C":(0, 1, 4, 6),
              "E":(0, 1, 3, 4, 6),
              "F":(0, 1, 3, 4),
              "U":(1, 4, 6, 5, 2),
              "H":(1, 2, 3, 4, 5),
              "L":(1, 4, 6),
              "P":(0, 1, 2, 3, 4),
              "h":(1, 3, 4, 5)
              }

    _lines = ((0, 1), (0, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5))

    def __init__(self, shape, position=None, size=None, colour=None,
                 inactive_colour=None, background_colour=None,
                 line_width=None, gap=None, simple_lines=None):
        """Create a LCD symbol.

        Parameters
        ----------
        shape : list
            shape to show
        position : (int, int), optional
            position to show the symbol
        size : (int, int)
            size of the LCD symbol
        colour : (int, int, int), optional
            LCD symbol colour
        inactive_colour : (int, int, int), optional
            colour of inactive lines
        background_colour : (int, int, int), optional
        line_width : int, optional
            width of the lines
        gap :int, optional
            gap between lines
        simple_lines : bool, optional
            use simple lines

        """

        Visual.__init__(self, position)
        if shape in self._shapes:
            self._shape = self._shapes[shape]
        else:
            self._shape = shape
        if size is not None:
            self._width = size[0]
            self._height = size[1]
        else:
            size = defaults.lcdsymbol_size
            if size is None:
                try:
                    size = _internals.active_exp.screen.surface.get_size()
                except:
                    raise RuntimeError("Could not get size of screen!")
            self._width = size[0]
            self._height = size[1]
        if colour is None:
            colour = defaults.lcdsymbol_colour
        if colour is not None:
            self._colour = colour
        else:
            self._colour = _internals.active_exp.foreground_colour
        if inactive_colour is not None:
            self._inactive_colour = inactive_colour
        else:
            self._inactive_colour = \
                    defaults.lcdsymbol_inactive_colour
        if background_colour is not None:
            self._background_colour = background_colour
        else:
            self._background_colour = \
                    defaults.lcdsymbol_background_colour
        if line_width is not None:
            self._line_width = line_width
        else:
            self._line_width = defaults.lcdsymbol_line_width
        if gap is not None:
            self._gap = gap
        else:
            self._gap = defaults.lcdsymbol_gap
        if simple_lines is not None:
            self._simple_lines = simple_lines
        else:
            self._simple_lines = defaults.lcdsymbol_simple_lines

        x = int(self.line_width / 2.0) + 1
        self._points = (PolygonDot(radius=0, position=(x, x)),
                        PolygonDot(radius=0, position=(self._width - x, x)), \
                        PolygonDot(radius=0,
                            position=(x, math.floor(self._height / 2))), \
                        PolygonDot(radius=0,
                            position=(self._width - x,
                                      math.floor(self._height / 2))), \
                        PolygonDot(radius=0, position=(x, self._height - x)), \
                        PolygonDot(radius=0,
                            position=(self._width - x, self._height - x)))
        stimuli._stimulus.Stimulus._id_counter -= 6

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def shape(self):
        """Getter for shape."""

        return self._shape

    @shape.setter
    def shape(self, value):
        """Setter for shape."""

        if self.has_surface:
                raise AttributeError(
                    LcdSymbol._getter_exception_message.format("shape"))
        else:
            if value in self.shapes:
                self._shape = self.shapes[value]
            else:
                self._shape = value

    @property
    def size(self):
        """Getter for size."""

        return (self._width, self._height)

    @size.setter
    def size(self, value):
        """Setter for size."""

        if self.has_surface:
                raise AttributeError(
                    LcdSymbol._getter_exception_message.format("shape"))
        else:
            self._width = value[0]
            self._height = value[1]
            self._points = (PolygonDot(radius=0, position=(0, 0)),
                           PolygonDot(radius=0, position=(self._width, 0)),
                           PolygonDot(radisu=0,
                               position=(0, math.floor(self._height / 2))),
                           PolygonDot(radius=0, position=(self._width,
                                         math.floor(self._height / 2))),
                           PolygonDot(radius=0, position=(0, self._height)),
                           PolygonDot(radius=0, position=(self._width, self._height)))
            stimuli._stimulus.Stimulus._id_counter -= 6

    @property
    def colour(self):
        """Getter for colour."""

        return self._colour

    @colour.setter
    def colour(self, value):
        """Setter for colour."""

        if self.has_surface:
                raise AttributeError(
                    LcdSymbol._getter_exception_message.format("colour"))
        else:
            self._colour = value

    @property
    def inactive_colour(self):
        """Getter for inactive_colour."""

        return self._inactive_colour

    @inactive_colour.setter
    def inactive_colour(self, value):
        """Setter for inactive_colour."""

        if self.has_surface:
                raise AttributeError(
                    LcdSymbol._getter_exception_message.format(
                        "inactive_colour"))
        else:
            self._inactive_colour = value

    @property
    def background_colour(self):
        """Getter for background_colour."""

        return self._background_colour

    @background_colour.setter
    def background_colour(self, value):
        """Setter for background_colour."""

        if self.has_surface:
                raise AttributeError(
                    LcdSymbol._getter_exception_message.format(
                        "background_colour"))
        else:
            self._background_colour = value

    @property
    def line_width(self):
        """Getter for line_width."""

        return self._line_width

    @line_width.setter
    def line_width(self, value):
        """Setter for line_width."""

        if self.has_surface:
                raise AttributeError(
                    LcdSymbol._getter_exception_message.format("line_width"))
        else:
            self._line_width = value

    @property
    def gap(self):
        """Getter for gap."""

        return self._gap

    @gap.setter
    def gap(self, value):
        """Setter for gap."""

        if self.has_surface:
                raise AttributeError(
                    LcdSymbol._getter_exception_message.format("gap"))
        else:
            self._gap = value

    @property
    def simple_lines(self):
        """Getter for simple_lines."""

        return self._simple_lines

    @simple_lines.setter
    def simple_lines(self, value):
        """Setter for simple_lines."""

        if self.has_surface:
                raise AttributeError(
                    LcdSymbol._getter_exception_message.format(
                        "simple_lines"))
        else:
            self._simple_lines = value

    @property
    def points(self):
        """Getter for points."""

        return self._points

    def _create_surface(self):
        """Create the surface of the stimulus."""

        surface = pygame.surface.Surface((self._width, self._height),
                                        pygame.SRCALPHA).convert_alpha()
        if self.background_colour is not None:
            surface.fill(self.background_colour)
        if self.inactive_colour is not None:
            #draw background
            for x in self._shapes["8"]:
                moved_poly = []
                for p in self.get_line_polygon(x):
                    moved_poly.append((p[0], p[1]))
                pygame.draw.polygon(surface, self.inactive_colour,
                                    moved_poly, 0)
        if len(self._shape) > 0:
            for x in self._shape:
                moved_poly = []
                for p in self.get_line_polygon(x):
                    moved_poly.append((p[0], p[1]))
                pygame.draw.polygon(surface, self.colour, moved_poly, 0)
        return surface

    def get_line_points(self, idx):
        """Return point tuple including start and end point of a line.

        Parameters
        ----------
        idx : int
            index of the line

        Returns
        -------
        points : ((int, int), (int,int))
            point tuple including start and end point of a line

        """

        if idx == 0 or idx == 3 or idx == 6 : # horizontal line
            p1 = copy.copy(self.points[self._lines[idx][0]])
            p2 = copy.copy(self.points[self._lines[idx][1]])
            p1.position[0] = p1.position[0] + self.gap
            p2.position[0] = p2.position[0] - self.gap
            return (p1.position, p2.position)
        elif idx == 1 or idx == 2 or idx == 4 or idx == 5: # vertical line
            p1 = copy.copy(self.points[self._lines[idx][0]])
            p2 = copy.copy(self.points[self._lines[idx][1]])
            p1.position[1] = p1.position[1] + self.gap
            p2.position[1] = p2.position[1] - self.gap
            return (p1.position, p2.position)
        else:
            return ()

    def get_line_polygon(self, idx):
        """Return point list describing the line as polygon.

        Parameters
        ----------
        idx : int
            index of the line (int)

        Returns
        -------
        point : list of tuple
        """

        if idx == 0 or idx == 3 or idx == 6 : # horizontal line
            return self._line_to_polygon(self.points[self._lines[idx][0]], \
                                     self.points[self._lines[idx][1]], True)
        elif idx == 1 or idx == 2 or idx == 4 or idx == 5: # vertical line
            return self._line_to_polygon(self.points[self._lines[idx][0]], \
                                     self.points[self._lines[idx][1]], False)
        else:
            return ()

    def _line_to_polygon(self, start, end, horizontal):
        """Convert a line defined by start and end points to a polygon.

        Parameters
        ----------
        start : int
            start point
        end : int
            end point
        horizontal : bool
            True or False

        """

        w2 = math.floor((self.line_width - 1) / 2)
        if w2 <= 0:
            w2 = 1
        poly = []
        poly.append(copy.copy(start.position))
        p = PolygonDot(radius=0, position=(0, 0))
        stimuli._stimulus.Stimulus._id_counter -= 1
        if horizontal:
            p.position[0] = start.position[0] + self.gap
            p.position[1] = start.position[1] - w2
            poly.append(copy.copy(p.position))
            p.position[0] = end.position[0] - self.gap
            poly.append(copy.copy(p.position))
            poly.append(copy.copy(end.position))
            p.position[0] = end.position[0] - self.gap
            p.position[1] = end.position[1] + w2
            poly.append(copy.copy(p.position))
            p.position[0] = start.position[0] + self.gap
            poly.append(copy.copy(p.position))
        else:
            p.position[0] = start.position[0] + w2
            p.position[1] = start.position[1] + self.gap
            poly.append(copy.copy(p.position))
            p.position[1] = end.position[1] - self.gap
            poly.append(copy.copy(p.position))
            poly.append(copy.copy(end.position))
            p.position[0] = end.position[0] - w2
            p.position[1] = end.position[1] - self.gap
            poly.append(copy.copy(p.position))
            p.position[1] = start.position[1] + self.gap
            poly.append(copy.copy(p.position))

        if self.simple_lines:
            poly.pop(3)
            poly.pop(0)

        return tuple(poly)


if __name__ == "__main__":
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    lcdsymbol = LcdSymbol("A", size=(100, 100))
    lcdsymbol.present()
    exp.clock.wait(1000)
