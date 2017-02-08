"""
Video playback.

This module contains a class implementing video playback.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import os
import time
from types import FunctionType

import pygame
try:
    import android.mixer as mixer
except:
    import pygame.mixer as mixer

from . import defaults
from . import _visual
from ..misc import unicode2byte, Clock, has_internet_connection
from .._internals import CallbackQuitEvent
from .. import _internals


class Video(_visual.Stimulus):
    """A class implementing a general video stimulus.

    This class uses a background thread for playing the video!

    Note
    ----
    When the backend is set to ``"pygame"``, only MPEG-1 videos with MP3 audio
    are supported. You can use ffmpeg (www.ffmpeg.org) to convert from other
    formats:

        ffmpeg -i <inputfile> -vcodec mpeg1video -acodec libmp3lame -intra -qscale 2  <outputfile.mpg>

    The -qscale option is the quality setting. It can take values from 1 to 31.
    1 is the best quality, but big file size. 31 is the worst quality, but
    small file size. Play around with this setting to get a good balance
    between quality and file size.

    When the audio from the video should be played as well, the audiosystem
    has to be stopped (by calling ``expyriment.control.stop_audiosystem()``)
    BEFORE the video stimulus is preloaded! After the stimulus has been played
    the audiosystem can be started again (by calling
    ``expyriment.control.start_audiosystem()``).

    When showing videos in large dimensions, and your computer is not fast
    enough, frames might be dropped! When using ``Video.wait_frame()`` or
    ``Video.wait_end()``, dropped video frames will be reported and logged.

    """

    def __init__(self, filename, backend=None, position=None):
        """Create a video stimulus.

        Parameters
        ----------
        filename : str
            filename (incl. path) of the video
        backend : str, optional
            'mediadecoder' or 'pygame'
        position : (int, int), optional
            position of the stimulus

        Note
        ----
        When the backend is set to ``"pygame"``, only MPEG-1 videos with MP3
        audio are supported. You can use ffmpeg (www.ffmpeg.org) to convert from
        other formats:

            ffmpeg -i <inputfile> -vcodec mpeg1video -acodec libmp3lame -intra -qscale 2  <outputfile.mpg>

        The -qscale option is the quality setting. It can take values from 1 to 31.
        1 is the best quality, but big file size. 31 is the worst quality, but
        small file size. Play around with this setting to get a good balance
        between quality and file size.

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
        if backend:
            self._backend = backend
        else:
            self._backend = defaults.video_backend
        if position:
            self._position = position
        else:
            self._position = defaults.video_position

        if not(os.path.isfile(self._filename)):
            raise IOError("The video file {0} does not exists".format(
                unicode2byte(self._filename)))
            
        if self._backend == "mediadecoder":
            try:
                k = 'IMAGEIO_NO_INTERNET'
                v = ['yes', 'true', '1']
                if not (os.environ.has_key(k) and os.environ[k] in v):
                    if not has_internet_connection():
                        os.environ['IMAGEIO_NO_INTERNET'] = 'yes'
                import mediadecoder as _mediadecoder
            except ImportError:
                message = """Video cannot be initialized with backend
"mediadecoder". The Python package 'mediadecoder' is not installed."""
                raise ImportError(message)

            try:
                import sounddevice as _sounddevice
            except ImportError:
                print("Warning: Package 'sounddevice' not installed!\n" +
                      "Audio will be played back using 'Pygame' backend.")


    def __del__(self):
        """Destructor for the video stimulus."""

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

    @property
    def is_playing(self):
        """Property to check if video is playing."""

        if self._is_preloaded:
            if self._backend == "pygame":
                return self._file.get_busy()
            elif self._backend == "mediadecoder":
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
            if self._backend == "pygame":
                return self._file.get_time()
            elif self._backend == "mediadecoder":
                return self._file.current_playtime

    @property
    def size(self):
        """Property to get the resolution of the video."""

        if self._is_preloaded:
            if self._backend == "pygame":
                return self._file.get_size()
            elif self._backend == "mediadecoder":
                return self._file.clip.size

    @property
    def frame(self):
        """Property to get the current available video frame."""

        if self._is_preloaded:
            if self._backend == "pygame":
                return self._file.get_frame()
            elif self._backend == "mediadecoder":
                return self._file.current_frame_no

    @property
    def new_frame_available(self):
        """Property to check if new video frame is available to render."""

        if self._is_preloaded:
            if self._backend == "pygame":
                return self.frame > self._frame
            elif self._backend == "mediadecoder":
                time.sleep(0.0001)  # Needed for performance for some reason
                return self._new_frame_available

    @property
    def length(self):
        """Property to get the length of the video."""

        if self._is_preloaded:
            if self._backend == "pygame":
                return self._file.get_length()
            elif self._backend == "mediadecoder":
                return self._file.duration

    @property
    def has_video(self):
        """Property to check if video fifle has video information."""

        if self._is_preloaded:
            if self._backend == "pygame":
                return self._file.has_video()
            elif self._backend == "mediadecoder":
                return self._file.clip.video is not None

    @property
    def has_audio(self):
        """Property to check if video file has audio information."""

        if self._is_preloaded:
            if self._backend == "pygame":
                return self._file.has_audio()
            elif self._backend == "mediadecoder":
                return self._file.clip.audio is not None

    def preload(self):
        """Preload stimulus to memory.

        Note
        ----
        When the audio from the video should be played as well, the audiosystem
        has to be stopped (by calling ``expyriment.control.stop_audiosystem()``)
        BEFORE the video stimulus is preloaded! After the stimulus has been
        played the audiosystem can be started again (by calling
        ``expyriment.control.start_audiosystem()``).

        """

        if not self._is_preloaded:
            if self._backend == "pygame":
                self._file = pygame.movie.Movie(unicode2byte(self._filename,
                                                             fse=True))
                size = self._file.get_size()
            elif self._backend == "mediadecoder":
                from mediadecoder.states import PLAYING
                from mediadecoder.decoder import Decoder
                self._file = Decoder(mediafile=unicode2byte(self._filename),
                                     videorenderfunc=self._update_surface)
                if _internals.active_exp._screen.open_gl:
                    import moviepy.video.fx.all as vfx
                    self._file.clip = vfx.mirror_y(self._file.clip)
                if self._file.audioformat:
                    try:
                        from mediadecoder.soundrenderers.sounddevicerenderer import SoundrendererSounddevice
                        self._audio = SoundrendererSounddevice(
                            self._file.audioformat)
                        self._audio_renderer = "sounddevice"
                    except ImportError:
                        from mediadecoder.soundrenderers import SoundrendererPygame
                        self._audio = SoundrendererPygame(
                            self._file.audioformat)
                        self._audio_renderer = "pygame"
                    self._file.set_audiorenderer(self._audio)
                size = self._file.clip.size
            else:
                raise RuntimeError("Unknown backend '{0}'!".format(
                    self._backend))
            screen_size = _internals.active_exp.screen.surface.get_size()

            self._pos = [screen_size[0] // 2 - size[0] // 2 +
                         self._position[0],
                         screen_size[1] // 2 - size[1] // 2 -
                         self._position[1]]
            if self._backend== "pygame":
                self._surface = pygame.surface.Surface(size)
                self._file.set_display(self._surface)
            self._is_paused = False
            self._is_preloaded = True

    def unload(self, **kwargs):
        """Unload stimulus from memory.

        This removes the reference to the object in memory.
        It is up to the garbage collector to actually remove it from memory.

        """

        if self._is_preloaded:
            self._file = None
            self._surface = None
            self._is_preloaded = False

    def play(self, loop=False, log_event_tag=None):
        """Play the video stimulus from the current position.

        Parameters
        ----------
        loop : bool, optional
            loop video playback (will be ignored when using play to unpause!)
        log_event_tag : numeral or string, optional
            if log_event_tag is defined and if logging is switched on for this
            stimulus (default), a summary of the inter-event-intervalls are
            appended at the end of the event file

        Note
        ----
        When the audio from the video should be played as well, the audiosystem
        has to be stopped (by calling expyriment.control.stop_audiosystem() )
        BEFORE the video stimulus is preloaded! After the stimulus has been
        played the audiosystem can be started again (by calling
        expyriment.control.start_audiosystem() ).

        When showing videos in large dimensions, and your computer is not fast
        enough, frames might be dropped! When using Video.wait_frame() or
        Video.wait_end(), dropped video frames will be reported and logged.

        """

        if self._is_paused:
            self.pause()
        else:
            if self._backend == "pygame" and mixer.get_init() is not None:
                message = "Mixer is still initialized, cannot play audio! Call \
    expyriment.control.stop_audiosystem() before preloading the video."
                print("Warning: ", message)
                if self._logging:
                    _internals.active_exp._event_file_log(
                        "Video,warning," + message)

            if not self._is_preloaded:
                self.preload()
            if self._logging:
                _internals.active_exp._event_file_log(
                    "Video,playing,{0}".format(unicode2byte(self._filename)),
                    log_level=1, log_event_tag=log_event_tag)
            if self._backend == "mediadecoder" and self._file.audioformat:
                self._audio.start()
            self._file.loop = loop
            self._file.play()

    def stop(self):
        """Stop the video stimulus."""

        if self._is_preloaded:
            self._file.stop()
            self.rewind()
            if self._backend == "mediadecoder" and self._file.audioformat:
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

        Note
        ----
        When the backend is set to ``"pygame"``, this will not forward
        immediately, but play a short period of the beginning of the file! This
        is a Pygame issue which we cannot fix right now.

        Parameters
        ----------
        seconds : int
            amount to advance (in seconds)

        """

        if self._is_preloaded:
            if self._backend == "pygame":
                self._file.skip(float(seconds))
                new_frame = self._file.get_frame()
            else:
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

        if self._backend == "mediadecoder" and not self._surface_locked:
            self._surface = frame
            self._new_frame_available = True

    def present(self):
        """Present current frame.

        This method waits for the next frame and presents it on the screen.
        When using OpenGL, the method blocks until this frame is actually being
        written to the screen.

        Note
        ----
        When the audio from the video should be played as well, the audiosystem
        has to be stopped (by calling ``expyriment.control.stop_audiosystem()``)
        BEFORE the video stimulus is preloaded! After the stimulus has been
        played the audiosystem can be started again (by calling
        ``expyriment.control.start_audiosystem()``).

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

        start = Clock.monotonic_time()
        self._surface_locked = True
        if not _internals.active_exp._screen.open_gl:
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
        design.experiment.register_wait_callback_function

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
            if _internals.active_exp is not None and \
               _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    return rtn_callback
                if process_control_events:
                    if _internals.active_exp.mouse.process_quit_event():
                        break

            for event in pygame.event.get(pygame.KEYDOWN):
                if _internals.active_exp is not None and \
                   _internals.active_exp.is_initialized and \
                   process_control_events and \
                   event.type == pygame.KEYDOWN and (
                       event.key == self.Keyboard.get_quit_key() or
                       event.key == self.Keyboard.get_pause_key()):
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
        If keybaord events should not be cleared, a loop has to be created
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
        If keybaord events should not be cleared, a loop has to be created
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
