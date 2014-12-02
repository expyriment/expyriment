"""
A screen.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import sys

import pygame
try:
    import OpenGL.GL as ogl
except ImportError:
    ogl = None

import expyriment
from _input_output import Output


class Screen(Output):
    """A class implementing a screen output.

    Each experiment and all stimuli need a screen instance to function.
    They are expecting this screen instance to be referenced in
    expyriment._active_exp.screen.
    Calling expyriment.control.intialize(exp) will automatically create such
    a screen instance and will additionally reference it in exp.screen for
    easy access.

    """

    def __init__(self, colour, open_gl, window_mode, window_size, blocking_mode=1):
        """Create and set up a screen output.

        Notes
        -----
        CAUTION: We discourage from creating a screen instance manually!

        Parameters
        ----------
        colour : (int, int, int)
            colour of the screen
        open_gl : bool
             if OpenGL should be used
        window_mode : bool
             if screen should be a window
        window_size : (int, int)
            size of the window in window_mode,
            full screen mode if size of window_mode[0]<=0

        blocking_mode : int
            type of screen blocking
            0: no sync screen blocking (always in non open_gl modes)
            1: old sync xxxxx #TODO
            2: new sync xxx #TODO

        """

        Output.__init__(self)
        self._colour = colour
        self._open_gl = open_gl
        self._fullscreen = not window_mode
        self._window_size = window_size
        if open_gl: # TODO: Checking also Win & ATI here?
            self._blocking_mode = blocking_mode
        else:
            self._blocking_mode = 0

        if ogl is None:
            warn_message = "PyOpenGL is not installed. \
OpenGL will be deactivated!"
            print("Warning: " + warn_message)
            expyriment._active_exp._event_file_warn("Screen,warning," + warn_message)
            self._open_gl = False

        if self._open_gl and not self._fullscreen:
            warn_message = "OpenGL does not support window mode. \
OpenGL will be deactivated!"
            print("Warning: " + warn_message)
            expyriment._active_exp._event_file_warn("Screen,warning," + warn_message)
            self._open_gl = False
        pygame.display.init()
        if expyriment._active_exp.is_initialized:
            self._monitor_resolution = \
                        expyriment._active_exp.screen.monitor_resolution
        else:
            self._monitor_resolution = (pygame.display.Info().current_w,
                                        pygame.display.Info().current_h)
        if self._fullscreen:
            self._window_size = self._monitor_resolution
        else:
            self._window_size = window_size

        if not self._open_gl:
            if self._fullscreen:
                self._surface = pygame.display.set_mode(self._window_size,
                                                       pygame.FULLSCREEN)
            else:
                self._surface = pygame.display.set_mode(self._window_size)
        else:
            self._surface = pygame.display.set_mode(
                self._window_size,
                pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN)
            ogl_version = ogl.glGetString(ogl.GL_VERSION)
            if float(ogl_version[0:3]) < 2.0:
                ogl_extensions = ogl.glGetString(ogl.GL_EXTENSIONS)
                if "ARB_texture_non_power_of_two" not in ogl_extensions:
                    raise RuntimeError("OpenGL mode is not supported on this \
machine!")
        pygame.mouse.set_visible(False)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_blocked(pygame.MOUSEBUTTONUP)

    @property
    def colour(self):
        """Getter for colour."""
        return self._colour

    @colour.setter
    def colour(self, value):
        """Setter for colour."""
        self._colour = value

    @property
    def surface(self):
        """Getter for surface."""

        return self._surface

    @property
    def open_gl(self):
        """Getter for open_gl."""

        return self._open_gl

    @property
    def blocking_mode(self):
        """Getter for sync_mode."""

        return self._blocking_mode

    @property
    def window_mode(self):
        """Getter for window_mode."""

        return not self._fullscreen

    @property
    def window_size(self):
        """Getter for window_size."""

        return self._window_size

    @property
    def monitor_resolution(self):
        """Getter for monitor_resolution."""

        return self._monitor_resolution

    def update(self):
        """Update the screen.

        This will flip the display double buffer.

        """

        pygame.event.pump()
        pygame.display.flip()
        if self._open_gl and self._blocking_mode>0:
            if self._blocking_mode == 2:
                ogl.glBegin(ogl.GL_POINTS)
                ogl.glColor4f(0, 0, 0, 0)
                vendor = ogl.glGetString(ogl.GL_VENDOR)
                if sys.platform == 'win32' and vendor.lower().startswith('ati'): # TODO can't see be check when setting sync_mode in __init__
                    pass
                else:
                    # this corrupts text rendering on win with some ATI cards :-(
                    ogl.glVertex2i(0, 0)
                ogl.glEnd()
            ogl.glFinish()
        if self._logging:
            expyriment._active_exp._event_file_log("Screen,updated", 2)

    def update_stimuli(self, stimuli):
        """Update only some stimuli on the screen.

        Notes
        -----
        This does only work for non OpenGL screens.

        Parameters
        ----------
        stimuli : list
            stimulus or a list of stimuli to update

        """
        if type(stimuli) is not list:
            stimuli = [stimuli]

        if not self._open_gl:
            rectangles = []
            half_screen_size = (self.size[0] / 2, self.size[1] / 2)
            for stim in stimuli:
                pos = stim.absolute_position
                stim_size = stim.surface_size
                rect_pos = (pos[0] + half_screen_size[0] - stim_size[0] / 2,
                            - pos[1] + half_screen_size[1] - stim_size[1] / 2)
                rectangles.append(pygame.Rect(rect_pos, stim_size))
            pygame.display.update(rectangles)
            if self._logging:
                expyriment._active_exp._event_file_log("Screen,stimuli updated,{0}"\
                                .format([stim.id for stim in stimuli]), 2)
            pygame.event.pump()

    @property
    def center_x(self):
        """Getter for X-coordinate of the screen center.

        Notes
        -----
        Each initialized experiment has its one screen (exp.screen). Please use always the
        screen of your current  experiment.

        """

        return self._window_size[0] / 2

    @property
    def center_y(self):
        """Getter for the Y-coordinate of the screen center.

        Notes
        -----
        Each initialized experiment has its one screen (exp.screen). Please use always the
        screen of your current  experiment.

        """
        
        return self._window_size[1] / 2

    @property
    def size(self):
        """Getter for the size of the screen.
        
        Notes
        -----
        Each initialized experiment has its one screen (exp.screen). Please use always the
        screen of your current  experiment.

        """

        return self._window_size

    def clear(self):
        """Clear the screen.

        This will reset the default experimental background colour.

        """

        if self._open_gl:
            ogl.glClearColor(float(self._colour[0]) / 255,
                             float(self._colour[1]) / 255,
                             float(self._colour[2]) / 255, 0)
            ogl.glClear(ogl.GL_COLOR_BUFFER_BIT | ogl.GL_DEPTH_BUFFER_BIT)
        else:
            self._surface.fill(self._colour)
        if self._logging:
            expyriment._active_exp._event_file_log("Screen,cleared", 2)

    def save(self, filename):
        """Save the content of the screen as a picture.

        Parameters
        ----------
        filename : str
            name of the file to write (possible extensions are BMP,
            TGA, PNG, or JPEG, with the default being TGA)

        """

        pygame.image.save(self._surface, filename)
