"""
Video playback.

This module contains a class implementing video playback.

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import os

import pygame
try:
    import android.mixer as mixer
except:
    import pygame.mixer as mixer

from . import defaults
from . import _visual
from expyriment.io import Keyboard
from expyriment.misc import unicode2str
import expyriment


class Video(_visual.Stimulus):
    """A class implementing a general video stimulus.

    This class uses a background thread for playing the video!
    
    Only MPEG-1 movies with MP3 audio are supported. You can use ffmpeg
    (www.ffmpeg.org) to convert from other formats:
        
        ffmpeg -i <inputfile> -vcodec mpeg1video -acodec libmp3lame -intra -qscale 2  <outputfile.mpg>
        
    The -qscale option is the quality setting. It can take values from 1 to 31.
    1 is the best quality, but big file size. 31 is the worst quality, but
    small file size. Play around with this setting to get a good balance
    between quality and file size.
    
    When the audio from the video should be played as well, the audiosystem
    has to be stopped (by calling expyriment.control.stop_audiosystem() )
    BEFORE the video stimulus is preloaded! After the stimulus has been played
    the audiosystem can be started again (by calling
    expyriment.control.start_audiosystem() ).

    When showing videos in large dimensions, and your computer is not fast
    enough, frames might be dropped! When using Video.wait_frame() or
    Video.wait_end(), dropped video frames will be reported and logged.

    """

    def __init__(self, filename, position=None):
        """Create a video stimulus.
    
        Parameters
        ----------
        filename : str
            filename (incl. path) of the video
        position : (int, int), optional
            position of the stimulus
            
        Notes
        -----
        Only MPEG-1 movies with MP3 audio are supported. You can use ffmpeg
        (www.ffmpeg.org) to convert from other formats:
        
            ffmpeg -i <inputfile> -vcodec mpeg1video -acodec libmp3lame -intra -qscale 2  <outputfile.mpg>
        
        The -qscale option is the quality setting. It can take values from 1 to 31.
        1 is the best quality, but big file size. 31 is the worst quality, but
        small file size. Play around with this setting to get a good balance
        between quality and file size.

        """

        _visual.Stimulus.__init__(self, filename)
        self._filename = filename
        self._is_preloaded = False
        self._frame = 0
        if position:
            self._position = position
        else:
            self._position = defaults.video_position
        if not(os.path.isfile(self._filename)):
            raise IOError("The video file {0} does not exists".format(
                unicode2str(self._filename)))

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
        """Property to check if movie is playing."""

        if self._is_preloaded:
            return self._file.get_busy()

    @property
    def time(self):
        """Property to get the current playback time."""

        if self._is_preloaded:
            return self._file.get_time()

    @property
    def size(self):
        """Property to get the resolution of the movie."""

        if self._is_preloaded:
            return self._file.get_size()

    @property
    def frame(self):
        """Property to get the current frame."""
        if self._is_preloaded:
            return self._file.get_frame()

    @property
    def length(self):
        """Property to get the length of the movie."""

        if self._is_preloaded:
            return self._file.get_length()

    @property
    def has_video(self):
        """Property to check if movie has video."""

        if self._is_preloaded:
            return self._file.has_video()

    @property
    def has_audio(self):
        """Property to check if movie has audio."""

        if self._is_preloaded:
            return self._file.has_audio()

    def preload(self):
        """Preload stimulus to memory.
        
        Notes
        -----
        When the audio from the video should be played as well, the audiosystem
        has to be stopped (by calling expyriment.control.stop_audiosystem() )
        BEFORE the video stimulus is preloaded! After the stimulus has been played
        the audiosystem can be started again (by calling
        expyriment.control.start_audiosystem() ).
        
        """

        if not self._is_preloaded:
            self._file = pygame.movie.Movie(unicode2str(self._filename,
                                                        fse=True))
            screen_size = expyriment._active_exp.screen.surface.get_size()
            self._pos = [screen_size[0] // 2 - self._file.get_size()[0] // 2 +
                         self._position[0],
                         screen_size[1] // 2 - self._file.get_size()[1] // 2 -
                         self._position[1]]
            size = self._file.get_size()
            self._surface = pygame.surface.Surface(size)
            self._file.set_display(self._surface)
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

    def play(self):
        """Play the video stimulus from the current position.
        
        Notes
        -----
        When the audio from the video should be played as well, the audiosystem
        has to be stopped (by calling expyriment.control.stop_audiosystem() )
        BEFORE the video stimulus is preloaded! After the stimulus has been played
        the audiosystem can be started again (by calling
        expyriment.control.start_audiosystem() ).

        When showing videos in large dimensions, and your computer is not fast
        enough, frames might be dropped! When using Video.wait_frame() or
        Video.wait_end(), dropped video frames will be reported and logged.
        
        """

        if mixer.get_init() is not None:
            message = "Mixer is still initialized, cannot play audio! Call \
expyriment.control.stop_audiosystem() before preloading the video."
            print("Warning: ", message)
            if self._logging:
                expyriment._active_exp._event_file_log(
                    "Video,warning," + message)

        if not self._is_preloaded:
            self.preload()
        if self._logging:
            expyriment._active_exp._event_file_log(
                "Video,playing,{0}".format(unicode2str(self._filename)))
        self._file.play()

    def stop(self):
        """Stop the video stimulus."""

        if self._is_preloaded:
            self._file.stop()
            self.rewind()

    def pause(self):
        """Pause the video stimulus."""

        if self._is_preloaded:
            self._file.pause()

    def forward(self, seconds):
        """Advance playback position.

        This will not forward immediately, but play a short period of the
        beginning of the file! This is a Pygame issue which we cannot fix right
        now.

        Parameters
        ----------
        seconds : int
            amount to advance (in seconds)

        """

        if self._is_preloaded:
            self._file.skip(float(seconds))

    def rewind(self):
        """Rewind to start of video stimulus."""

        if self._is_preloaded:
            self._file.rewind()
            self._frame = 0

    def present(self):
        """Play the video and present current frame.

        This method starts video playback and presents a single frame (the
        current one). When using OpenGL, the method blocks until this frame is
        actually being written to the screen.

        Notes
        -----
        When the audio from the video should be played as well, the audiosystem
        has to be stopped (by calling expyriment.control.stop_audiosystem() )
        BEFORE the video stimulus is preloaded! After the stimulus has been played
        the audiosystem can be started again (by calling
        expyriment.control.start_audiosystem() ).

        When showing videos in large dimensions, and your computer is not fast
        enough, frames might be dropped! When using Video.wait_frame() or
        Video.wait_end(), dropped video frames will be reported and logged.
        
        """

        self.play()
        while not self._file.get_frame() > self._frame:
            pass
        self.update()

    def update(self):
        """Update the screen on each new frame."""

        if self._is_preloaded:
            frame = self._file.get_frame()
            if frame > self._frame:
                self._frame = frame
                if expyriment._active_exp._screen.open_gl:
                    ogl_screen = _visual._LaminaPanelSurface(
                        self._surface, position=self._position)
                    ogl_screen.display()
                else:
                    expyriment._active_exp._screen.surface.blit(self._surface,
                                                                self._pos)
                expyriment._active_exp._screen.update()

    def _wait(self, frame=None):
        """Wait until frame was shown or end of movie and update screen.

        Parameters
        ----------
        frame : int, optional
            number of the frame to stop after

        See Also
        --------
        design.experiment.register_wait_callback_function

        """

        while self.is_playing:
            rtn_callback = expyriment._active_exp._execute_wait_callback()
            if isinstance(rtn_callback, expyriment.control.CallbackQuitEvent):
                return rtn_callback

            old_frame = self._frame
            self.update()
            new_frame = self._frame
            if frame is not None and new_frame > frame:
                self.stop()
                break
            diff = new_frame - old_frame
            if diff > 1:
                warn_message = repr(diff - 1) + " video frames dropped!"
                print(warn_message)
                expyriment._active_exp._event_file_warn(
                    "Video,warning," + warn_message)
            for event in pygame.event.get(pygame.KEYDOWN):
                if event.type == pygame.KEYDOWN and (
                   event.key == Keyboard.get_quit_key() or
                   event.key == Keyboard.get_pause_key()):
                    self.stop()
                    Keyboard.process_control_keys(event)
                    self.play()

    def wait_frame(self, frame):
        """Wait until certain frame was shown and constantly update screen.

        Notes
        -----
        This function will also check for control keys (quit and pause).
        Thus, keyboard events will be cleared from the cue and cannot be
        received by a Keyboard().check() anymore!
        If keybaord events should not be cleared, a loop has to be created
        manually like::

            movie.present()
                while movie.is_playing:
                movie.update()
                key = exp.keyboard.check()
                if key == ...

        Parameters
        ----------
        frame : int
            number of the frame to stop after

        """

        self._wait(frame)

    def wait_end(self, last_frame=None):
        """Wait until video has ended and constantly update screen.

        Notes
        -----
        This will also check for control keys (quit and pause).
        Thus, keyboard events will be cleared from the cue and cannot be
        received by a Keyboard().check() anymore!
        If keybaord events should not be cleared, a loop has to be created
        manually like::

            movie.present()
            while movie.is_playing:
                movie.update()
                key = exp.keyboard.check()
                if key == ...

        """

        self._wait()
