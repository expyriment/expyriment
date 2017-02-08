#!/usr/bin/env python

"""
A random dot kinematogram (stimulus-like).

This module contains a class implementing a random dot kinematogram.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import math
import random

from . import defaults

from ...io import Keyboard
from ...stimuli import Canvas, Circle
from ...stimuli._stimulus import Stimulus
from ...misc import Clock



class RandomDotKinematogram(Stimulus):
    """Random Dot Kinematogram"""

    def __init__(self, area_radius, n_dots, target_direction, target_dot_ratio,
                position = None, dot_speed = None, dot_lifetime = None,
                dot_radius = None, dot_colour=None,
                background_colour = None, north_up_clockwise = None):
        """Create a Random Dot Kinematogram

        Parameters:
        -----------
        area_radius : int
            the radius of the stimulus area
        n_dots : int
            number of moving dots
        target_direction : int, float (0-360)
            movement target direction in degrees
        target_dot_ratio : float (0-1)
            ratio of dots that move consistently in the same target direction
            (the rest of the target moves in a random direction)
            can be sometimes only approximated! self.target_dot_ratio returns the
            precise actual target dot ratio
        position : (int, int), optional
            position of the stimulus
        dot_speed : int, optional
            the moving speed in pixel per second (default=100)
        dot_lifetime : int, optional
            the time the object lives in milliseconds (default 400)
        dot_radius : int, optional
            radius of the dots (default = 3)
        dot_colour : (int, int, int), optional
            colour (RGB) of the dots (default=experiment.foreground_colour)
        background_colour : (int, int, int), optional
            colour (RGB) of the background (default=experiment.background_colour)
        north_up_clockwise : bool, optional
            if true (default) all directional information refer to an
            north up and clockwise system
            otherwise 0 is right, counterclockwise (default=True)

        Notes:
        ------
        Logging is switch off per default

        """
        if dot_speed is None:
            dot_speed = defaults.randomdotkinematogram_dot_speed
        if dot_lifetime is None:
            dot_lifetime = defaults.randomdotkinematogram_dot_lifetime
        if dot_radius is None:
            dot_radius = defaults.randomdotkinematogram_dot_radius
        if dot_colour is None:
            dot_colour = defaults.randomdotkinematogram_dot_colour
        if north_up_clockwise is None:
            north_up_clockwise = defaults.randomdotkinematogram_north_up_clockwise
        if position is None:
            position = defaults.randomdotkinematogram_position
        if background_colour is None:
            background_colour = defaults.randomdotkinematogram_background_colour

        self.area_radius = area_radius
        self.dot_speed = dot_speed
        self.dot_lifetime = dot_lifetime
        self.dot_radius = dot_radius
        self.dot_colour = dot_colour
        self.north_up_clockwise = north_up_clockwise
        self._canvas = Canvas(size=(2*(self.area_radius + self.dot_radius),
                                    2*(self.area_radius + self.dot_radius)),
                                    position=position, colour=background_colour)
        self.reset(n_dots=n_dots, target_direction=target_direction,
                        target_dot_ratio=target_dot_ratio)
        self.set_logging(False)

    def reset(self, n_dots, target_direction, target_dot_ratio):
        """Reset and recreate dot pattern

        Parameters:
        -----------
        n_dots : int
            number of moving dots
        target_direction : int, float (0-360)
            movement target direction in degrees
        target_dot_ratio : float (0-1)
            ratio of dots that move consistently in the same target direction
            (the rest of the target moves in a random direction)
            can be sometimes only approximated! self.target_dot_ratio returns the
            precise actual target dot ratio

        """
        self.target_direction = target_direction
        self.dots = [self._make_random_dot(direction=None) for x in range(n_dots)]
        self.target_dot_ratio = target_dot_ratio

    def reset_all_ages(self, randomize_ages=False):
        """Reset all ages (born at current time) and randomize start age if required"""
        map(lambda x : x.reset_age(randomize_age=randomize_ages), self.dots)

    @property
    def n_dots(self):
        """Getter for n_dots."""
        return len(self.dots)

    @property
    def logging(self):
        """Getter for logging."""
        return self._canvas.logging

    def set_logging(self, onoff):
        """Set logging of this object on or off

        Parameters:
        -----------
        onoff : bool
            set logging on (True) or off (False)

        """
        self._canvas.set_logging(onoff)

    @property
    def n_target_dots(self):
        return sum([int(x.is_target) for x in self.dots])

    @property
    def target_dot_ratio(self):
        """Getter for target dot ratio"""
        return self.n_target_dots / float(len(self.dots))

    @target_dot_ratio.setter
    def target_dot_ratio(self, value):
        if value<0:
            value = 0
        if value > 1:
            value = 1
        curr_n_targets = self.n_target_dots
        goal_n_targets = int(len(self.dots) * value)
        while goal_n_targets != curr_n_targets:
            if goal_n_targets > curr_n_targets:
                # remove non target and add target
                for d in self.dots:
                    if not d.is_target:
                        self.dots.remove(d)
                        break
                d = self._make_random_dot(direction=self.target_direction, randomize_age=True)
                d.is_target = True
                self.dots.append(d)
            elif goal_n_targets < curr_n_targets:
                # remove a target and add non target
                for d in self.dots:
                    if d.is_target:
                        self.dots.remove(d)
                        break
                self.dots.append(self._make_random_dot(direction=None, randomize_age=True))
            curr_n_targets = self.n_target_dots

    @property
    def last_stimulus(self):
        """Getter for the last plotted stimulus"""
        return self._canvas

    def _make_random_dot(self, direction=None, randomize_age=False):
        """make a random dot"""
        while (True):
            pos = (int(self.area_radius - random.random()*2*self.area_radius),
              int(self.area_radius - random.random()*2*self.area_radius))
            if math.hypot(pos[0],pos[1])< self.area_radius:
                break
        if direction is None:
            direction = random.random() * 360
        rtn = MovingPosition(position=pos,
                        direction=direction,
                        speed = self.dot_speed,
                        lifetime = self.dot_lifetime,
                        north_up_clockwise=self.north_up_clockwise)
        if randomize_age:
            rtn.reset_age(randomize_age=True)
        return rtn

    def make_frame(self, background_stimulus=None):
        """Make new frame. The function creates the current random dot kinematogram
        and returns it as Expyriment stimulus.

        Parameters:
        -----------
        background_stimulus : Expyriment stimulus, optional
            optional stimulus to be plotted in the background
            (default=None)

        Notes:
        ------
        Just loop this function and plot the returned stimulus.
        See present_and_wait_keyboard

        Returns:
        --------
        stimulus : return the current as Expyriment stimulus
        """
        self._canvas.clear_surface()
        if background_stimulus is not None:
            background_stimulus.plot(self._canvas)

        def _process_dot(d):
            if d.is_dead or d.is_outside(self.area_radius):
                if d.is_target:
                    d = self._make_random_dot(direction=d.direction)
                    d.is_target = True
                else:
                    d = self._make_random_dot()
            Circle(position = d.position, radius=self.dot_radius,
                        colour=self.dot_colour).plot(self._canvas)
            return d
        self.dots = list(map(_process_dot, self.dots))
        return self._canvas

    def present_and_wait_keyboard(self, background_stimulus=None,
                        check_keys = None,
                        change_parameter=(None, None),
                        duration=None, button_box=None):
        """Present the random dot kinematogram and wait for keyboard press.

        Parameters:
        -----------
        background_stimulus : Expyriment stimulus, optional
            optional stimulus to be plotted in the background
            (default=None)
        check_keys : int or list, optional
            a specific key or list of keys to check
        change_parameter : tuple (int, int), optional, default = (None, None)
            [step size (target dot ratio), step interval (ms)]
            if both parameter are defined (not None), target dot ratio changes
            accordingly while presentation
        duration: int, optional
            maximum duration to wait for keypress
        button_box: expyriment io.ButtonBox object, optional
            if not the keyboard but a button_box should be used
            (e.g. io.StreamingButtonBox)

        """
        from ... import _internals
        RT = Clock()
        if button_box is None:
            button_box = _internals.active_exp.keyboard
        button_box.clear()
        self.reset_all_ages(randomize_ages=True)
        last_change_time = RT.stopwatch_time
        while(True):
            if None not in change_parameter:
                if RT.stopwatch_time >= change_parameter[1] + last_change_time:
                    last_change_time = RT.stopwatch_time
                    self.target_dot_ratio = self.target_dot_ratio + \
                                    change_parameter[0]
            self.make_frame(background_stimulus=background_stimulus).present()

            if isinstance(button_box, Keyboard):
                key = button_box.check(keys=check_keys)
            else:
                _internals.active_exp.keyboard.process_control_keys()
                key = button_box.check(codes=check_keys)

            if key is not None:
                break
            if duration is not None and RT.stopwatch_time >= duration:
                return (None, None)
        return key, RT.stopwatch_time



class MovingPosition(object):

    def __init__(self, position, direction, speed, lifetime, extra_age=0,
                            north_up_clockwise = True,
                            is_target=False):
        """Create a MovingPosition

        Parameters
        ----------
        position : (int, int)
            start position
        direction : int, float (0-360)
            movement direction in degrees
        speed : int
            the moving speed in pixel per second
        lifetime : int
            the time the object lives in milliseconds
        extra_age : int, optional
            the object can have already an age when creating or resetting
            (default=0)
        north_up_clockwise : bool, optional
            if true (default) all directional information refer to an
            north up and clockwise system
            otherwise 0 is right, counterclockwise (default=True)
        is_target : bool
            target position

        """
        self._start_position = list(position)
        self.lifetime = lifetime
        self.extra_age = extra_age # add extra age for shorter lifetime
        self.is_target = is_target
        self._speed = speed
        self._north_up_clockwise = north_up_clockwise,
        self._direction = direction
        self._update_movement_vector()
        self._clock = Clock()

    @property
    def is_dead(self):
        """Return True is lifetime of the object is over"""
        return (self.age >= self.lifetime)

    @property
    def age(self):
        """Return the age of a dot"""
        return self._clock.stopwatch_time + self.extra_age

    def reset_age(self, randomize_age=False):
        """Reset the age to zero (born at current time) or if randomize_age=True, age will randomized."""
        if randomize_age:
            self.extra_age = int(random.random() * self.lifetime)
        self._clock.reset_stopwatch()

    def is_outside(self, the_range):
        """Return True the object is outside the range from (0,0)"""
        pos = self.position
        return (math.hypot(pos[0], pos[1])>=the_range)

    @property
    def north_up_clockwise(self):
        """getter for north up and clockwise"""
        return self._north_up_clockwise

    @property
    def position(self):
        """The current position (depends on time).
        Note: This property changes continuously over time, since the
        position is moving.

        """
        return (self._start_position[0] + self._clock.stopwatch_time *
                            self._movement_vector[0],
            self._start_position[1] + self._clock.stopwatch_time *
                            self._movement_vector[1])

    @property
    def direction(self):
        """Getter for direction."""
        return self._direction

    @property
    def speed(self):
        """Getter for speed."""
        return self._speed

    @direction.setter
    def direction(self, x):
        self._direction = x
        self._update_movement_vector()

    @speed.setter
    def speed(self, x):
        """speed in pix per second"""
        self._speed = x
        self._update_movement_vector()

    def _update_movement_vector(self):
        if self._north_up_clockwise:
            direction = 450 - self._direction
        else:
            direction = self._direction
        angle = direction * math.pi / 180.0
        speed = self._speed / 1000.0
        self._movement_vector = (speed * math.cos(angle),
                                 speed * math.sin(angle))



if __name__ == "__main__":
    from .. import control, design
    control.set_develop_mode(True)
    exp = control.initialize()
    direction = design.randomize.rand_int(0, 360)
    # first rdk stimulus with 20% consitencyin random direction
    rdk = RandomDotKinematogram(area_radius=200, n_dots=150,
          target_direction = direction,
          target_dot_ratio = 0.20,
          dot_speed = 80, dot_lifetime = 600,
          dot_radius = 3, dot_colour=None)
    key, rt = rdk.present_and_wait_keyboard()

    # smae direct buy with 80% consitency
    rdk = RandomDotKinematogram(area_radius=200, n_dots=150,
          target_direction = direction,
          target_dot_ratio = 0.80,
          dot_speed = 80, dot_lifetime = 600,
          dot_colour = None)
    key, rt = rdk.present_and_wait_keyboard()
    print(direction)