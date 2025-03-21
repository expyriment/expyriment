"""
Video playback.

This module contains a class implementing video playback.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import os
import time
import atexit
from types import FunctionType

import pygame

from . import defaults
from . import _visual
from ..control import defaults as control_defaults
from ..misc import unicode2byte, Clock, has_internet_connection, which
from ..misc._timer import get_time
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
    started with parameters (sample rate, bit depth, channels) matching the
    audiosystem defaults. The temporary audiosystem will be stopped when the
    video is stopped.

    When showing videos in large dimensions, and your computer is not fast
    enough, frames might be dropped! When using ``Video.wait_frame()`` or
    ``Video.wait_end()``, dropped video frames will be reported and logged.

    """

    @staticmethod
    def get_ffmpeg_binary():
        try:
            import imageio_ffmpeg
            try:
                ffmpeg_binary = imageio_ffmpeg.get_ffmpeg_exe()
                if ffmpeg_binary == "ffmpeg":
                    ffmpeg_binary = which(ffmpeg_binary)
                return ffmpeg_binary
            except RuntimeError:
                pass
        except ImportError:
            pass

    def __init__(self, filename, resizing=None, audio_backend=None,
                 position=None):
        """Create a video stimulus.

        Parameters
        ----------
        filename : str
            filename (incl. path) of the video file
        resizing : int, float, bool, None, list or tuple , optional
            Determines whether and how the video should be resized upon
            preloading.
            When given a single value, the value can be:
                int     - Resizing of video to the given height
                          (e.g., 1080, 720)
                float   - Resizing of video with given scaling factor
                          (e.g., 0.5 * original)
                `True`  - Resizing of video to fit screen
                `False` - No resizing of video
            Resizing using a single value will always maintain the orignal
            aspect ratio.
            When given a list or tuple of (width, height), resizing of each
            dimension can be controlled individually, and the values can be:
                int     - Resizing of dimension to given value
                float   - Resizing of dimension with given scaling factor
                `True`  - Resizing of dimension to fit screen dimension
                `False` - No resizing of dimension
                `None`  - Conditional resizing of dimension
                          (i.e., compute value to keep aspect ratio, given
                          value of the other dimension; if both dimensions are
                          `None`, resize to fit the screen, but only if either
                          dimension of the original exceeds the corresponding
                          screen dimension)
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
        self._start_position = 0

        if audio_backend is not None:
            self._audio_backend = audio_backend
        else:
            self._audio_backend = defaults.video_audio_backend
        if resizing is not None:
            self._resizing = resizing
        else:
            self._resizing = defaults.video_resizing
        if position is not None:
            self._position = position
        else:
            self._position = defaults.video_position

        if not(os.path.isfile(self._filename)):
            raise IOError(u"The video file {0} does not exists".format(
                self._filename))

        try:
            import mediadecoder
        except ImportError:
            raise ImportError(
                "Video playback needs the package 'mediadecoder'." +
                "\nPlease install mediadecoder(>=0.2,<1).")

        if self._audio_backend == "sounddevice":
            try:
                import sounddevice
            except ImportError:
                raise ImportError(
                    "Audio backend needs the package 'sounddevice'." +
                    "\nPlease install sounddevice(>=0.3.,<1).")

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
    def resizing(self):
        """Getter for resizing."""

        return self._resizing

    @resizing.setter
    def resizing(self, value):
        if self._is_preloaded:
            raise AttributeError(Video._getter_exception_message.format(
                "resizing"))
        else:
            self._resizing = value

    @property
    def audio_backend(self):
        """Getter for audio_backend."""

        return self._audio_backend

    @audio_backend.setter
    def audio_backend(self, value):
        if self._is_preloaded:
            raise AttributeError(Video._getter_exception_message.format(
                "audio_backend"))
        else:
            if value not in ("pygame", "sounddevice"):
                raise ValueError("Unknown audio backend '{0}'!".format(value))
            self._audio_backed = value

    @property
    def position(self):
        """Getter for position."""

        return self._position

    @position.setter
    def position(self, value):
        if self._is_preloaded:
            raise AttributeError(Video._getter_exception_message.format(
                "position"))
        else:
            self._position = value

    @property
    def size(self):
        """Getter for size."""

        if self._is_preloaded:
            return self._file.clip.size

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

        Returns
        -------
        time : int
            the time it took to execute this method

        """

        start = get_time()
        if not self._is_preloaded:
            if not _internals.active_exp.is_initialized:
                message = "Can't preload video. Expyriment needs to be " + \
                          "initialized before preloading a video."
                raise RuntimeError(message)

            if self.get_ffmpeg_binary() is None:
                raise RuntimeError("'ffmpeg' not found!")

            if self._audio_backend == "sounddevice":
                # Set output device from control.defaults
                import sounddevice as _sounddevice
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

            from mediadecoder.states import PLAYING
            from mediadecoder.decoder import Decoder

            # Calculate target_resolution
            screen_size = _internals.active_exp.screen.surface.get_size()
            if isinstance(self._resizing, (int, float, bool)):  # single value
                if self._resizing == False:
                    target_res = (None, None)
                elif isinstance(self._resizing, (int, float, bool)):
                    video_size = Decoder(mediafile=self._filename, play_audio=False).clip.size
                    if self._resizing is True:
                        x_diff = video_size[0] - screen_size[0]
                        y_diff = video_size[1] - screen_size[1]
                        if x_diff > y_diff:
                            target_res = (screen_size[0], None)
                        else:
                            target_res = (None, screen_size[1])
                    elif isinstance(self._resizing, int):
                        target_res = (None, self._resizing)
                    elif isinstance(self._resizing, float):
                        target_res = (int(video_size[0] * self._resizing),
                                      int(video_size[1] * self._resizing))

            elif (hasattr(self._resizing, '__getitem__')) and \
                  (hasattr(self._resizing, '__len__')) and \
                   len(self._resizing) >= 2:  # List/tuple (or other indexable)
                if (self._resizing[0] is None and self._resizing[1] is None) \
                or any(isinstance(x, float) for x in self._resizing) \
                        or False in self._resizing:
                        video_size = Decoder(mediafile=self._filename,
                                             play_audio=False).clip.size
                if self._resizing[0] is None and self._resizing[1] is None:
                    x_diff = video_size[0] - screen_size[0]
                    y_diff = video_size[1] - screen_size[1]
                    if x_diff > 0 and y_diff > 0:
                        if x_diff > y_diff:
                            target_res = (screen_size[0], None)
                        else:
                            target_res = (None, screen_size[1])
                    else:
                        target_res = (None, None)
                else:
                    target_res = [None, None]
                    for c, value in enumerate(self._resizing):
                        if value == False:
                            target_res[c] = video_size[c]
                        elif value == True:
                            target_res[c] = screen_size[c]
                        elif type(value) is int:
                            target_res[c] = value
                        elif type(value) is float:
                            target_res[c] = int(value * video_size[c])
                        elif value is None:
                            pass

            # Load media
            self._file = Decoder(
                mediafile=self._filename,
                videorenderfunc=self._update_surface,
                target_resolution=target_res,
                audio_fps=control_defaults.audiosystem_sample_rate,
                audio_nbytes=\
                abs(int(control_defaults.audiosystem_bit_depth / 8)),
                audio_nchannels=control_defaults.audiosystem_channels)
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
            atexit.register(self.unload)

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
            self.stop()
            del self._file
            self._file = None
            self._surface = None
            self._is_preloaded = False

        return int((get_time() - start) * 1000)

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
        parameters (sample rate, bit depth, channels) matching the audiosystem
        defaults. The temporary audiosystem will be stopped when the video is
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
                    self._audio = SoundrendererPygame(
                        self._file.audioformat,
                        pygame_buffersize=\
                        control_defaults.audiosystem_buffer_size)

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
            if self._start_position != 0:
                while True:
                    try:
                        self._file.seek(self._start_position)
                        self._new_frame_available = False
                        break
                    except AttributeError:  # if thread not fully started yet
                        if self._file.status == 2:  # paused by seek method
                            self._file.pause()  # set playing again

    def stop(self):
        """Stop the video stimulus."""

        if self._is_preloaded:
            self._file.stop()
            self._file.seek(0)
            self._frame = 0
            self._start_position = 0
            if self._file.audioformat and hasattr(self, "_audio"):
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
            if not(self.is_playing or self._is_paused):
                pos = self._start_position + seconds
                self._start_position = pos
            else:
                pos = self._file.current_playtime + seconds
                if self._is_paused:
                    self.pause()  # mediadecoder pauses itself before seeking!
                    was_paused = True
                else:
                    was_paused = False
                while True:
                    try:
                        self._file.seek(pos)
                        break
                    except AttributeError: # if thread not fully started yet
                        pass
                if was_paused:
                    self.pause()  # mediadecoder unpauses itself after seeking!
            new_frame = int(pos * self._file.fps)
            self._frame = new_frame
            self._new_frame_available = False

    def rewind(self):
        """Rewind to start of video stimulus."""

        if self._is_preloaded:
            self._file.rewind()
            self._frame = 0
            self._start_position = 0

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
