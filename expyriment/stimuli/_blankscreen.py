#!/usr/bin/env python

"""
A blank screen stimulus.

This module contains a class implementing a blank screen stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from ._canvas import Canvas
from .. import _internals

class BlankScreen(Canvas):
    """A class implementing a blank screen."""

    def __init__(self, colour=None):
        """Create a blank screen.

        Parameters
        ----------
        colour : (int,int,int), optional
            colour of the blank screen
        """

        if colour is not None:
            self._colour = colour
        else:
            self._colour = _internals.active_exp.background_colour
        try:
            size = _internals.active_exp.screen.surface.get_size()
        except:
            raise RuntimeError("Could not get size of screen!")
        Canvas.__init__(self, size, colour=self._colour)


    @staticmethod
    def _demo(exp=None):
        if exp is None:
            from .. import control
            control.set_develop_mode(True)
            control.defaults.event_logging.event_logging = 0
            exp_ = control.initialize()
        blankscreen = BlankScreen()
        blankscreen.present()
        if exp is None:
            exp_.clock.wait(1000)
