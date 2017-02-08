#!/usr/bin/env python

"""
A Rectangle stimulus.

This module contains a class implementing a rectangle stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from . import defaults
from ...stimuli._shape import Shape
from ... import _internals

class PolygonRectangle(Shape):
    """A class implementing a rectangle stimulus."""

    def __init__(self, size, position=None, colour=None, anti_aliasing=None):
        """Create a filled rectangle.

        Parameters
        ----------
        size : (int, int)
            size (width, height) of the Rectangle
        position : (int, int), optional
            position of the stimulus
        colour   : (int, int, int), optional
            colour of the rectangle
        anti_aliasing : int, optional
            anti aliasing parameter

        """

        if position is None:
            position = defaults.polygonrectangle_position
        if colour is None:
            colour = defaults.polygonrectangle_colour
        if colour is None:
            colour = _internals.active_exp.foreground_colour
        if anti_aliasing is None:
            anti_aliasing = defaults.polygonrectangle_anti_aliasing

        Shape.__init__(self, position=position, colour=colour,
                       line_width=0, anti_aliasing=anti_aliasing)
        self.add_vertex((size[0], 0))
        self.add_vertex((0, size[1]))
        self.add_vertex((-size[0], 0))


if __name__ == "__main__":
    from .. import control, stimuli
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    cnvs = stimuli.Rectangle((20, 200), colour=(255, 0, 255))
    cnvs.present()
    exp.clock.wait(1000)
