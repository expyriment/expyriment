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


import expyriment
from _canvas import Canvas

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
            self._colour = expyriment._active_exp.background_colour
        try:
            size = expyriment._active_exp.screen.surface.get_size()
        except:
            raise RuntimeError("Could not get size of screen!")
        Canvas.__init__(self, size, colour=self._colour)


if __name__ == "__main__":
    from expyriment import control
    control.set_develop_mode(True)
    defaults.event_logging = 0
    exp = control.initialize()
    blankscreen = BlankScreen()
    blankscreen.present()
    exp.clock.wait(1000)
