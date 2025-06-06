#!/usr/bin/env python

"""
A picture stimulus.

This module contains a class implementing a picture stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


import os

import pygame

from .. import _internals
from ..misc import unicode2byte
from . import defaults
from ._visual import Visual


class Picture(Visual):
    """A class implementing a general picture stimulus."""

    def __init__(self, filename, position=None):
        """Create a picture.

        Parameters
        ----------
        filename : str
            filename (incl. path) of the picture file
        position :(int,int), optional
            position of the stimulus

        """

        if position is None:
            position = defaults.picture_position
        Visual.__init__(self, position, log_comment=filename)
        self._filename = filename
        if not(os.path.isfile(self._filename)):
            raise IOError(u"The picture file '{0}' does not exist".format(
                filename))

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def filename(self):
        """Getter for filename."""

        return self._filename

    @filename.setter
    def filename(self, value):
        """Setter for filename."""

        if self.has_surface:
            raise AttributeError(Picture._getter_exception_message.format(
                "filename"))
        else:
            self._filename = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        # Due to a bug in handling file names in PyGame 1.9.2, we pass a file
        # handle to PyGame. See also:
        # https://github.com/expyriment/expyriment/issues/81
        with open(self._filename, 'rb') as f:
            surface = pygame.image.load(f).convert_alpha()
        if self._logging:
            _internals.active_exp._event_file_log(
                "Picture,loaded,{0}".format(self._filename), 1)
        return surface


    @staticmethod
    def _demo(exp=None):
        if exp is None:
            from .. import __file__, control
            control.set_develop_mode(True)
            control.defaults.event_logging = 0
            exp_ = control.initialize()
        directory = os.path.dirname(__file__)
        picture = Picture(os.path.join(directory, "expyriment_logo.png"))
        picture.present()
        if exp is None:
            exp_.clock.wait(1000)
