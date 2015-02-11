#!/usr/bin/env python

"""
A circle stimulus.

This module contains a class implementing a circle stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import math

import defaults
from _ellipse import Ellipse


class Circle(Ellipse):
    """A class implementing a basic 2D circle."""

    def __init__(self, radius, colour=None, line_width=None, position=None,
                 anti_aliasing=None):
        """Create a circle.

        Parameters
        ----------
        radius : int
            radius of the circle
        colour : (int,int,int), optional
            colour of the circle
        line_width : int, optional
            line width in pixels; 0 or a value larger the radius will result
            in a filled circle
        position : (int, int), optional
            position of the stimulus
        anti_aliasing : int, optional
            anti aliasing parameter (good anti_aliasing with 10)

        """

        self._radius = radius
        if position is None:
            position = defaults.circle_position
        if colour is None:
            colour = defaults.circle_colour
        if line_width is None:
            line_width = defaults.circle_line_width
        elif line_width < 0 or line_width >= self._radius:
            raise AttributeError("line_width must be >= 0 and < radius!")
        if anti_aliasing is not None:
            self._anti_aliasing = anti_aliasing
        else:
            self._anti_aliasing = defaults.circle_anti_aliasing
        Ellipse.__init__(self, [radius, radius], colour, line_width,
                         position, anti_aliasing)

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def radius(self):
        """Getter for radius."""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Setter for radius."""

        if self.has_surface:
            raise AttributeError(Circle._getter_exception_message.format(
                "radius"))
        else:
            self._radius = value

    def get_polar_coordiantes(self):
        """Returns tuple with polar coordinates (radial, angle in degrees)."""
        angle = math.atan2(self._position[1], self._position[0])
        angle = angle / math.pi * 180
        radial = math.sqrt ((self._position[0] * self._position[0]) +
                            (self._position[1] * self._position[1]))
        return (radial, angle)

    def set_polar_coordinates(self, radial, angle_in_degrees):
        """Set polar coordinates.

        Parameters
        ----------
        radial : int
            radial to set
        angle_in_degrees : float
            angle of degrees to set

        """

        a = angle_in_degrees / 180.0 * math.pi
        self._position[0] = radial * math.cos(a)
        self._position[1] = radial * math.sin(a)

    def overlapping_with_circle(self, other, minimal_gap=0):
        """Return True if touching or overlapping with another circle.

        Parameters
        ----------
        other : expyriment.stimuli.Circle object
            other circle
        minimal_gap : int, optional
            minimum gap between two circle, small gaps will be treated as
            overlapping (default=0)

        Returns
        -------
        is_inside : bool

        """

        d = self.distance(other)
        return (d - minimal_gap <= other._radius + self._radius)

    def center_inside_circle(self, other):
        """Return True if the center is inside another circle.

        Parameters
        ----------
        other : expyriment.stimuli.Circle object
            other circle

        Returns
        -------
        is_inside : bool

        """

        d = self.distance(other)
        return (d <= other._radius)

    def inside_circle(self, other):
        """Return True if the whole circle is inside another circle.

        Parameters
        ----------
        other : expyriment.stimuli.Circle object
            other circle

        Returns
        -------
        is_inside : bool

        """

        d = self.distance(other)
        return (d <= other._radius - self._radius)

if __name__ == "__main__":
    from expyriment import control
    control.set_develop_mode(True)
    defaults.event_logging = 0
    exp = control.initialize()
    dot = Circle(radius=100, anti_aliasing=10)
    dot.present()
    exp.clock.wait(1000)
