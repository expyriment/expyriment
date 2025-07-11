"""
A screen.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import ctypes
import os
import platform

import pygame

try:
    import OpenGL.GL as ogl
except ImportError:
    ogl = None

from .. import _internals
from ..misc.geometry import position_to_coordinates
from ._input_output import Output


class Screen(Output):
    """A class implementing a screen output.

    Each experiment and all stimuli need a screen instance to function.
    They are expecting this screen instance to be referenced in
    expyriment._active_exp.screen.
    Calling expyriment.control.initialise(exp) will automatically create such
    a screen instance and will additionally reference it in exp.screen for
    easy access.

    """

    def __init__(self, colour, opengl, window_mode, window_size, no_frame,
                 display, display_resolution):
        """Create and set up a screen output.

        Notes
        -----
        CAUTION: We discourage creating a screen instance manually!

        Parameters
        ----------
        colour : (int, int, int)
            colour of the screen
        opengl : int or bool
            0/False - No OpenGL (no vsync / no blocking)
            1       - OpenGL (vsync / no blocking)
            2/True  - OpenGL (vsync / blocking)
        window_mode : bool
             if screen should be a window, fullscreen otherwise
        window_size : (int, int)
            size of the window in window_mode,
        no_frame : bool
            set True for windows (in window mode) with no frame;
            this parameter does not affect fullscreen mode
        display : int
            the display index to show the screen on (only has an effect if
            Pygame version >= 2)
        display_resolution : list or None
            the resolution of the display

        """

        Output.__init__(self)
        self._colour = colour
        if opengl is False:
            opengl = 0
        elif opengl is True:
            opengl = 2
        elif opengl > 2:
            warn_message = "OpenGL mode '{0}' does not exist. \
                OpenGL will be set to '2' (default)".format(opengl)
            print("Warning: " + warn_message)
            _internals.active_exp._event_file_warn("Screen,warning," + warn_message)
            opengl = 2
        self._opengl = opengl
        self._fullscreen = not window_mode
        self._window_size = window_size
        self._no_frame = no_frame
        self._display = display

        if ogl is None:
            warn_message = "PyOpenGL is not installed. \
OpenGL will be deactivated!"
            print("Warning: " + warn_message)
            _internals.active_exp._event_file_warn("Screen,warning," + warn_message)
            self._opengl = False

        # Set HiDPI mode on Windows (if SDL environment variable is not set)
        if platform.system() == "Windows":
            if "SDL_WINDOWS_DPI_AWARENESS" not in os.environ:
                os.environ["SDL_WINDOWS_DPI_AWARENESS"] = "permonitorv2"

        pygame.display.init()

        if _internals.active_exp.is_initialised:
            self._display_resolution = \
                        _internals.active_exp.screen.display_resolution
        else:
            if display_resolution is not None:
                self._display_resolution = display_resolution
            else:
                self._display_resolution = pygame.display.list_modes(
                    display=display)[0]

        # Change icon to Expyriment logo
        if platform.system() == "Windows":
            id_ = 'mycompany.myproduct.subproduct.version'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(id_)
        icon = pygame.image.load(os.path.join(os.path.split(__file__)[0],
                                              "..", "xpy_icon.png"))
        if platform.system() != "Darwin":
            icon = pygame.transform.smoothscale(icon, (32, 32))
        pygame.display.set_icon(icon)

        if not self._opengl:
            if self._fullscreen:
                self._surface = pygame.display.set_mode(
                    self._display_resolution, pygame.FULLSCREEN,
                    display=self._display)
            else:
                self._surface = pygame.display.set_mode(
                    self._window_size, display=self._display)
                pygame.display.set_caption('Expyriment')

        else:
            try:
                pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, 1)
            except Exception:
                pass

            pygame_mode = pygame.DOUBLEBUF | pygame.OPENGL

            if self._fullscreen:
                self._surface = pygame.display.set_mode(
                    self._display_resolution, pygame_mode | pygame.FULLSCREEN,
                    display=self._display, vsync=1)

            else:
                if no_frame:
                    pygame_mode = pygame_mode | pygame.NOFRAME
                self._surface = pygame.display.set_mode(
                    self._window_size, pygame_mode, display=self._display,
                    vsync=1)

                pygame.display.set_caption('Expyriment')

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
    def display(self):
        """Getter for display."""

        return self._display

    @property
    def opengl(self):
        """Getter for opengl."""

        return self._opengl

    @property
    def no_frame(self):
        """Getter for no_frame boolean"""

        return self._no_frame

    @property
    def window_mode(self):
        """Getter for window_mode."""

        return not self._fullscreen

    @property
    def window_size(self):
        """Getter for window_size."""

        return self._window_size

    @property
    def display_resolution(self):
        """Getter for display_resolution."""

        return self._display_resolution

    @property
    def monitor_resolution(self):
        """Getter for monitor_resolution.

        DEPRECATED! Use display_resolution instead.

        """
        # will be remove with 1.1
        return self._display_resolution

    def update(self, blocking=True):
        """Update the screen.

        This will flip the display double buffer.

        Parameters
        ----------
        blocking : bool, optional
            whether to block on vertical retrace (OpenGL only; default=True)

        """

        pygame.event.pump()
        pygame.display.flip()
        if self._opengl >= 2 and blocking:
            ogl.glBegin(ogl.GL_POINTS)
            ogl.glColor4f(0, 0, 0, 1)  # Opaque needed for non-alpha video!
            ogl.glVertex2i(0, 0)
            ogl.glEnd()
            ogl.glFinish()
        if self._logging:
            _internals.active_exp._event_file_log("Screen,updated", 2)

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

        try:
            stimuli = list(stimuli)
        except Exception:
            stimuli = [stimuli]

        if not self._opengl:
            rectangles = []
            for stim in stimuli:
                pos = stim.absolute_position
                stim_size = stim.surface_size
                rect_pos = position_to_coordinates(pos, self.size)
                rect_pos[0] -= stim_size[0] // 2
                rect_pos[1] -= stim_size[1] // 2
                rectangles.append(pygame.Rect(rect_pos, stim_size))
            pygame.display.update(rectangles)
            if self._logging:
                _internals.active_exp._event_file_log("Screen,stimuli updated,{0}"\
                                .format([stim.id for stim in stimuli]), 2)
            pygame.event.pump()

    @property
    def center_x(self):
        """Getter for X-coordinate of the screen center.

        Notes
        -----
        Each initialised experiment has its one screen (exp.screen).
        Please use always the screen of your current experiment.

        """

        return self.size[0] // 2

    @property
    def center_y(self):
        """Getter for the Y-coordinate of the screen center.

        Notes
        -----
        Each initialised experiment has its one screen (exp.screen).
        Please use always the screen of your current experiment.

        """

        return self.size[1] // 2

    @property
    def size(self):
        """Getter for the size of the screen.

        Notes
        -----
        Each initialised experiment has its one screen (exp.screen).
        Please use always the screen of your current experiment.

        """

        return self._surface.get_size()

    def clear(self):
        """Clear the screen.

        This will reset the default experimental background colour.

        """

        if self._opengl:
            ogl.glClearColor(float(self._colour[0]) / 255,
                             float(self._colour[1]) / 255,
                             float(self._colour[2]) / 255, 0)
            ogl.glClear(ogl.GL_COLOR_BUFFER_BIT | ogl.GL_DEPTH_BUFFER_BIT)
        else:
            self._surface.fill(self._colour)
        if self._logging:
            _internals.active_exp._event_file_log("Screen,cleared", 2)

    def save(self, filename):
        """Save the content of the screen as a picture.

        Parameters
        ----------
        filename : str
            name of the file to write (possible extensions are BMP,
            TGA, PNG, or JPEG, with the default being TGA)

        """

        if self._opengl:
            size = self._surface.get_size()
            ogl.glReadBuffer(ogl.GL_FRONT)
            buffer = ogl.glReadPixels(0, 0, size[0], size[1], ogl.GL_RGB,
                                      ogl.GL_UNSIGNED_BYTE)
            ogl.glReadBuffer(ogl.GL_BACK)
            surf = self._surface.copy()
            content = pygame.image.fromstring(buffer, size, "RGB", True)
            rect = pygame.Rect((0, 0), size)
            surf.blit(content, rect)
        else:
            surf = self._surface
        pygame.image.save(surf, filename)
