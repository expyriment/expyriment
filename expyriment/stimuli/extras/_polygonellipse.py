#!/usr/bin/env python

"""
An ellipse stimulus.

This module contains a class implementing an ellipse stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import math as _math
from . import defaults
from ...stimuli._shape import Shape
from ...misc import geometry as _geometry


class PolygonEllipse(Shape):
    """A class implementing an ellipse stimulus."""

    _default_number_of_vertices = 36

    def __init__(self, size, position=None, line_width=None, colour=None,
                 resolution_factor=None, anti_aliasing=None):
        """Create an ellipse.

        Parameters
        ----------
        size : (int,int)
            size of the ellipse (x,y)
        position : (int, int, int), optional
            position of the stimulus
        colour  : (int, int, int), optional
        line_width : int, optional
            if line width is 0, the shape is filled
        resolution_factor : int, optional
            The resolution_factor increases the resolution of the eclipse.
            The default factor is 1 resulting in 36 points describing the
            ellipse
        anti_aliasing : int, optional
            anti aliasing parameter

        """

        if position is None:
            position = defaults.polygonellipse_position
        if colour is None:
            colour = defaults.polygonellipse_colour
        if anti_aliasing is None:
            anti_aliasing = defaults.polygonellipse_anti_aliasing
        if resolution_factor is None:
            resolution_factor = defaults.polygonellipse_resolution_factor
        if line_width is None:
            line_width = defaults.polygonellipse_line_width

        Shape.__init__(self, position=position, colour=colour,
                         anti_aliasing=anti_aliasing,
                         line_width=line_width)

        self._resolution_factor = resolution_factor
        self._ellipse_size = list(size)
        self._circumference = None

        n_vtx = self._default_number_of_vertices * self._resolution_factor
        s = 2 * _math.pi / n_vtx
        w, h = self.ellipse_size
        l = 0
        points = []
        while l < 2 * _math.pi:
            points.append([.5 * _math.cos(l) * w + .5 * w,
                           .5 * _math.sin(l) * h + .5 * h])
            l = l + s
        self._vertices = _geometry.points_to_vertices(points)
        self._update_points()


    @property
    def circumference(self):
        """Getter for circumference.

        Notes
        -----
        Calculates the circumference if required. The algorithm for this
        calculation is taken from http://paulbourke.net/geometry/ellipsecirc/
        Ramanujan, Second Approximation

        """

        if self._circumference is None:
            a, b = self._ellipse_size
            h3 = 3 * (_math.pow((a - b), 2) / _math.pow((a + b), 2))
            self._circumference = _math.pi * (a + b) * \
                              (1.0 + h3 / (10.0 + _math.sqrt(4.0 - h3)))
        return self._circumference

    @property
    def ellipse_size(self):
        """Getter for frame_size."""

        return self._ellipse_size

    @property
    def resolution_factor(self):
        """Getter for the resolution."""

        return self._resolution_factor


if __name__ == "__main__":
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    stim = PolygonEllipse(size=(100, 100), line_width=5)
    stim.present()
    exp.clock.wait(2000)
