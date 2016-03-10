#!/usr/bin/env python

"""
A fixation cross stimulus.

This module contains a class implementing a fixation cross stimulus.

"""
from __future__ import absolute_import
from __future__ import division


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from . import defaults
from ._shape import Shape
import expyriment

class FixCross(Shape):
    """A class implementing a general fixation cross."""

    def __init__(self, size=None, position=None, line_width=None,
                 colour=None, anti_aliasing=None, cross_size=None):
        """Create a fixation cross.

        Parameters
        ----------
        size : (int, int), optional
            size of the cross
        position : (int, int), optional
            position of the stimulus
        line_width : int optional
            width of the lines
        colour : (int, int, int), optional
            colour of the cross
        anti_aliasing :  int, optional
            anti aliasing parameter (good anti_aliasing with 10)


        NOTE
        ----
        The parameter cross_size is now OBSOLETE.
        Please use 'size' and specify x and y dimensions.

        """

        if cross_size is not None and size is None:
            raise DeprecationWarning("Property cross_size is obsolete. Please use size")

        if position is None:
            position = defaults.fixcross_position
        if colour is None:
            colour = defaults.fixcross_colour
        if colour is not None:
            self._colour = colour
        else:
            self._colour = expyriment._active_exp.foreground_colour
        if anti_aliasing is None:
            anti_aliasing = defaults.fixcross_anti_aliasing
        Shape.__init__(self, position=position, line_width=0,
                         colour=colour,
                         anti_aliasing=anti_aliasing)
        if size is None:
            size = defaults.fixcross_size
        if line_width is None:
            line_width = defaults.fixcross_line_width

        self._size = size
        x = (self._size[0] - line_width) // 2
        y = (self._size[1] - line_width) // 2
        self.add_vertex((line_width, 0))
        self.add_vertex((0, -y))
        self.add_vertex((x, 0))
        self.add_vertex((0, -line_width))
        self.add_vertex((-x, 0))
        self.add_vertex((0, -y))
        self.add_vertex((-line_width, 0))
        self.add_vertex((0, y))
        self.add_vertex((-x, 0))
        self.add_vertex((0, line_width))
        self.add_vertex((x, 0))

    @property
    def size(self):
        """Getter for size."""

        return self._size

    @property
    def cross_size(self):
        """OBSOLETE property, please use size"""

        raise DeprecationWarning("Property cross_size is obsolete. Please use size")

    @property
    def line_width(self):
        """Getter for line_width."""

        return self._line_width


if __name__ == "__main__":
    from expyriment import control
    control.set_develop_mode(True)
    defaults.event_logging = 0
    exp = control.initialize()
    fixcross = FixCross(size=(100, 100))
    fixcross.present()
    exp.clock.wait(1000)
