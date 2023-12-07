"""
Audio playback.

This module contains a class implementing audio playback.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import os

try:
    import android.mixer as mixer
except Exception:
    import pygame.mixer as mixer
from .. import _internals
from ..misc import unicode2byte
from ._stimulus import Stimulus


class Audio(Stimulus):
    """A class implementing a general auditory stimulus.

    See Also
    --------
    expyriment.control.start_audiosystem
    expyriment.control.stop_audiosystem
    expyriment.control.get_audiosystem_is_playing
    expyriment.control.wait_end_audiosystem

    """

    def __init__(self, filename):
        """Create an audio stimulus.

        Parameters
        ----------
        filename : str
            the filename. Must be an .ogg or uncompressed .wav file.

        """
        if os.path.splitext(filename)[1] not in ('.wav', '.ogg'):
            raise ValueError("The audio file must be an .ogg or uncompressed .wav file")

        Stimulus.__init__(self, filename)
        self._filename = filename
        self._file = None
        self._is_preloaded = False
        if not(os.path.isfile(self._filename)):
            raise IOError(u"The audio file {0} does not exists".format(
                self._filename))

    _getter_exception_message = "Cannot set {0} if preloaded!"

    @property
    def is_preloaded(self):
        """Getter for is_preloaded."""

        return self._is_preloaded

    @property
    def filename(self):
        """Getter for filename."""

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
        copy: expyriment.stimuli.Audio
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
        # Due to a bug in handling file names in PyGame 1.9.2, we pass a file
        # handle to PyGame. See also:
        # https://github.com/expyriment/expyriment/issues/81
            with open(self._filename, 'rb') as f:
                self._file = mixer.Sound(f)
            self._is_preloaded = True

    def unload(self, **kwargs):
        """Unload stimulus from memory.

        This removes the reference to the object in memory.
        It is up to the garbage collector to actually remove it from memory.

        """

        if self._is_preloaded:
            self._file = None
            self._is_preloaded = False

    def play(self, loops=0, maxtime=0, fade_ms=0, log_event_tag=None):
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
        log_event_tag : numeral or string, optional
            if log_event_tag is defined and if logging is switched on for this
            stimulus (default), a summary of the inter-event-intervalls are
            appended at the end of the event file

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

            _internals.active_exp._event_file_log(
                "Stimulus,played,{0}".format(filename), 1,
                                 log_event_tag=log_event_tag)
        return rtn

    def stop(self):
        """Stop the audio stimulus"""

        if self._is_preloaded:
            self._file.stop()

    def present(self, log_event_tag=None):
        """Presents the sound.

        The function is identical to Audio.play(loops=0, maxtime=0, fade_ms=0)
        and returns also immediately after the sound started to play.

        Notes
        -----
        See Audio.play for more information.

        """

        self.play(log_event_tag=log_event_tag)
