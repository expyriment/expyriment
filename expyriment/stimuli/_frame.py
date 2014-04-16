#!/usr/bin/env python

"""
A frame stimulus.

This module contains a class implementing a frame stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import defaults
from _shape import Shape

class Frame(Shape):
    """A class implementing a frame stimulus."""

    #FIXME: frames line width are still no symetric. Fixme later!

    def __init__(self, size, position=None, frame_line_width=None,
                 colour=None, anti_aliasing=None, line_width=None):
        """Create a frame.


        Parameters
        ----------
        size : (int, int)
            size of the frame (xy)
        position : (int, int), optional
            position of the stimulus
        frame_line_width : int, optional
            width of the frame lines
        colour : (int, int, int), optional
            colour of the frame
        anti_aliasing : int, optional
            anti aliasing parameter

        Notes
        -----
        DEPRECATED CLASS: Please use 'Rectangle' with a line_width > 0!

        """

        if position is None:
            position = defaults.frame_position
        if colour is None:
            colour = defaults.frame_colour
        if anti_aliasing is None:
            anti_aliasing = defaults.frame_anti_aliasing
        Shape.__init__(self, position=position, colour=colour,
                    line_width=0, anti_aliasing=anti_aliasing)
        if frame_line_width is None:
            frame_line_width = defaults.frame_frame_line_width
        if line_width is not None:
            message = "Frame: line_width attribute have been renamed! " +\
                           "Please use frame_line_width."
            raise RuntimeError(message)

        self._frame_size = list(size)
        self._frame_line_width = frame_line_width

        l1 = self._frame_size[0]
        l2 = self._frame_size[1]
        l3 = int(l1 - (self._frame_line_width * 2.0))
        l4 = int(l2 - (self._frame_line_width * 2.0))
        self.add_vertex((l1, 0))
        self.add_vertex((0, l2))
        self.add_vertex((-l1, 0))
        self.add_vertex((0, -l2 + self._frame_line_width))
        self.add_vertex((self._frame_line_width , 0))
        self.add_vertex((0, l4 - 1))
        self.add_vertex((l3, 0))

        self.add_vertex((0, -l4 + 1))
        self.add_vertex((-l3 - self._frame_line_width, 0))

    @property
    def frame_size(self):
        """Getter for frame_size."""

        return self._frame_size

    @property
    def frame_line_width(self):
        """Getter for frame_line_width."""

        return self._frame_line_width


if __name__ == "__main__":
    from expyriment import control
    control.set_develop_mode(True)
    defaults.event_logging = 0
    exp = control.initialize()
    fixcross = Frame(size=(100, 100), frame_line_width=1, position=(0, 100))
    fixcross.present()
    exp.clock.wait(2000)
