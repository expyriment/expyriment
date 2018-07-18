#!/usr/bin/env python

"""
A fixation cross stimulus.

This module contains a class implementing a fixation cross stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from . import defaults
from ._line import Line
from ._canvas import Canvas
from .. import _internals

class FixCross(Canvas):
    """A class implementing a general fixation cross."""

    def __init__(self, size=None, position=None, line_width=None,
                 colour=None, anti_aliasing=False, cross_size=None):
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

        NOTE
        ----
        The parameter anti_aliasing and cross_size are deprecated.
        Please use 'size' and specify x and y dimensions.

        """

        if cross_size is not None and size is None:
            raise DeprecationWarning("Property cross_size is obsolete. Please use size")

        if position is None:
            position = defaults.fixcross_position

        if size is None:
            size = defaults.fixcross_size

        if colour is None:
            colour = defaults.fixcross_colour
        if colour is None:
            colour = _internals.active_exp.foreground_colour
        if line_width is None:
            line_width = defaults.fixcross_line_width

        if anti_aliasing is not False:
            raise DeprecationWarning("Anti_aliasing for fixcross is deprecated.")

        Canvas.__init__(self, size=(size[0], size[1]), position=position, colour=colour)
        self._line_width = line_width

    @property
    def cross_size(self):
        """OBSOLETE property, please use size"""

        raise DeprecationWarning("Property cross_size is obsolete. Please use size")

    @property
    def anti_aliasing(self):
        """Getter for anti_aliasing."""

        raise DeprecationWarning("Anti_aliasing for fixcross is deprecated.")

    @property
    def line_width(self):
        """Getter for line_width."""

        return self._line_width

    def _create_surface(self):

        canvas = Canvas(position=self._position, size=self._size, colour=None)
        s = (self._size[0] // 2, self._size[1] // 2)
        Line(start_point=(-s[0], 0), end_point=(s[1], 0), line_width=self._line_width,
                    colour=self._colour, anti_aliasing=False).plot(canvas)
        Line(start_point=(0, -s[0]), end_point=(0, s[1]), line_width=self._line_width,
                    colour=self._colour, anti_aliasing=False).plot(canvas)
        canvas._create_surface()

        return canvas._get_surface()



if __name__ == "__main__":
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    fixcross = FixCross(size=(100, 100))
    fixcross.present()
    exp.clock.wait(1000)
