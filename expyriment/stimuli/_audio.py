"""
Audio playback.

This module contains a class implementing audio playback.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import os
import time
from types import FunctionType

import pygame

from .. import _internals
from .._internals import CallbackQuitEvent
from ..misc import MediaTime
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
        self._start_position = 0
        self._start_time = 0
        self._paused_time = 0
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

    @property
    def length(self):
        """Property to get the length of the audio."""

        if self._is_preloaded:
            return MediaTime(self._length)

    @property
    def time(self):
        """Property to get the current playback time (in seconds)"""

        if self._is_preloaded:
            if self._is_paused:
                return MediaTime(self._paused_time)
            elif self.is_playing:
                return MediaTime(get_time() - self._start_time)
            else:
                return 0

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
            self._length = self._file.get_length()
            self._sound_array = pygame.sndarray.array(self._file)
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
            self._sound_array = None
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

        Notes
        -----
        If ``seek()``, ``forward()`` or ``rewind()`` have been used to set a
        new playback position **before** calling this method, the ``loop``
        start will be the newly set position.

        Using ``seek()``, ``forward()`` or ``rewind()`` to set a new playback
        position **after** calling this method (i.e. during playback), will
        reset ``loops``, ``maxtime`` and ``fade_ms`` to 0.

        """

        if not self._is_preloaded:
            self.preload()

        if self._is_paused:
            self.pause()

        if self.is_playing:
            return self._channel

        self._channel = self._file.play(loops, maxtime, fade_ms)
        self._start_time = get_time() - self._start_position

        _internals.active_exp.keyboard.quit_control.register_functions(
                event_detected_function=self.pause,
                quit_confirmed_function=self.stop,
                quit_denied_function=self.pause)

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
            if self.is_playing:
                self._channel.pause()
                self._paused_time = get_time() - self._start_time
                self._is_paused = True
            elif self._is_paused:
                self._channel.unpause()
                self._start_time = get_time() - self._paused_time
                self._paused_time = 0
                self._is_paused = False

    def stop(self):
        """Stop the audio stimulus"""

        if self._is_preloaded:
            self._file.stop()
            self.seek(0)
            self._start_position = 0
            self._start_time = 0
            self._paused_time = 0
            self._is_paused = False

            _internals.active_exp.keyboard.quit_control.unregister_functions(
                event_detected_function=self.pause,
                quit_confirmed_function=self.stop,
                quit_denied_function=self.pause)

    def seek(self, time):
        """Seek playback position to specified time.

        Parameters
        ----------
        time : int, float, list or str
            the time to seek to; can be any of the following formats:
                - float: seconds
                - tuple: (minutes, seconds) or (hours, minutes, seconds)
                - list: [minutes, seconds] or [hours, minutes, seconds]
                - str: 'hhrmm:ss', 'hh:mm:ss.sss', or 'mm:ss.sss'

        Examples
        --------
        >>> seek(15.4)          # seconds
        >>> seek((1, 21.5))     # (min, sec)
        >>> seek((1, 1, 2))     # (hr, min, sec)
        >>> seek('01:01:33.5')  # (hr:min:sec)
        >>> seek('01:01:33.045')
        >>> seek('01:01:33,5')  # comma works too

        """

        if self._is_preloaded:
            time = MediaTime.convert_to_seconds(time)
            if time < 0:
                time = 0
            elif time > self._length:
                time = self._length

        if self.is_playing:
            was_playing = True
        else:
            was_playing = False
        self._file.stop()
        self._start_time = 0
        self._paused_time = 0
        self._is_paused = False

        sample_rate = len(self._sound_array) / self._length
        samples_to_skip = int(time * sample_rate)
        sliced_array = self._sound_array[samples_to_skip:]
        self._file = pygame.sndarray.make_sound(sliced_array)

        if was_playing:
            self._channel.play(self._file)
            self._start_time = get_time() - time
        else:
            self._start_position = time

    def forward(self, duration):
        """Forward playback position by specified duration.

        Parameters
        ----------
        duration : int, float, tuple, list or str
            the duration to forward by; can be any of the following formats:
                - float: seconds
                - tuple: (minutes, seconds) or (hours, minutes, seconds)
                - list: [minutes, seconds] or [hours, minutes, seconds]
                - str: 'hhrmm:ss', 'hh:mm:ss.sss', or 'mm:ss.sss'

        Examples
        --------
        >>> forward(15.4)          # seconds
        >>> forward((1, 21.5))     # (min, sec)
        >>> forward((1, 1, 2))     # (hr, min, sec)
        >>> forward('01:01:33.5')  # (hr:min:sec)
        >>> forward('01:01:33.045')
        >>> forward('01:01:33,5')  # comma works too

        """

        if self._is_preloaded:
            if not(self.is_playing or self._is_paused):
                pos = self._start_position + \
                    MediaTime.convert_to_seconds(duration)
            else:
                pos = self.time + MediaTime.convert_to_seconds(duration)
            self.seek(pos)

    def rewind(self, duration=None):
        """Rewind playback position by specified duration or to beginning."

        Parameters
        ----------
        duration : int, float, tuple, list or str, optional
            the duration to rewind by; can be any of the following formats:
                - float: seconds
                - tuple: (minutes, seconds) or (hours, minutes, seconds)
                - list: [minutes, seconds] or [hours, minutes, seconds]
                - str: 'hhrmm:ss', 'hh:mm:ss.sss', or 'mm:ss.sss'

        Examples
        --------
        >>> rewind(15.4)          # seconds
        >>> rewind((1, 21.5))     # (min, sec)
        >>> rewind((1, 1, 2))     # (hr, min, sec)
        >>> rewind('01:01:33.5')  # (hr:min:sec)
        >>> rewind('01:01:33.045')
        >>> rewind('01:01:33,5')  # comma works too

        """

        if self._is_preloaded:
            if duration is None:
                pos = 0
            elif not(self.is_playing or self._is_paused):
                pos = self._start_position - \
                    MediaTime.convert_to_seconds(duration)
            else:
                pos = self.time - MediaTime.convert_to_seconds(duration)
            self.seek(pos)

    def present(self, log_event_tag=None):
        """Presents the sound.

        The function is identical to Audio.play(loops=0, maxtime=0, fade_ms=0)
        and returns also immediately after the sound started to play.

        Parameters
        ----------
        log_event_tag : numeral or string, optional
            if log_event_tag is defined and if logging is switched on for this
            stimulus (default), a summary of the inter-event-intervalls are
            appended at the end of the event file

        Notes
        -----
        See Audio.play for more information.

        """

        self.play(log_event_tag=log_event_tag)

    def wait_time(self, time, callback_function=None,
                  process_control_events=True):
        """Wait until specified time.

        Blocks until specified time is reached and only returns then.

        Parameters
        ----------
        time : int, float, tuple, list or str
            time to wait until; can be any of the following formats:
                 - float: seconds
                - tuple: (minutes, seconds) or (hours, minutes, seconds)
                - list: [minutes, seconds] or [hours, minutes, seconds]
                - str: 'hhrmm:ss', 'hh:mm:ss.sss', or 'mm:ss.sss'
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
        If keyboard events should not be cleared, a loop has to be created
        manually, for instance like::

            while audio.is_playing and audio.time < time:
                key = exp.keyboard.check()
                if key == ...

        """

        while self.is_playing and self.time < time:
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
                _internals.active_exp.mouse.process_quit_event()
                _internals.active_exp.keyboard.process_control_keys()
            else:
                pygame.event.pump()

            time.sleep(0.0001)


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
        If keyboard events should not be cleared, a loop has to be created
        manually, for instance like::

            while audio.is_playing:
                key = exp.keyboard.check()
                if key == ...

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
                _internals.active_exp.mouse.process_quit_event()
                _internals.active_exp.keyboard.process_control_keys()
            else:
                pygame.event.pump()

            time.sleep(0.0001)

