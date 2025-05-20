"""
Audio playback.

This module contains a class implementing audio playback.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import os
from types import FunctionType

import pygame

from .. import _internals
from .._internals import CallbackQuitEvent
from ..misc import unicode2byte
from ..misc._timer import get_time
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
            filename (incl. path) of the audio file

        """

        Stimulus.__init__(self, filename)
        self._filename = filename
        self._file = None
        self._is_preloaded = False
        self._channel = None
        self._is_paused = False
        if not(os.path.isfile(self._filename)):
            raise IOError(u"The audio file {0} does not exists".format(
                self._filename))

    _getter_exception_message = "Cannot set {0} if preloaded!"

    @property
    def is_preloaded(self):
        """Getter for is_preloaded."""

        return self._is_preloaded

    @property
    def is_playing(self):
        """Property to check if audio is playing."""
        if self._is_preloaded and self._channel and not self._is_paused:
            return self._channel.get_busy()

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
        """Preload stimulus to memory.

        Returns
        -------
        time : int
            the time it took to execute this method

        """

        start = get_time()
        if not self._is_preloaded:
            # Due to a bug in handling file names introduced in PyGame 1.9.2,
            # we pass a file handle to PyGame. See also:
            # https://github.com/expyriment/expyriment/issues/81
            with open(self._filename, 'rb') as f:
                self._file = pygame.mixer.Sound(f)
            self._is_preloaded = True

        return int((get_time() - start) * 1000)

    def unload(self, **kwargs):
        """Unload stimulus from memory.

        This removes the reference to the object in memory.
        It is up to the garbage collector to actually remove it from memory.

        Returns
        -------
        time : int
            the time it took to execute this method

        """

        start = get_time()
        if self._is_preloaded:
            self._file = None
            self._is_preloaded = False

        return int((get_time() - start) * 1000)

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

        if self._is_paused:
            self.pause()

        if self.is_playing:
            return self._channel

        self._channel = self._file.play(loops, maxtime, fade_ms)
        if self._logging:
            if isinstance(self._filename, str):
                import sys
                filename = self._filename.encode(sys.getfilesystemencoding())
            else:
                filename = self._filename

            _internals.active_exp._event_file_log(
                "Stimulus,played,{0}".format(filename), 1,
                                 log_event_tag=log_event_tag)
        return self._channel

    def pause(self):
        if self._is_preloaded:
            if not self._is_paused:
                self._channel.pause()
                self._is_paused = True
            elif self._is_paused:
                self._channel.unpause()
                self._is_paused = False

    def stop(self):
        """Stop the audio stimulus"""

        if self._is_preloaded:
            self._file.stop()
            self._is_paused = False

    def present(self, log_event_tag=None):
        """Presents the sound.

        The function is identical to Audio.play(loops=0, maxtime=0, fade_ms=0)
        and returns also immediately after the sound started to play.

        Notes
        -----
        See Audio.play for more information.

        """

        self.play(log_event_tag=log_event_tag)

    def wait_end(self, callback_function=None, process_control_events=True):
        """Wait until audio has ended playing.

        Blocks until the audios is not playing anymore and only returns then.

        Parameters
        ----------
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = True)

        Notes
        ------
        This will also by default process control events (quit and pause).
        Thus, keyboard events will be cleared from the cue and cannot be
        received by a Keyboard().check() anymore!

        """

        while self.is_playing:
            if _internals.skip_wait_methods:
                break

            if isinstance(callback_function, FunctionType):
                rtn_callback = callback_function()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    self.stop()
                    return rtn_callback
            if _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    self.stop()
                    return rtn_callback

            if process_control_events:
                _internals.active_exp.mouse.process_quit_event(
                    event_detected_function=self.pause,
                    quit_confirmed_function=self.stop,
                    quit_denied_function=self.play)
                _internals.active_exp.keyboard.process_control_keys(
                    event_detected_function=self.pause,
                    quit_confirmed_function=self.stop,
                    quit_denied_function=self.play)
            else:
                pygame.event.pump()


