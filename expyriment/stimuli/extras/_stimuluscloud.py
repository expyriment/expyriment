#!/usr/bin/env python

"""
A stimulus cloud stimulus.

This module contains a class implementing a stimulus cloud stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import random

import pygame

from . import defaults
from ... import _internals
from ...stimuli._visual import Visual


class StimulusCloud(Visual):
    """A stimulus cloud class.

    This class produces a cloud of ANY visual stimuli.
    The cloud will be of rectengular shape!

    """

    def __init__(self, size=None, position=None, background_colour=None):
        """Create a stimulus cloud.

        Parameters
        ----------
        size : (int, int), optional
            size of the cloud
        position : (int, int), optional
            position of the cloud
        background_colour : (int, int, int), optional
            colour of the background

        """

        Visual.__init__(self, position)
        self._cloud = []
        if size is not None:
            self._size = size
        else:
            size = defaults.stimuluscloud_size
            if size is None:
                try:
                    self._size = _internals.active_exp.screen.surface.get_size()
                except:
                    raise RuntimeError("Could not get size of screen!")
        if background_colour is not None:
            self._background_colour = background_colour
        else:
            self._background_colour = \
                    defaults.stimuluscloud_background_colour
        self._rect = None

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def size(self):
        """Getter for size."""
        return self._size

    @size.setter
    def size(self, value):
        """Setter for size."""

        if self.has_surface:
            raise AttributeError(
                StimulusCloud._getter_exception_message.format("size"))
        else:
            self._size = value
    @property
    def background_colour(self):
        """Getter for background_colour."""
        return self._background_colour

    @background_colour.setter
    def background_colour(self, value):
        """Setter for background_colour."""

        if self.has_surface:
            raise AttributeError(
                StimulusCloud._getter_exception_message.format("background_colour"))
        else:
            self._background_colour = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        surface = pygame.surface.Surface(self.size,
                                        pygame.SRCALPHA).convert_alpha()
        if self.background_colour is not None:
            surface.fill(self.background_colour)
        for stim in self._cloud:
            stim.rect = pygame.Rect((0, 0), stim.surface_size)
            surface_size = surface.get_size()
            stim.rect.center = [stim.position[0] + surface_size[0] // 2,
                                - stim.position[1] + surface_size[1] // 2]
            surface.blit(stim._get_surface(), stim.rect)
        return surface

    def make(self, stimuli, min_distance=None):
        """Make the cloud by randomly putting stimuli on it.

        Notes
        -----
        If min_distance is None, the stimuli will automatically spaced to not
        overlap. This will result in a long computation!
        Set the distance manually to space them wit a minimal distance between
        centers. This will result in a way shorter computation!

        This will build surfaces for all stimuli in the cloud!

        Parameters
        ----------
        stimuli : list
            list of stimuli to put in the cloud
        min_distance : int, optional
            minimal allowed distance between stimuli

        """

        surface = pygame.surface.Surface(self.size,
                                         pygame.SRCALPHA).convert_alpha()
        surface.fill((0, 0, 0))
        self._set_surface(surface)
        remix = 0
        while(True): #remix-loop
            self._cloud = []
            remix = remix + 1
            for stimulus in stimuli:
                reps = 0
                stimulus._set_surface(stimulus._get_surface())
                while(True): #find a solution
                    stimulus.position = (random.randint(-self.size[0] // 2,
                                                        self.size[0] // 2),
                                         random.randint(-self.size[1] // 2,
                                                        self.size[1] // 2))
                    reps = reps + 1
                    if stimulus.inside_stimulus(self):
                        okay = True
                        if min_distance is None:
                            for s in self._cloud:
                                if stimulus.overlapping_with_stimulus(s)[0]:
                                    okay = False
                                    break
                        else:
                            for s in self._cloud:
                                if stimulus.distance(s) < min_distance:
                                    okay = False
                                    break
                        if okay:
                            self._cloud.append(stimulus)
                            reps = 0
                            if len(self._cloud) == len(stimuli):
                                self.clear_surface()
                                return True
                            break
                    if reps > 10000:
                        break

            if (remix > 10):
                message = "Stimuluscloud make: Cannot find a solution."
                print(("Warning: ", message))
                return False

    def shuffel_surface_sequence(self, from_idx=0, to_idx= -1):
        """Shuffle the surfaces sequence.

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
    from ...stimuli._textline import TextLine
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    stimuluscloud = StimulusCloud()
    stims = []
    for i in range(0, 25):
        stims.append(TextLine("A"))
    stimuluscloud.make(stims)
    stimuluscloud.present()
    exp.clock.wait(1000)
