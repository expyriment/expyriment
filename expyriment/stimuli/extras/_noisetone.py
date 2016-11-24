#!/usr/bin/env python

"""
The noise tone stimulus module.

This module contains a class implementing a noise tone stimulus.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import os
import wave
import struct
import itertools
import tempfile
import shutil
import random

from . import defaults
from ...stimuli import defaults as stim_defaults
from ...stimuli._audio import Audio


class NoiseTone(Audio):
    """A class implementing a noise tone stimulus."""

    def __init__(self, duration, samplerate=None, bitdepth=None,
                 amplitude=None):
        """Create a noise tone.

        Parameters
        ----------
        duration : int
            duration of the noise tone in ms
        frequency : int, optional
            frequency of the noise tone
        samplerate : int, optional
            samplerate of the noise tone
        bitdepth : int, optional
            bitdeth of the noise tone
        amplitude : int, optional
            amplitude of the noise tone

        """

        self._duration = duration / 1000.0
        if samplerate is None:
            samplerate = defaults.noisetone_samplerate
        self._samplerate = samplerate
        if bitdepth is None:
            bitdepth = defaults.noisetone_bitdepth
        self._bitdepth = bitdepth
        if amplitude is None:
            amplitude = defaults.noisetone_amplitude
        self._amplitude = amplitude
        filename = self._create_noise_wave()
        Audio.__init__(self, filename)


    @property
    def duration(self):
        """Getter for duration."""

        return self._duration * 1000.0

    @duration.setter
    def duration(self, value):
        """Setter for duration."""

        if self.is_preloaded:
            raise AttributeError(Audio._getter_exception_message.format(
                "duration"))
        else:
            self._duration = value / 1000.0
            self._filename = self._create_sine_wave()


    @property
    def samplerate(self):
        """Getter for samplerate."""

        return self._samplerate

    @samplerate.setter
    def samplerate(self, value):
        """Setter for samplerate."""

        if self.is_preloaded:
            raise AttributeError(Audio._getter_exception_message.format(
                "samplerate"))
        else:
            self._samplerate = value
            self._filename = self._create_sine_wave()

    @property
    def bitdepth(self):
        """Getter for bitdepth."""

        return self._bitdepth

    @bitdepth.setter
    def bitdepth(self, value):
        """Setter for bitdepth."""

        if self.is_preloaded:
            raise AttributeError(Audio._getter_exception_message.format(
                "bitdepth"))
        else:
            self._bitdepth = value
            self._filename = self._create_sine_wave()

    @property
    def amplitude(self):
        """Getter for amplitude."""

        return self._amplitude

    @amplitude.setter
    def amplitude(self, value):
        """Setter for amplitude."""

        if self.is_preloaded:
            raise AttributeError(Audio._getter_exception_message.format(
                "amplitude"))
        else:
            self._amplitude = value
            self._filename = self._create_sine_wave()

    def _grouper(self, n, iterable, fillvalue=None):
        """Write in chunks."""

        args = [iter(iterable)] * n
        return itertools.zip_longest(fillvalue=fillvalue, *args)

    def _create_noise_wave(self):
        """Create the sine wave."""

        random.seed()
        noise = (float(self._amplitude) * random.uniform(-1, 1) for _ in \
                 itertools.count(0))
        channels = ((noise,),)
        n_samples = self._duration * self._samplerate
        samples = itertools.islice(zip(
            *(map(sum, zip(*channel)) \
              for channel in channels)), n_samples)
        fid, filename = tempfile.mkstemp(dir=stim_defaults.tempdir, suffix=".wav")
        os.close(fid)
        w = wave.open(filename, 'w')
        w.setparams((1, self._bitdepth // 8, self._samplerate, n_samples, 'NONE',
                     'not compressed'))
        max_amplitude = float(int((2 ** (self._bitdepth)) / 2) - 1)
        for chunk in self._grouper(2048, samples):
            frames = ''.join(''.join(struct.pack(
                'h', int(max_amplitude * sample)) for sample in channels) \
                for channels in chunk if channels is not None)
            w.writeframesraw(frames)
        w.close()
        return filename

    def save(self, filename):
        """Save the sine tone to a file.

        Parameters
        ----------
        filename : str
            filename the sine tone should be saved to

        """

        shutil.copy(self._filename, filename)


if __name__ == "__main__":
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    control.start_audiosystem()
    sine = NoiseTone(duration=1000)
    sine.present()
    exp.clock.wait(1000)
