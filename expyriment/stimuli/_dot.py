#!/usr/bin/env python

"""
A dot stimulus.

This module contains a class implementing a dot stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import defaults
from _circle import Circle

class Dot(Circle):
    """A class implementing a basic 2D dot."""

    def __init__(self, radius, colour=None, position=None):
        """Create a dot.

        DEPRECATED CLASS: Please use 'Circle'!

        Parameters
        ----------
        radius : int
            radius of the dot
        colour : (int, int, int), optional
            colour of the dot
        position : (int, int), optional
            position of the stimulus

        """

        if position is None:
            position = defaults.dot_position
        if colour is None:
            colour = defaults.dot_colour
        Circle.__init__(self, diameter=radius*2, colour=colour,
                        position=position)

    def is_overlapping(self, other, minimal_gap=0):
        """DEPRECATED METHOD: Please use 'overlapping_with_circle'"""
        return self.overlapping_with_circle(other, minimal_gap)

    def is_center_inside(self, other):
        """DEPRECATED METHOD: Please use 'center_inside_circle'"""
        return self.center_inside_circle(other)

    def is_inside(self, other):
        """DEPRECATED METHOD: Please use 'inside_circle'"""
        return self.inside_circle(other)

if __name__ == "__main__":
    from expyriment import control
    control.set_develop_mode(True)
    defaults.event_logging = 0
    exp = control.initialize()
    dot = Dot(radius=100)
    dot.present()
    exp.clock.wait(1000)
