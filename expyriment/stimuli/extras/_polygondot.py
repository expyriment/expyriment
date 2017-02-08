#!/usr/bin/env python

"""
A dot stimulus.

This module contains a class implementing a dot stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from . import defaults
from ...stimuli.extras._polygonellipse import PolygonEllipse

class PolygonDot(PolygonEllipse):
    """A class implementing a dot as a child of PolygonEllipse."""

    def __init__(self, radius, position=None, colour=None,
                 resolution_factor=None, anti_aliasing=None):
        """Create a dot.

        Parameters
        ----------
        radius : int
            radius of the dot
        position : int, optional
            position of the stimulus
        colour : (int, int, int), optional
            colour of the dot
        resolution_factor : int, optional
            The resolution_factor increases the resolution of the eclipse.
            The default factor is 1 resulting in 36 points describing the
            ellipse.
        anti_aliasing : int, optional
            anti aliasing parameter

        """

        if position is None:
            position = defaults.polygondot_position
        if colour is None:
            colour = defaults.polygondot_colour
        if anti_aliasing is None:
            anti_aliasing = defaults.polygondot_anti_aliasing
        if resolution_factor is None:
            resolution_factor = defaults.polygondot_resolution_factor

        if radius == 0:
            radius = 0.5
        PolygonEllipse.__init__(self, size=[2 * radius, 2 * radius],
                        position=position,
                        resolution_factor=resolution_factor,
                        colour=colour, line_width=0)

    @property
    def radius(self):
        """Getter for radius."""
        return self.ellipse_size[0] // 2

    def is_center_inside(self, other):
        """Return True if the center is inside another dot.

        Parameters
        ----------
        other : stimuli.PolygonDot
            the other dot

        Returns
        -------
        out : bool

        """

        d = self.distance(other)
        return (d <= other.radius)

    def is_inside(self, other):
        """Return True if the whole dot is inside another dot.

        Parameters
        ----------
        other : stimuli.PolygonDot
            other dot

        Returns
        -------
        out : bool

        """

        d = self.distance(other)
        return (d <= other.radius - self.radius)



if __name__ == "__main__":
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    dot = PolygonDot(radius=100)
    dot.present()
    exp.clock.wait(1000)
