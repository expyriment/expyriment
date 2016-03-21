"""
Audio playback.

This module contains a class implementing audio playback.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import os

try:
    import android.mixer as mixer
except:
    import pygame.mixer as mixer
from .. import _globals
from ..misc import unicode2byte
from ._stimulus import Stimulus


class Audio(Stimulus):
    """A class implementing a general auditory stimulus.

    Notes
    -----
    See also

        - expyriment.control.start_audiosystem
        - expyriment.control.stop_audiosystem
        - expyriment.control.audiosystem_is_busy
        - expyriment.control.audiosystem_wait_end

    """

    def __init__(self, filename):
        """Create an audio stimulus.

        Parameters
        ----------
        filename : str
            the filename

        """

        Stimulus.__init__(self, filename)
        self._filename = filename
        self._file = None
        self._is_preloaded = False
        if not(os.path.isfile(self._filename)):
            raise IOError("The audio file {0} does not exists".format(
                unicode2byte(self._filename)))

    _getter_exception_message = "Cannot set {0} if preloaded!"

    @property
    def is_preloaded(self):
        """Getter for is_preloaded"""

        return self._is_preloaded

    @property
    def filename(self):
        """Getter for filename"""

        return self._filename

    @filename.setter
    def filename(self, value):
        """Setter for filename."""

        if self._is_preloaded:
            raise AttributeError(Audio._getter_exception_message.format(
                "filename"))
        else:
            self._filename = value

    def copy(self):
        """Copy the stimulus.

        Returns
        -------
        copy: stimulus.Audio
            Returned copy will NOT be is_preloaded!

        """

        was_loaded = self._is_preloaded
        self.unload()
        rtn = Stimulus.copy(self)
        if was_loaded:
            self.preload()
        return rtn

    def preload(self):
        """Preload stimulus to memory."""

        if not self._is_preloaded:
            self._file = mixer.Sound(unicode2byte(self._filename, fse=True))
            self._is_preloaded = True

    def unload(self, **kwargs):
        """Unload stimulus from memory.

        This removes the reference to the object in memory.
        It is up to the garbage collector to actually remove it from memory.

        """

        if self._is_preloaded:
            self._file = None
            self._is_preloaded = False

    def play(self, loops=0, maxtime=0, fade_ms=0):
        """Play the audio stimulus.

        The function returns immediately after the sound started to play.
        A pygame.mixer.Channel object is returned.

        Parameters
        ----------
        loops : int, optional
            how often to repeat (-1 = forever) (default = 0)
        maxtime : int
            stop after given amount of milliseconds (default = 0)
        fade_ms : int, optional
            fade in time in milliseconds (default = 0)

        """

        if not self._is_preloaded:
            self.preload()
        rtn = self._file.play(loops, maxtime, fade_ms)
        if self._logging:
            if isinstance(self._filename, str):
                import sys
                filename = self._filename.encode(sys.getfilesystemencoding())
            else:
                filename = self._filename

            _globals.active_exp._event_file_log(
                "Stimulus,played,{0}".format(filename), 1)
        return rtn

    def stop(self):
        """Stop the audio stimulus"""

        if self._is_preloaded:
            self._file.stop()

    def present(self):
        """Presents the sound.

        The function is identical to Audio.play(loops=0, maxtime=0, fade_ms=0)
        and returns also immediately after the sound started to play.

        Notes
        -----
        See Audio.play for more information.

        """

        self.play()
