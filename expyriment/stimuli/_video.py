"""
Video playback.

This module contains a class implementing video playback.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import os
import time
from types import FunctionType

import pygame
try:
    import android.mixer as mixer
except Exception:
    import pygame.mixer as mixer

from . import defaults
from . import _visual
from ..control import defaults as control_defaults
from ..misc import unicode2byte, Clock, has_internet_connection, which
from .._internals import CallbackQuitEvent
from .. import _internals


class Video(_visual.Stimulus):
    """A class implementing a general video stimulus.

    This class uses a background thread for playing the video!

    Notes
    -----
    With the "pygame" audio backend, the Expyriment audiosystem is used to play
    the audio of the video. If the audiosystem is stopped BEFORE the video
    stimulus is played, (by calling ``expyriment.control.stop_audiosystem()``),
    or if the "sounddevice" backend is used, a temporary audiosystem will be
    started with parameters (sample rate, bit depth, channels) matching those
    of the video. The temporary audiosystem will be stopped when the video is
    stopped.

    When showing videos in large dimensions, and your computer is not fast
    enough, frames might be dropped! When using ``Video.wait_frame()`` or
    ``Video.wait_end()``, dropped video frames will be reported and logged.

    """

    @staticmethod
    def get_ffmpeg_binary():
        try:
            import imageio
            try:
                ffmpeg_binary = imageio.plugins.ffmpeg.get_exe()
                if ffmpeg_binary == "ffmpeg":
                    ffmpeg_binary = which(ffmpeg_binary)
                return ffmpeg_binary
            except imageio.core.NeedDownloadError:
                try:
                    assert has_internet_connection()
                    imageio.plugins.ffmpeg.download()
                    return imageio.plugins.ffmpeg.get_exe()
                except Exception:
                    os.environ['IMAGEIO_NO_INTERNET'] = 'yes'
        except ImportError:
            pass

    def __init__(self, filename, audio_backend=None, position=None):
        """Create a video stimulus.

        Parameters
        ----------
        filename : str
            filename (incl. path) of the video file
        audio_backend : str, optional
            audio backend to use (one of "pygame" or "sounddevice")
        position : (int, int), optional
            position of the stimulus

        """

        from ..io import Keyboard

        _visual.Stimulus.__init__(self, filename)
        self.Keyboard = Keyboard()
        self._filename = filename
        self._is_preloaded = False
        self._is_paused = False
        self._frame = 0
        self._new_frame_available = False
        self._surface_locked = False
        self._audio_started = False

        if audio_backend:
            self._audio_backend = audio_backend
        else:
            self._audio_backend = defaults.video_audio_backend
        if position:
            self._position = position
        else:
            self._position = defaults.video_position

        if not(os.path.isfile(self._filename)):
            raise IOError(u"The video file {0} does not exists".format(
                self._filename))

        Video.get_ffmpeg_binary()  # in case it still needs to be downloaded
        try:
            import mediadecoder as _mediadecoder
        except ImportError:
            raise ImportError(
                "Video playback needs the package 'mediadecoder'." +
                "\nPlease install mediadecoder(>=0.1.6,<1).")

        if self._audio_backend == "sounddevice":
            try:
                import sounddevice as _sounddevice
            except ImportError:
                raise ImportError(
                    "Audio backend needs the package 'sounddevice'." +
                    "\nPlease install sounddevice(>=0.3.,<1).")

            # Set output device from control.defaults
            default_device = control_defaults.audiosystem_device
            if default_device is not None:
                device_id = None
                # get devices that sounddevice knows
                devices = _sounddevice.query_devices()
                # only consider devices of default audio api
                devices = [x for x in devices \
                           if x["hostapi"] == _sounddevice.default.hostapi]
                # only consider output devices
                devices = [x for x in devices \
                           if x["max_output_channels"] > 0]
                # find device that best corresponds to the one Pygame uses
                for device in devices:
                    tmp = sorted([device["name"], default_device], key=len)
                    # allow for a mismatch of up to 1 character
                    # (":" vs. "," on Linux)
                    if len([x for c,x in enumerate(tmp[0]) \
                            if tmp[1][c] != x]) <= 1:
                        device_id = device["index"]
                if device_id is not None:
                    _sounddevice.default.device = None, device_id
        elif self._audio_backend != "pygame":
            raise ValueError("Unknown audio backend '{0}'!".format(
                self._audio_backend))


    def __del__(self):
        """Destructor for the video stimulus."""

        self.stop()
        self._surface = None
        self._file = None

    _getter_exception_message = "Cannot set {0} if preloaded!"

    @property
    def is_preloaded(self):
        """Getter for is_preloaded."""

        return self._is_preloaded

    @property
    def position(self):
        """Getter for position."""

        return self._position

    @property
    def audio_backend(self):
        """Getter for audio_backend."""

        return self._audio_backend

    @property
    def filename(self):
        """Getter for filename."""

        return self._filename

    @filename.setter
    def filename(self, value):
        """Setter for filename."""

        if self._is_preloaded:
            raise AttributeError(Video._getter_exception_message.format(
                "filename"))
        else:
            self._filename = value
            if not(os.path.isfile(self._filename)):
                raise IOError(u"The video file {0} does not exists".format(
                    self._filename))

    @property
    def is_playing(self):
        """Property to check if video is playing."""

        if self._is_preloaded:
            return self._file.status == 3

    @property
    def is_paused(self):
        """Property to check if video is paused."""

        if self._is_preloaded:
            return self._is_paused

    @property
    def time(self):
        """Property to get the current playback time."""

        if self._is_preloaded:
            return self._file.current_playtime

    @property
    def size(self):
        """Property to get the resolution of the video."""

        if self._is_preloaded:
            return self._file.clip.size

    @property
    def frame(self):
        """Property to get the current available video frame."""

        if self._is_preloaded:
            return self._file.current_frame_no

    @property
    def new_frame_available(self):
        """Property to check if new video frame is available to render."""

        if self._is_preloaded:
            time.sleep(0.0001)  # Needed for performance for some reason
            return self._new_frame_available

    @property
    def length(self):
        """Property to get the length of the video."""

        if self._is_preloaded:
            return self._file.duration

    @property
    def has_video(self):
        """Property to check if video fifle has video information."""

        if self._is_preloaded:
            return self._file.clip.video is not None

    @property
    def has_audio(self):
        """Property to check if video file has audio information."""

        if self._is_preloaded:
            return self._file.clip.audio is not None

    def preload(self):
        """Preload stimulus to memory.

        """

        if not self._is_preloaded:
            if not _internals.active_exp.is_initialized:
                message = "Can't preload video. Expyriment needs to be " + \
                          "initialized before preloading a video."
                raise RuntimeError(message)
            if self.get_ffmpeg_binary() is None:
                raise RuntimeError("'ffmpeg' not found!")
            from mediadecoder.states import PLAYING
            from mediadecoder.decoder import Decoder
            self._file = Decoder(mediafile=self._filename,
                                 videorenderfunc=self._update_surface)
            if _internals.active_exp._screen.opengl:
                import moviepy
                if int(moviepy.__version__.split(".")[0]) > 1:
                    from moviepy.video.fx import MirrorY
                    self._file.clip = self._file.clip.with_effects([MirrorY()])
                else:
                    import moviepy.video.fx.all as vfx
                    self._file.clip = vfx.mirror_y(self._file.clip)

            size = self._file.clip.size

            screen_size = _internals.active_exp.screen.surface.get_size()
            self._pos = [screen_size[0] // 2 - size[0] // 2 +
                         self._position[0],
                         screen_size[1] // 2 - size[1] // 2 -
                         self._position[1]]

            self._is_paused = False
            self._is_preloaded = True

    def unload(self, **kwargs):
        """Unload stimulus from memory.

        This removes the reference to the object in memory.
        It is up to the garbage collector to actually remove it from memory.

        """

        if self._is_preloaded:
            self.stop()
            self._file = None
            self._surface = None
            self._is_preloaded = False

    def play(self, loop=False, log_event_tag=None, audio=True):
        """Play the video stimulus from the current position.

        Parameters
        ----------
        loop : bool, optional
            loop video playback (will be ignored when using play to unpause!)
        log_event_tag : numeral or string, optional
            if log_event_tag is defined and if logging is switched on for this
            stimulus (default), a summary of the inter-event-intervalls are
            appended at the end of the event file
        audio : bool, optional
            whether audio of video (if present) should be played (default=True)

        Notes
        -----
        With the "pygame" audio backend, the Expyriment audiosystem is used to
        play the audio of the video. If the audiosystem is stopped BEFORE the
        video stimulus is played, (by calling
        ``expyriment.control.stop_audiosystem()``), or if the "sounddevice"
        backend is used, a temporary audiosystem will be started with
        parameters (sample rate, bit depth, channels) matching those of the
        video. The temporary audiosystem will be stopped when the video is
        stopped.

        When showing videos in large dimensions, and your computer is not fast
        enough, frames might be dropped! When using Video.wait_frame() or
        Video.wait_end(), dropped video frames will be reported and logged.

        """

        if self._is_paused:
            if audio and not self._audio_started:
                self._audio.stream.start()
                self._audio_started = True
            elif not audio and self._audio_started:
                self._audio.stream.stop()
                self._audio_started = False
            self.pause()
        else:
            if not self._is_preloaded:
                self.preload()
            if self._logging:
                _internals.active_exp._event_file_log(
                    "Video,playing,{0}".format(self._filename),
                    log_level=1, log_event_tag=log_event_tag)
            if self._file.audioformat and audio:
                if self._audio_backend == "pygame":
                    from mediadecoder.soundrenderers import SoundrendererPygame
                    self._audio = SoundrendererPygame(self._file.audioformat)

                elif self._audio_backend == "sounddevice":
                    from mediadecoder.soundrenderers import \
                        SoundrendererSounddevice
                    self._audio = SoundrendererSounddevice(
                        self._file.audioformat)
                self._file.set_audiorenderer(self._audio)
                self._audio.start()
                self._audio_started = True
            self._file.loop = loop
            self._file.play()

    def stop(self):
        """Stop the video stimulus."""

        if self._is_preloaded:
            self._file.stop()
            self.rewind()
            if self._file.audioformat:
                self._audio.close_stream()

    def pause(self):
        """Pause the video stimulus."""

        if self._is_preloaded:
            self._file.pause()
            if self._is_paused:
                self._is_paused = False
            else:
                self._is_paused = True

    def forward(self, seconds):
        """Advance playback position.

        Parameters
        ----------
        seconds : int
            amount to advance (in seconds)

        """

        if self._is_preloaded:
            pos = self._file.current_playtime + seconds
            self._file.seek(pos)
            new_frame = int(pos * self._file.fps)
            self._frame = new_frame

    def rewind(self):
        """Rewind to start of video stimulus."""

        if self._is_preloaded:
            self._file.rewind()
            self._frame = 0

    def _update_surface(self, frame):
        """Update surface with newly available video frame."""

        if not self._surface_locked:
            self._surface = frame
            self._new_frame_available = True

    def present(self):
        """Present current frame.

        This method waits for the next frame and presents it on the screen.
        When using OpenGL, the method blocks until this frame is actually being
        written to the screen.

        Notes
        -----
        When showing videos in large dimensions, and your computer is not fast
        enough, frames might be dropped! When using ``Video.wait_frame()`` or
        ``Video.wait_end()``, dropped video frames will be reported and logged.

        """

        start = Clock.monotonic_time()
        while not self.new_frame_available:
            if not self.is_playing:
                return
        diff = self.frame - self._frame
        if diff > 1:
            warn_message = repr(diff - 1) + " video frame(s) dropped!"
            print(warn_message)
            _internals.active_exp._event_file_warn(
                "Video,warning," + warn_message)
        self._frame = self.frame
        self.update()
        return (Clock.monotonic_time() - start) * 1000

    def update(self):
        """Update the screen."""

        if not self.is_playing:
            return
        start = Clock.monotonic_time()
        self._surface_locked = True
        if not _internals.active_exp._screen.opengl:
            _internals.active_exp._screen.surface.blit(
                pygame.surfarray.make_surface(self._surface.swapaxes(0,1)),
                self._pos)
            self._surface_locked = False
            self._new_frame_available = False
        else:
            ogl_screen = _visual._LaminaPanelSurface(
                self._surface, quadDims=(1,1,1,1), position=self._position)
            self._surface_locked = False
            self._new_frame_available = False
            ogl_screen.display()
        _internals.active_exp._screen.update()

    def _wait(self, frame=None, callback_function=None,
              process_control_events=True):
        """Wait until frame was shown or end of video and update screen.

        Parameters
        ----------
        frame : int, optional
            number of the frame to stop after
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

        See Also
        --------
        expyriment.design.Experiment.register_wait_callback_function

        """

        while self.is_playing:

            if _internals.skip_wait_methods:
                return

            self.present()
            if frame is not None and self.frame >= frame:
                break

            if isinstance(callback_function, FunctionType):
                rtn_callback = callback_function()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    return rtn_callback
            if _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    return rtn_callback
                if process_control_events:
                    if _internals.active_exp.mouse.process_quit_event():
                        break

            for event in pygame.event.get(pygame.KEYDOWN):
                if _internals.active_exp.is_initialized and \
                   process_control_events and \
                   event.type == pygame.KEYDOWN and (
                       event.key == self.Keyboard.get_quit_key()):
                    self.pause()
                    self.Keyboard.process_control_keys(event, self.stop)
                    self.play()

    def wait_frame(self, frame, callback_function=None,
                   process_control_events=True):
        """Wait until certain frame was shown and constantly update screen.

        Parameters
        ----------
        frame : int
            number of the frame to stop after
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
        manually like::

            video.present()
            while video.is_playing and video.frame < frame:
                while not video.new_frame_available:
                    key = exp.keyboard.check()
                    if key == ...
                video.update()
            video.stop()

        """

        if self.is_playing:
            self._wait(frame, callback_function, process_control_events)

    def wait_end(self, callback_function=None, process_control_events=True):
        """Wait until video has ended and constantly update screen.

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
        manually like::

            video.present()
            while video.is_playing and video.frame < frame:
                while not video.new_frame_available:
                    key = exp.keyboard.check()
                    if key == ...
                video.update()
            video.stop()

        """

        self._wait(callback_function, process_control_events)
