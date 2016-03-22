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
from . import defaults

from ._polygonrectangle import PolygonRectangle
from ... import _internals
from ... import misc


class PolygonLine(PolygonRectangle):
    """A class implementing a line stimulus."""

    def __init__(self, start_position, end_position, line_width, colour=None,
                 anti_aliasing=None):
        """Create a line between two points.

        Parameters
        ----------
        start_position : (int, int)
            start point of the line (x,y)
        end_position : (int, int)
            end point of the line (x,y)
        line_width : int, optional
            width of the plotted line
        colour : (int, int, int), optional
            line colour
        anti_aliasing : int
            anti aliasing parameter (good anti_aliasing with 10)

        """

        if colour is None:
            colour = defaults.polygonline_colour
        if colour is None:
            colour = _internals.active_exp.foreground_colour
        if anti_aliasing is None:
            anti_aliasing = defaults.polygonline_anti_aliasing

        f = misc.geometry.XYPoint(start_position)
        t = misc.geometry.XYPoint(end_position)
        d = misc.geometry.XYPoint(t.x - f.x, t.y - f.y)
        PolygonRectangle.__init__(self, size=(f.distance(t), line_width),
                                  colour=colour, anti_aliasing=anti_aliasing)
        self.native_rotate(math.atan2(d.y, d.x) * 180 / math.pi)
        self.position[0] = f.x + (d.x // 2)
        self.position[1] = f.y + (d.y // 2)


if __name__ == "__main__":
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    p1 = (-180, 15)
    p2 = (200, 0)
    line = PolygonLine(p1, p2, 2)
    line.present()
    exp.clock.wait(1000)
