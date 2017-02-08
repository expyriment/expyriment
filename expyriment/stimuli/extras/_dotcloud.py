#!/usr/bin/env python

"""
A dotcloud stimulus.

This module contains a class implementing a dotcloud stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import random
import pygame

from ... import _internals, stimuli
from ...stimuli._visual import Visual
from ...stimuli._circle import Circle
from . import  defaults


class DotCloud(Visual):
    """A dot cloud class.

    This class creates dots arranged in a circular cloud.

    """

    def __init__(self, radius=None, position=None, background_colour=None,
                 dot_colour=None):
        """Create a dot cloud.

        Parameters
        ----------
        radius : int, optional
            radius of the cloud
        position : (int, int), optional
            position of the stimulus
        background_colour : (int, int, int), optional
            colour of the background
        dot_colour : (int, int, int), optional
            colour of the dots.

        """

        Visual.__init__(self, position)
        self._cloud = []
        if radius is not None:
            self._radius = radius
        else:
            radius = defaults.dotcloud_radius
            if radius is None:
                try:
                    self._radius = min(
                        _internals.active_exp.screen.surface.get_size()) // 2
                except:
                    raise RuntimeError("Could not get size of screen!")
        if background_colour is not None:
            self._background_colour = background_colour
        else:
            self._background_colour = \
                    defaults.dotcloud_background_colour
        if dot_colour is None:
            dot_colour = defaults.dotcloud_dot_colour
        if dot_colour is not None:
            self._dot_colour = dot_colour
        else:
            self._dot_colour = _internals.active_exp.foreground_colour
        self.create_area()

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def radius(self):
        """Getter for radius."""

        return self._radius

    @radius.setter
    def radius(self, value):
        """Setter for radius."""

        if self.has_surface:
            raise AttributeError(DotCloud._getter_exception_message.format(
                "radius"))
        else:
            self._radius = value
            self.create_area()

    @property
    def background_colour(self):
        """Getter for background_colour."""

        return self._background_colour

    @background_colour.setter
    def background_colour(self, value):
        """Setter for background_colour."""

        if self.has_surface:
            raise AttributeError(DotCloud._getter_exception_message.format(
                "background_colour"))
        else:
            self._background_colour = value
            self.create_area()

    @property
    def dot_colour(self):
        """Getter for dot_colour."""

        return self._dot_colour

    @dot_colour.setter
    def dot_colour(self, value):
        """Setter for dot_colour."""

        if self.has_surface:
            raise AttributeError(DotCloud._getter_exception_message.format(
                "dot_colour"))
        else:
            self._dot_colour = value
            self.create_area()

    @property
    def area(self):
        """Getter for area."""

        return self._area

    def _create_surface(self):
        """Create the surface of the stimulus."""

        surface = self.area._get_surface()
        for dot in self._cloud:
            dot.rect = pygame.Rect((0, 0), dot.surface_size)
            surface_size = surface.get_size()
            dot.rect.center = [dot.position[0] + surface_size[0] // 2,
                               dot.position[1] + surface_size[1] // 2]
            surface.blit(dot._get_surface(), dot.rect)
        return surface

    def create_area(self):
        """Create the area of the cloud (a dot object itself)."""

        self._area = Circle(radius=self._radius,
                         position=(0, 0),
                         colour=self._background_colour)
        stimuli._stimulus.Stimulus._id_counter -= 1
        self._area._set_surface(pygame.surface.Surface(
            (self.radius * 2, self.radius * 2),
            pygame.SRCALPHA).convert_alpha())
        if self._background_colour is not None:
            pygame.draw.circle(self._area._get_surface(), self._background_colour,
                               (self._radius, self._radius), self._radius)

    def _is_overlapping_with_point(self, dot, gap):
        """Return True if a dot in the cloud is overlapping with another dot.

        Parameters
        ----------
        dot : stimuli.dot
            the other dot
        gap : int
            constant added to the distance

        Returns
        -------
        out : bool
            True if a dot in the cloud is overlapping with another dot

        """

        for elem in self._cloud:
            d = elem.distance(dot)
            if d <= (elem.radius + dot.radius + gap):
                return True
        return False

    def make(self, n_dots, dot_radius, gap=0, multi_colour=None):
        """Make the cloud by randomly putting dots on it.

        Parameters
        ----------
        n_dots : integer (or list of integers, if multi-colour cloud)
            number of dots to put into the cloud. In the case of a
            multi_colour cloud, the list n_dots specifies the distribution
            of the differently colours dots.
        dot_radius : int
            radius of the dots
        gap : int, optional
            gap between dots (default = 0)
        multi_colour : list of colours
            If the multi_colour list is defined, n_dots has to be a list of
            integers of the same length. The cloud comprises then dots
            in different colours according the specified distribution

        """

        if multi_colour is not None:
            dot_distribution = list(n_dots)
            if len(multi_colour) != len(n_dots):
                raise RuntimeError("Length of n_dots and multi_colours "+
                        "have to have the same length,")
            n_dots = sum(dot_distribution)

        top_left = dot_radius - self._radius
        bottom_right = self._radius - dot_radius
        remix = 0
        while True: #remix-loop
            self._cloud = []
            remix = remix + 1
            reps = 0
            while True: #find a solution
                if multi_colour is None:
                    dot = Circle(radius=dot_radius, colour = self._dot_colour)
                else:
                    # find colour counter
                    s = 0
                    for colour_cnt, d in enumerate(dot_distribution):
                        s += d
                        if len(self._cloud) < s:
                            break
                    dot = Circle(radius=dot_radius,
                                colour=multi_colour[colour_cnt])

                stimuli._stimulus.Stimulus._id_counter -= 1
                dot.position = (random.randint(top_left, bottom_right),
                                random.randint(top_left, bottom_right))
                reps = reps + 1

                if dot.inside_circle(self.area):
                    if not self._is_overlapping_with_point(dot, gap):
                        self._cloud.append(dot)
                        reps = 0
                if reps > 10000:
                    break
                if len(self._cloud) >= n_dots:
                    self.clear_surface()
                    return True

            if remix > 10:
                message = "Dotcloud make: Cannot find a solution."
                print(("Warning: ", message))
                if self._logging:
                    _internals.active_exp._event_file_log(message)
                return False

    def shuffel_dot_sequence(self, from_idx=0, to_idx= -1):
        """Shuffle the dots sequence.

        Parameters
        ----------
        from_idx : int, optional
            index to start from (default = 0)
        to_idx : int, optional
            index to end on (default = -1)

        """
        if (from_idx < 0):
            from_idx = 0
        if to_idx < from_idx or to_idx >= len(self._cloud):
            to_idx = len(self._cloud) - 1

        for x in range(from_idx, to_idx) :
            r = random.randint(from_idx, to_idx)
            self._cloud[r], self._cloud[x] = self._cloud[x], self._cloud[r]


if __name__ == "__main__":
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    dotcloud = DotCloud()
    dotcloud.make(25, 10)
    dotcloud.present()
    exp.clock.wait(1000)
