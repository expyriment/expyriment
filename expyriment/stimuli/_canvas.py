#!/usr/bin/env python

"""
A Canvas stimulus.

This module contains a class implementing a canvas stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import pygame

from . import defaults
from ._visual import Visual


class Canvas(Visual):
    """A class implementing a canvas stimulus."""

    def __init__(self, size, position=None, colour=None):
        """Create a canvas.

        Parameters
        ----------
        size : (int, int)
            size of the canvas (int,int)
        position : (int, int), optional
            position of the stimulus
        colour : (int,int,int), optional
            colour of the canvas stimulus

        """

        if position is None:
            position = defaults.canvas_position
        Visual.__init__(self, position)
        self._size = size
        if colour is not None:
            self._colour = colour
        else:
            self._colour = defaults.canvas_colour

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def size(self):
        """Getter for size."""
        return self._size

    @size.setter
    def size(self, value):
        """Setter for size."""

        if self.has_surface:
            raise AttributeError(Canvas._getter_exception_message.format(
                "size"))
        else:
            self._size = value

    @property
    def colour(self):
        """Getter for colour."""
        return self._colour

    @colour.setter
    def colour(self, value):
        """Setter for colour."""

        if self.has_surface:
            raise AttributeError(Canvas._getter_exception_message.format(
                "colour"))
        else:
            self._colour = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        surface = pygame.surface.Surface(self._size,
                                         pygame.SRCALPHA).convert_alpha()
        if self._colour is not None:
            surface.fill(self._colour)
        return surface


    @staticmethod
    def _demo(exp=None):
        if exp is None:
            from .. import control
            control.set_develop_mode(True)
            control.defaults.event_logging = 0
            exp_ = control.initialize()
        cnvs = Canvas((200, 200), colour=(255, 255, 255))
        cnvs.present()
        if exp is None:
            exp_.clock.wait(1000)
