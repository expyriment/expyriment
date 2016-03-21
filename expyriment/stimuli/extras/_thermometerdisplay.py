#!/usr/bin/env python

"""
A thermometer display stimulus.

This module contains a class implementing a thermometer display stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import pygame

from . import defaults
from ...stimuli import Rectangle
from ...stimuli._visual import Visual


class ThermometerDisplay(Visual):
    """A class implementing a thermometer display."""

    def __init__(self, state, goal=None, size=None, nr_segments=None,
                 gap=None, frame_line_width=None, active_colour=None,
                 inactive_colour=None, frame_colour=None, goal_colour=None,
                 gap_colour=None, position=None):
        """Initializing a thermometer display.

        Parameters:
        -----------
        state : int
            The state of the thermometer in percent.
        goal : int, optional
            The goal state indication in percent.
        size : (int, int), optional
            The size of the thermometer display.
        nr_segments : int, optional
            The number of segments to use.
        gap : int, optional
            The visual gap between the individual segments.
        frame_line_width : int, optional
            The line width of the frame around the thermometer display.
        active_colour : (int, int, int), optional
            The colour of the active segments.
        inactive_colour : (int, int, int), optional
            The colour of the inactive segments.
        frame_colour : (int, int, int), optional
            The colour of the frame around the thermometer display.
        goal_colour : (int, int, int), optional
            The colour of the goal indicator.
        gap_colour : (int, int, int), optional
            The gap colour of the thermometer stimulus.
        position : (int, int), optional
            The position of the thermometer display.
        """

        self._state = state
        if goal is not None:
            self._goal = goal
        else:
            self._goal = defaults.thermometerdisplay_goal
        if size is not None:
            self._size = size
        else:
            self._size = defaults.thermometerdisplay_size
        if nr_segments is not None:
            self._nr_segments = nr_segments
        else:
            self._nr_segments = defaults.thermometerdisplay_nr_segments
        if gap is not None:
            self._gap = gap
        else:
            self._gap = defaults.thermometerdisplay_gap
        if frame_line_width is not None:
            self._frame_line_width = frame_line_width
        else:
            self._frame_line_width = \
                defaults.thermometerdisplay_frame_line_width
        if active_colour is not None:
            self._active_colour = active_colour
        else:
            self._active_colour = defaults.thermometerdisplay_active_colour
        if inactive_colour is not None:
            self._inactive_colour = inactive_colour
        else:
            self._inactive_colour = \
                defaults.thermometerdisplay_inactive_colour
        if frame_colour is not None:
            self._frame_colour = frame_colour
        else:
            self._frame_colour = defaults.thermometerdisplay_frame_colour
        if goal_colour is not None:
            self._goal_colour = goal_colour
        else:
            self._goal_colour = defaults.thermometerdisplay_goal_colour
        if gap_colour is not None:
            self._gap_colour = gap_colour
        else:
            self._gap_colour = defaults.thermometerdisplay_gap_colour
        if position is not None:
            self._position = position
        else:
            self._position = defaults.thermometerdisplay_position

        Visual.__init__(self, position)

    _getter_exception_message = "Cannot set {0} if surface exists!"

    @property
    def state(self):
        """Getter for state."""
        return self._state

    @state.setter
    def state(self, value):
        """Setter for state."""

        if self.has_surface:
            raise AttributeError(
                ThermometerDisplay._getter_exception_message.format("state"))
        else:
            self._state = value


    @property
    def goal(self):
        """Getter for goal."""
        return self._goal

    @goal.setter
    def goal(self, value):
        """Setter for goal."""

        if self.has_surface:
            raise AttributeError(
                ThermometerDisplay._getter_exception_message.format("goal"))
        else:
            self._goal = value

    @property
    def size(self):
        """Getter for size."""
        return self._size

    @size.setter
    def size(self, value):
        """Setter for size."""

        if self.has_surface:
            raise AttributeError(
                ThermometerDisplay._getter_exception_message.format("size"))
        else:
            self._size = value

    @property
    def nr_segments(self):
        """Getter for nr_segments."""
        return self._nr_segments

    @nr_segments.setter
    def nr_segments(self, value):
        """Setter for nr_segments."""

        if self.has_surface:
            raise AttributeError(
                ThermometerDisplay._getter_exception_message.format(
                    "nr_segments"))
        else:
            self._nr_segments = value

    @property
    def gap(self):
        """Getter for gap."""
        return self._gap

    @gap.setter
    def gap(self, value):
        """Setter for gap."""

        if self.has_surface:
            raise AttributeError(
                ThermometerDisplay._getter_exception_message.format("gap"))
        else:
            self._gap = value

    @property
    def frame_line_width(self):
        """Getter for frame_line_width."""
        return self._frame_line_width

    @frame_line_width.setter
    def frame_line_width(self, value):
        """Setter for frame_line_width."""

        if self.has_surface:
            raise AttributeError(
                ThermometerDisplay._getter_exception_message.format(
                    "frame_line_width"))
        else:
            self._frame_line_width = value

    @property
    def active_colour(self):
        """Getter for active_colour."""
        return self._active_colour

    @active_colour.setter
    def active_colour(self, value):
        """Setter for active_colour."""

        if self.has_surface:
            raise AttributeError(
                ThermometerDisplay._getter_exception_message.format(
                    "active_colour"))
        else:
            self._active_colour = value

    @property
    def inactive_colour(self):
        """Getter for inactive_colour."""
        return self._inactive_colour

    @inactive_colour.setter
    def inactive_colour(self, value):
        """Setter for inactive_colour."""

        if self.has_surface:
            raise AttributeError(
                ThermometerDisplay._getter_exception_message.format(
                    "inactive_colour"))
        else:
            self._inactive_colour = value

    @property
    def frame_colour(self):
        """Getter for frame_colour."""
        return self._frame_colour

    @frame_colour.setter
    def frame_colour(self, value):
        """Setter for frame_colour."""

        if self.has_surface:
            raise AttributeError(
                ThermometerDisplay._getter_exception_message.format(
                    "frame_colour"))
        else:
            self._frame_colour = value

    @property
    def goal_colour(self):
        """Getter for goal_colour."""
        return self._goal_colour

    @goal_colour.setter
    def goal_colour(self, value):
        """Setter for goal_colour."""

        if self.has_surface:
            raise AttributeError(
                ThermometerDisplay._getter_exception_message.format(
                    "goal_colour"))
        else:
            self._goal_colour = value

    @property
    def gap_colour(self):
        """Getter for gap_colour."""
        return self._gap_colour

    @gap_colour.setter
    def gap_colour(self, value):
        """Setter for gap_colour."""

        if self.has_surface:
            raise AttributeError(
                ThermometerDisplay._getter_exception_message.format(
                    "gap_colour"))
        else:
            self._gap_colour = value

    def _create_surface(self):
        """Create the surface of the stimulus."""

        surface = pygame.surface.Surface((self._size[0] +
                                          self._frame_line_width,
                                          self._size[1] +
                                          self._frame_line_width),
                                         pygame.SRCALPHA).convert_alpha()

        if self._gap_colour is not None:
            surface.fill(self._gap_colour)

        parts = []
        width = self._size[0] - self._frame_line_width - \
                2 * self._frame_line_width % 2
        height = self._size[1] - self._frame_line_width - \
                 2 * self._frame_line_width % 2 + 1
        s_height = int(height - (self._nr_segments + 1) *
                       self._gap) // self._nr_segments
        for x in range(self._nr_segments):
            if x < self._state / 100.0 * self._nr_segments:
                colour = self._active_colour
            else:
                colour = self._inactive_colour
            s = Rectangle((width - self._gap * 2,
                           s_height), colour=colour,
                          position=(0, -height // 2 + s_height // 2 + x *
                                    height // self.nr_segments + self._gap))
            parts.append(s)
        parts.append(Rectangle(self._size, colour=self._frame_colour,
                               line_width=self._frame_line_width,
                               position=self._position))
        parts.append(Rectangle((width - self._gap, height - self._gap * 2),
                               colour=self._gap_colour,
                               line_width=self._gap,
                               position=self._position))

        if self._goal is not None:
            x = int(round(self._goal / 100.0 * self._nr_segments)) - 1
            current_y_pos = -height // 2 + s_height // 2 + \
                            x * height // self._nr_segments + self._gap
            above_y_pos = -height // 2 + s_height // 2 + \
                          (x + 1) * height // self._nr_segments + self._gap
            g1 = Rectangle((self._frame_line_width * 1.25,
                            self._frame_line_width * 1.25),
                           colour=self._goal_colour,
                           position=(
                               -self._size[0] // 2 - self._frame_line_width // 2,
                               (current_y_pos + above_y_pos) // 2))
            g2 = Rectangle((self._frame_line_width * 1.25,
                            self._frame_line_width * 1.25),
                           colour=self._goal_colour,
                           position=(
                               self._size[0] // 2 + self._frame_line_width // 2,
                               (current_y_pos + above_y_pos) // 2))
            g1.rotate(45)
            g2.rotate(45)
            parts.append(g1)
            parts.append(g2)

        for stim in parts:
            stim.rect = pygame.Rect((0, 0), stim.surface_size)
            surface_size = surface.get_size()
            stim.rect.center = [stim.position[0] + surface_size[0] // 2,
                                - stim.position[1] + surface_size[1] // 2]
            surface.blit(stim._get_surface(), stim.rect)
        return surface


if __name__ == "__main__":
    from ... import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    thermometer_display = ThermometerDisplay(50, 50)
    thermometer_display.present()
    #exp.clock.wait(1000)
    exp.keyboard.wait()