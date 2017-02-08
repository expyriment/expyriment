#!/usr/bin/env python

"""
A stimulus circle stimulus.

This module contains a class implementing a stimulus circle stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import random
import math

import pygame

from . import defaults
from ...stimuli._visual import Visual


class StimulusCircle(Visual):
    """A stimulus circle class.

    """

    def __init__(self, radius, stimuli, position=None,
                 background_colour=None):
        """Create a stimulus circle.

        Parameters
        ----------
        radius : int
            radius of the circle
        stimuli : expyriment stimulus
            stimuli to put into the circle
        position : (int, int), optional
            position of the circle
        background_colour : (int, int, int), optional
            background colour of the circle

        """

        Visual.__init__(self, position)
        self._radius = radius
        self._stimuli = stimuli
        if background_colour is None:
            background_colour = \
                    defaults.stimuluscircle_background_colour
        self._background_colour = background_colour

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def radius(self):
        """Getter for radius."""

        return self._radius

    @radius.setter
    def radius(self, value):
        """Setter for radius."""

        if self.has_surface:
            raise AttributeError(
                StimulusCircle._getter_exception_message.format("radius"))
        else:
            self._radius = value

    @property
    def stimuli(self):
        """Getter for stimuli."""

        return self._stimuli

    @stimuli.setter
    def stimuli(self, value):
        """Setter for stimuli."""

        if self.has_surface:
            raise AttributeError(
                StimulusCircle._getter_exception_message.format("stmuli"))
        else:
            self._stimuli = value

    @property
    def background_colour(self):
        """Getter for background_colour."""

        return self._background_colour

    @background_colour.setter
    def background_colour(self, value):
        """Setter for background_colour."""

        if self.has_surface:
            raise AttributeError(
                StimulusCircle._getter_exception_message.format(
                    "background_colour"))
        else:
            self._background_colour = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        # Find largest stim
        max_x = 0
        max_y = 0
        for stim in self.stimuli:
            size = stim.surface_size
            if size[0] > max_x:
                max_x = size[0]
            if size[1] > max_y:
                max_y = size[1]

        # Build surface
        surface = pygame.surface.Surface(
            (self._radius * 2 + max_x,
             self._radius * 2 + max_y),
            pygame.SRCALPHA).convert_alpha()
        if self._background_colour is not None:
            surface.fill(self._background_colour)
        surface_size = surface.get_size()
        for stim in self._stimuli:
            stim_rect = pygame.Rect((0, 0), stim.surface_size)
            stim_rect.center = [stim.position[0] + surface_size[0] // 2,
                                - stim.position[1] + surface_size[1] // 2]
            surface.blit(stim._get_surface(), stim_rect)
        return surface

    def _deg_to_polar(self, angle_in_degrees):
        """Converts degrees into polar coodrinates.

        Parameters
        ----------
        angle_in_degrees : int
            angle in degrees

        Returns
        -------
        angle : int
            angle in polar coordinates

        """

        a = angle_in_degrees / 180.0 * math.pi
        return (math.cos(a) , math.sin(a))

    def _get_circle_position(self, center, radius, angle):
        """Returns the position in the circle.

        Parameters
        ----------
        center : (int, int)
            center of the circle
        radius : (int, int)
            radius of the circle
        angle : int
            angle to compute

        Returns
        -------
        pos : int

        """

        angle = angle - 90
        p = self._deg_to_polar(angle)
        return (int(center[0] + p[0] * radius),
                int(center[1] - p[1] * radius))

    def make(self, shuffle=True, jitter=True):
        """Make the circle.

        Parameters
        ----------
        shuffle : bool, optional
            if True, positions will be shuffled (default = True)
        jitter : bool, optional
            if True, positions will be rotated between 0 and 1 step
            (default = True)

        """

        random.seed()
        step = 360 / float(len(self._stimuli))
        offset = 0
        if jitter:
            offset = random.randint(0, int(step))
        pos_list = [c for c, _s in enumerate(self._stimuli)]
        if shuffle:
            random.shuffle(pos_list)
        size = self.surface_size
        center = (size[0] // 2, size[1] // 2)
        for i, elem in enumerate(pos_list):
            d = offset + i * step
            xy = self._get_circle_position(center, self._radius, d)
            self._stimuli[elem].position = (xy[0] - size[0] // 2,
                                            xy[1] - size[1] // 2)


if __name__ == "__main__":
    from ...stimuli._textline import TextLine
    from ... import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    stims = []
    for i in range(0, 25):
        stims.append(TextLine("A"))
    stimuluscircle = StimulusCircle(radius=200, stimuli=stims)
    stimuluscircle.make()
    stimuluscircle.present()
    exp.clock.wait(1000)
