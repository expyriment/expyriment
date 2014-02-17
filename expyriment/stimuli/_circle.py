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

    def __init__(self, diameter, colour=None, line_width=None, position=None):
        """Create a circle.

        Parameters
        ----------
        diameter : int
            diameter of the circle
        colour : (int,int,int), optional
            colour of the circle
        line_width : int, optional
            line width in pixels; 0 or a value larger the radius will result
            in a filled circle
        position : (int, int), optional
            position of the stimulus

        """

        self._diameter = diameter
        self._radius = diameter/2.0
        if position is None:
            position = defaults.circle_position
        if colour is None:
            colour = defaults.circle_colour
        if line_width is None:
            line_width = defaults.circle_line_width
        elif line_width < 0 or line_width >= self._diameter/2.0:
            raise AttributeError("line_width must be >= 0 and < diameter/2!")
        Ellipse.__init__(self, [diameter, diameter], colour, line_width,
                         position)

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def diameter(self):
        """Getter for diameter."""
        return self._diameter

    @diameter.setter
    def diameter(self, value):
        """Setter for diameter."""

        if self.has_surface:
            raise AttributeError(Circle._getter_exception_message.format(
                "diameter"))
        else:
            self._diameter = value

    @property
    def radius(self):
        """Getter for radius."""
        return self._radius

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
    dot = Circle(diameter=100, line_width=3)
    dot.present()
    exp.clock.wait(1000)
