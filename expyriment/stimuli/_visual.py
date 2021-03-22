"""
This module contains the base classes for visual stimuli.
"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import tempfile
import os
import copy
import random
import itertools

import pygame
try:
    import OpenGL.GLU as oglu
    import OpenGL.GL as ogl
except ImportError:
    oglu = None
    ogl = None
try:
    import numpy as np
except ImportError:
    np = None

from . import defaults
from .. import _internals
from ._stimulus import Stimulus
from .. import misc
from ..misc import geometry, unicode2byte
from ..misc._timer import get_time

random.seed()


class _LaminaPanelSurface(object):
    """A class implementing an OpenGL surface."""

    # The following code is based on part of the Lamina module by David Keeney
    # (https://pypi.org/project/Lamina/) with some modifications to fit it
    # into expyriment (e.g. positioning)
    def __init__(self, surface, quadDims=(-1, 1, 1, 1),
                 position=(0, 0)):
        """Initialize new instance.

        Parameters
        ----------
        surface : pygame.Surface or numpy.array object
            surface to convert
        quadDims : (int,int), optional
        position : (int,int), optional

        """

        if isinstance(surface, pygame.Surface):
            # Fix for uneven surface sizes
            surface_size = surface.get_size()
            if surface_size[0] % 2 == 1:
                rect = pygame.Rect((0, 0), surface_size)
                s = pygame.surface.Surface((surface_size[0] + 1, surface_size[1]), pygame.SRCALPHA).convert_alpha()
                s.blit(surface, rect)
                surface = s
            surface_size = surface.get_size()
            if surface_size[1] % 2 == 1:
                rect = pygame.Rect((0, 0), surface_size)
                s = pygame.surface.Surface((surface_size[0], surface_size[1] + 1), pygame.SRCALPHA).convert_alpha()
                s.blit(surface, rect)
                surface = s
            self._winsize = surface.get_size()
        else:
            self._winsize = (len(surface[0]), len(surface))
        self._txtr = Visual._load_texture(surface)
        self._position = position
        left, top, width, height = quadDims
        right, bottom = left + width, top - height
        self._qdims = quadDims
        self.dims = ((left, top, 0), (right, top, 0),
                     (right, bottom, 0), (left, bottom, 0))
        self.refresh_position()

    def __del__(self):
        """Call glDeleteTextures when deconstruction the object."""

        if getattr(self, '_txtr', None) is not None:
            try:
                ogl.glDeleteTextures([self._txtr])
            except:
                pass

    def convertMousePos(self, pos):
        """Convert 2d pixel mouse pos to 2d gl units.

        Parameters
        ----------
        pos : (int, int)
            position of mouse

        """

        x0, y0 = pos
        x = int(x0 / self._winsize[0] * self._qdims[2] + self._qdims[0])
        y = int(y0 / self._winsize[1] * self._qdims[3] + self._qdims[1])
        return x, y

    def refresh_position(self):
        """Recalc where in modelspace quad needs to be to fill screen."""

        screensize = pygame.display.get_surface().get_size()
        bottomleft = oglu.gluUnProject(screensize[0] // 2 - \
                                       int(misc.round(self._winsize[0] / 2)) + \
                                       self._position[0],
                                       screensize[1] // 2 - \
                                       self._winsize[1] // 2 + \
                                       self._position[1], 0)
        bottomright = oglu.gluUnProject(screensize[0] // 2 + \
                                        self._winsize[0] // 2 + \
                                        self._position[0],
                                        screensize[1] // 2 - \
                                        self._winsize[1] // 2 + \
                                        self._position[1], 0)
        topleft = oglu.gluUnProject(screensize[0] // 2 - \
                                    int(misc.round(self._winsize[0] / 2)) + \
                                    self._position[0],
                                    screensize[1] // 2 + \
                                    int(misc.round(self._winsize[1] / 2)) + \
                                    self._position[1], 0)
        topright = oglu.gluUnProject(screensize[0] // 2 + \
                                     self._winsize[0] // 2 + \
                                     self._position[0],
                                     screensize[1] // 2 + \
                                     int(misc.round(self._winsize[1] / 2)) + \
                                     self._position[1], 0)


        self.dims = topleft, topright, bottomright, bottomleft
        width = topright[0] - topleft[0]
        height = topright[1] - bottomright[1]
        self._qdims = topleft[0], topleft[1], width, height

    def display(self):
        """Draw surface to a quad."""

        ogl.glEnable(ogl.GL_BLEND)
        ogl.glBlendFunc(ogl.GL_SRC_ALPHA, ogl.GL_ONE_MINUS_SRC_ALPHA)
        ogl.glEnable(ogl.GL_TEXTURE_2D)
        ogl.glBindTexture(ogl.GL_TEXTURE_2D, self._txtr)
        ogl.glTexEnvf(ogl.GL_TEXTURE_ENV, ogl.GL_TEXTURE_ENV_MODE,
                      ogl.GL_REPLACE)
        ogl.glTexParameterfv(ogl.GL_TEXTURE_2D, ogl.GL_TEXTURE_MIN_FILTER,
                           ogl.GL_LINEAR)
        ogl.glBegin(ogl.GL_QUADS)
        ogl.glTexCoord2f(0.0, 1.0)
        ogl.glVertex3f(*self.dims[0])
        ogl.glTexCoord2f(1.0, 1.0)
        ogl.glVertex3f(*self.dims[1])
        ogl.glTexCoord2f(1.0, 0.0)
        ogl.glVertex3f(*self.dims[2])
        ogl.glTexCoord2f(0.0, 0.0)
        ogl.glVertex3f(*self.dims[3])
        ogl.glEnd()
        ogl.glDisable(ogl.GL_BLEND)
        ogl.glDisable(ogl.GL_TEXTURE_2D)
    # End of code based on Lamina module


class Visual(Stimulus):
    """A class implementing a general visual stimulus.

    All other visual stimuli should be subclassed from this class since it
    entails code for converting Pygame surfaces into OpenGL textures. This
    allows for having hardware acceleration (including waiting for the
    vertical retrace) while still being able to manipulate stimuli in an
    easy way (based on Pygame surfaces).

    """


    # The following code is based on part of the Lamina module by David Keeney
    # (https://pypi.org/project/Lamina/) with some modifications to fit it
    # into expyriment (e.g. positioning)
    @staticmethod
    def _load_texture(surf):
        """Load surface into texture object.

        Returns a texture object.

        Parameters
        ----------
        surf : pygame.Surface or numpy.array object
            surface to make texture from

        """

        txtr = ogl.glGenTextures(1)
        if isinstance(surf, pygame.Surface):
            textureData = pygame.image.tostring(surf, "RGBA", 1)
            colours = ogl.GL_RGBA
            width, height = surf.get_size()
        else:
            textureData = surf
            if textureData.shape[2] == 3:
                colours = ogl.GL_RGB
            elif textureData.shape[2] == 4:
                colours = ogl.GL_RGBA
            width, height = len(surf[0]), len(surf)
        ogl.glEnable(ogl.GL_TEXTURE_2D)
        ogl.glBindTexture(ogl.GL_TEXTURE_2D, txtr)
        ogl.glTexImage2D(ogl.GL_TEXTURE_2D, 0, colours, width, height, 0,
          colours, ogl.GL_UNSIGNED_BYTE, textureData)
        ogl.glTexParameterf(ogl.GL_TEXTURE_2D,
                            ogl.GL_TEXTURE_MAG_FILTER,
                            ogl.GL_NEAREST)
        ogl.glTexParameterf(ogl.GL_TEXTURE_2D,
                            ogl.GL_TEXTURE_MIN_FILTER,
                            ogl.GL_NEAREST)
        ogl.glDisable(ogl.GL_TEXTURE_2D)
        return txtr
    # End of code based on Lamina module

    def __init__(self, position=None, log_comment=None):
        """Create a visual stimulus.

        Parameters
        ----------
        position : (int,int), optional
            position of the stimulus
        log_comment : str, optional
            comment for the event log file

        """

        Stimulus.__init__(self, log_comment)
        if position:
            self._position = list(position)
        else:
            self._position = list(defaults.visual_position)
        self._surface = None
        self._is_preloaded = False
        self._parent = None
        self._ogl_screen = None
        self._is_compressed = False
        self._compression_filename = None

        self._was_compressed_before_preload = None

        if not _internals.active_exp.is_initialized:
            warn_message = "Stimulus created before initializing " + \
                           "(experiment defaults won't apply)!"
            print("Warning: " + warn_message)

    _exception_message = "Cannot call {0} on preloaded " \
                                     "or compressed stimulus!"

    def __del__(self):
        """ Clear surface and ogl_screen when when the objects is deconstructed.

        """

        try:
            self.clear_surface()
        except:
            pass
        if self._compression_filename is not None:
            try:
                os.remove(self._compression_filename)
            except:
                pass

    @property
    def position(self):
        """Getter for position."""

        return self._position

    @position.setter
    def position(self, value):
        """Setter for position.

        When using OpenGL, this can take longer then 1ms!

        """

        self.reposition(value)

    @property
    def polar_position(self):
        """Getter for the position in polar coordinates (radial, angle[degrees])"""

        return geometry.cartesian2polar(self._position)

    @polar_position.setter
    def polar_position(self, value):
        """Setter for the position in polar coordinates (radial, angle[degrees])

        When using OpenGL, this can take longer then 1ms!

        """

        pos = geometry.polar2cartesian(value)
        self.reposition((int(misc.round(pos[0])), int(misc.round(pos[1]))))

    @property
    def absolute_position(self):
        """Getter for absolute_position.

        Notes
        -----
        The absolute position differs for instance from the (relative) position, if the
        stimulus is plotted ontop of another stimulus, which has not the position (0,0).

        """

        if self._parent:
            return (self._parent.absolute_position[0] + self.position[0],
                    self._parent.absolute_position[1] + self.position[1])
        else:
            return self.position

    @property
    def is_compressed(self):
        """Getter for is_compressed."""

        return self._is_compressed

    @property
    def has_surface(self):
        """Getter for has_surface."""

        if self._surface is not None:
            return True
        else:
            return self.is_compressed

    @property
    def surface_size(self):
        """ Getter for surface_size."""

        return self._get_surface().get_size()

    def get_surface_copy(self):
        """Returns a copy of the Pygame surface of the stimulus

        Returns
        -------
        surface: Pygame.surface

        Notes
        -----
        see also set_surface

        """

        return self._get_surface().copy()

    def get_pixel_array(self):
        """Return a 2D array referencing the surface pixel data.

        Returns
        -------
        pixel_array: Pygame.PixelArray
            a 2D array referencing the surface pixel data

        Notes
        -----
        see also set_surface

        """

        return pygame.PixelArray(self.get_surface_copy())

    def get_surface_array(self, replace_transparent_with_colour=None):
        """Get a 3D array containing the surface pixel data.

        Returns
        -------
        surface_array : numpy.ndarray
            a 3D array containing the surface pixel data
            using RGBA coding.

        """

        if np is None:
            message = """get_rgba_array can not be used.
        The Python package 'Numpy' is not installed."""
            raise ImportError(message)

        surface = self.get_surface_copy()
        s = surface.get_size()
        pixel = pygame.surfarray.pixels3d(surface)
        alpha = pygame.surfarray.pixels_alpha(surface)
        rtn = np.empty((s[0], s[1], 4), dtype=np.int)
        if replace_transparent_with_colour is None:
            rtn[:, :, 0:3] = pixel
            rtn[:, :, 3] = alpha
        else:
            alpha = alpha.T / 255.0
            background = (np.ones(pixel.shape) * replace_transparent_with_colour)
            tmp = pixel.T * alpha + background.T * (1-alpha)
            rtn[:, :, 0:3] = tmp.T
            rtn[:, :, 3] = 255
        return rtn


    def set_surface(self, surface):
        """Set the surface of the stimulus

        This method overwrites the surface of the stimulus. It can also handle
        surfaces in form of pygame.PixelArray or Numpy 3D array (RGB or RGBA)
        representations.

        Parameters
        ----------
        surface: pygame.Surface or pygame.PixelArray or numpy.ndarray
            a representation of the new surface

        Returns
        -------
        succeeded: boolean
            setting surface was successful or not

        Notes
        -----
        CAUTION: This is an expert's method.
        The method can be used together with get_surface() & get_pixel_array()
        to apply low-level Pygame operations on stimuli. However, users should
        be aware of what they are doing, because the incorrect usage of this
        methods might affect the stability of the experiment.

        """

        if isinstance(surface, pygame.PixelArray):
            return self._set_surface(surface.make_surface())
        elif np is not None and isinstance(surface, np.ndarray):
            if surface.shape[2] == 3: # RGB
                return self._set_surface(pygame.surfarray.make_surface(surface))

            elif surface.shape[2] == 4: # RGBA
                size = surface.shape[0:2]
                new_surface = pygame.Surface(size)
                new_surface = new_surface.convert_alpha()
                [new_surface.set_at((x, y), surface[x,y,:]) \
                                for x,y in itertools.product(range(size[0]), range(size[1])) ]
                return self._set_surface(new_surface)

            else:
                return False
        elif isinstance(surface, pygame.Surface):
            return self._set_surface(surface)
        else:
            return False

    def _create_surface(self):
        """Get the surface of the stimulus.

        This method has to be overwritten for all subclasses individually!

        """

        surface = pygame.surface.Surface((0, 0))
        return surface

    def _set_surface(self, surface):
        """Set the surface (from internal use only).

        Parameters
        ----------
        surface : pygame surface
            surface to be set

        """

        if self.is_compressed:
            return False
        else:
            self._surface = surface
            return True

    def _get_surface(self):
        """Get the surface."""

        if self._surface:
            return self._surface
        else:
            if self.is_compressed:
                tmp = pygame.image.load(
                    self._compression_filename).convert_alpha()
            else:
                tmp = self._create_surface()
            return tmp

    def copy(self):
        """Deep copy of the visual stimulus.

        Returns
        -------
        copy : deep copy of self

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        has_surface = self.has_surface
        is_preloaded = self.is_preloaded
        is_compressed = self.is_compressed
        if has_surface:
            surface_backup = self._get_surface()
            surface_copy = self._get_surface().copy()
            self._surface = None
        rtn = Stimulus.copy(self)
        if has_surface:
            self._surface = surface_backup
            rtn._surface = surface_copy
            rtn._is_preloaded = False
            rtn._ogl_screen = None
            rtn._is_compressed = False
            rtn._compression_filename = None
        if is_preloaded:
            if _internals.active_exp.screen.open_gl:
                self._ogl_screen = _LaminaPanelSurface(
                    self._get_surface(),
                    position=self.position)
            rtn.preload()
        if is_compressed:
            rtn.compress()
        rtn._was_compressed_before_preload = \
                self._was_compressed_before_preload
        return rtn

    def distance(self, other):
        """Surface center distance.

        This method computes the distance between the surface center
        of this and another visual stimulus.

        Parameters
        ----------
        other : stimulus
            the other visual stimulus

        Returns
        -------
        dist : float
            distance between surface centers

        """

        return geometry.XYPoint(
            self.position).distance(geometry.XYPoint(other.position))

    def replace(self, dummy):
        raise DeprecationWarning("Replace is an obsolete method. Please use reposition!")

    def reposition(self, new_position):
        """Move stimulus to a new position.

        When using OpenGL, this can take longer then 1ms!

        Parameters
        ----------
        new_position : tuple (x,y)
            translation along x and y axis

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        --------
        see also move

        """
        return self.move((new_position[0] - self.position[0],
                          new_position[1] - self.position[1]))

    def move(self, offset):
        """Moves the stimulus in 2D space.

        When using OpenGL, this can take longer then 1ms!

        Parameters
        ----------
        offset : tuple (x,y)
            translation along x and y axis

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        --------
        see also reposition

        """

        start = get_time()
        moved = False
        if offset[0] != 0:
            self._position[0] = self._position[0] + offset[0]
            moved = True
        if offset[1] != 0:
            self._position[1] = self._position[1] + offset[1]
            moved = True
        if moved and self._ogl_screen is not None:
            self._ogl_screen.refresh_position()
        return int((get_time() - start) * 1000)

    def inside_stimulus(self, stimulus, mode="visible"):
        """Check if stimulus is inside another stimulus.

        Parameters
        ----------
        stimulus : expyriment stimulus
            the other stimulus
        mode : mode (str), optional
            "visible": based on non-transparent pixels or
            "surface": based on pixels in pygame surface
            (default = visible")

        Returns
        -------
        out : bool

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        if mode == "visible":
            screen_size = _internals.active_exp.screen.surface.get_size()
            self_size = self.surface_size
            other_size = stimulus.surface_size
            self_pos = geometry.position2coordinates(self.position,
                                                     screen_size)
            self_pos[0] -= self_size[0] // 2
            self_pos[1] -= self_size[1] // 2
            if self_size[0] % 2 == 0:
                self_pos[0] += 1
            if self_size[1] % 2 == 0:
                self_pos[1] += 1
            other_pos = geometry.position2coordinates(stimulus.position,
                                                      screen_size)
            other_pos[0] -= other_size[0] // 2
            other_pos[1] -= other_size[1] // 2
            if other_size[0] % 2 == 0:
                other_pos[0] += 1
            if other_size[1] % 2 == 0:
                other_pos[1] += 1
            offset = (-self_pos[0] + other_pos[0], -self_pos[1] + other_pos[1])
            self_mask = pygame.mask.from_surface(self._get_surface())
            other_mask = pygame.mask.from_surface(stimulus._get_surface())
            overlap = self_mask.overlap_area(other_mask, offset)
            if overlap > 0 and overlap == self_mask.count():
                return True
            else:
                return False

        elif mode == "surface":
            screen_size = _internals.active_exp.screen.surface.get_size()
            sx, sy = geometry.coordinates2position(self.absolute_position,
                                                   screen_size)
            selfrect = pygame.Rect((0, 0), self.surface_size)
            if self.surface_size[0] % 2 == 0:
                sx += 1
            if self.surface_size[1] % 2 == 0:
                sy += 1
            selfrect.center = (sx, sy)
            ox, oy = geometry.coordinates2position(stimulus.absolute_position,
                                                   screen_size)
            if stimulus.surface_size[0] % 2 == 0:
                ox += 1
            if stimulus.surface_size[1] % 2 == 0:
                oy += 1
            stimrect = pygame.Rect((0, 0), stimulus.surface_size)
            stimrect.right = stimrect.right + 1
            stimrect.bottom = stimrect.bottom + 1
            stimrect.center = (ox, oy)
            if stimrect.contains(selfrect):
                return True
            else:
                return False

    def overlapping_with_stimulus(self, stimulus, mode="visible",
                                  use_absolute_position=True):
        """Check if stimulus is overlapping with another stimulus.

        Parameters
        ----------
        stimulus : expyriment stimulus
            the other stimulus
        mode : mode (str), optional
            "visible": based on non-transparent pixels or
            "surface": based on pixels in pygame surface
            (default = visible")
        use_absolute_position : bool, optional
            use absolute_position of stimuli (default) instead of position

        Returns
        -------
        overlapping : bool
            are stimuli overlapping or not
        overlap : (int, int)
            the overlap (x, y) in pixels. If mode is 'surface', the argument
            will always be None.

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        CAUTION: Please note that if a stimulus is plotted on another smaller
        stimulus, such that it is not fully visible on screen, this method will
        still check overlapping of the full stimulus! Due to a current bug in
        Pygame, we can right now not change this.

        """

        if mode == "visible":
            screen_size = _internals.active_exp.screen.surface.get_size()
            self_size = self.surface_size
            other_size = stimulus.surface_size
            if use_absolute_position:
                self_pos = geometry.position2coordinates(
                    self.absolute_position, screen_size)
                self_pos[0] -= self_size[0] // 2
                self_pos[1] -= self_size[1] // 2
                if self_size[0] % 2 == 0:
                    self_pos[0] += 1
                if self_size[1] % 2 == 0:
                    self_pos[1] += 1

                other_pos = geometry.position2coordinates(
                    stimulus.absolute_position, screen_size)
                other_pos[0] -= other_size[0] // 2
                other_pos[1] -= other_size[1] // 2
                if other_size[0] % 2 == 0:
                    other_pos[0] += 1
                if other_size[1] % 2 == 0:
                    other_pos[1] += 1

            else:
                self_pos = geometry.position2coordinates(
                    self.position, screen_size)
                self_pos[0] -= self_size[0] // 2
                self_pos[1] -= self_size[1] // 2
                if self_size[0] % 2 == 0:
                    self_pos[0] += 1
                if self_size[1] % 2 == 0:
                    self_pos[1] += 1

                other_pos = geometry.position2coordinates(
                    stimulus.position, screen_size)
                other_pos[0] -= other_size[0] // 2
                other_pos[1] -= other_size[1] // 2
                if other_size[0] % 2 == 0:
                    other_pos[0] += 1
                if other_size[1] % 2 == 0:
                    other_pos[1] += 1

            offset = (-self_pos[0] + other_pos[0], -self_pos[1] + other_pos[1])
            self_mask = pygame.mask.from_surface(self._get_surface())
            other_mask = pygame.mask.from_surface(stimulus._get_surface())
            overlap = self_mask.overlap_area(other_mask, offset)
            if overlap > 0:
                return True, overlap
            else:
                return False, overlap

        elif mode == "surface":
            screen_size = _internals.active_exp.screen.surface.get_size()
            if use_absolute_position:
                sx, sy = geometry.coordinates2position(
                    self.absolute_position, screen_size)
                ox, oy = geometry.coordinates2position(
                    stimulus.absolute_position, screen_size)
            else:
                sx, sy = geometry.coordinates2position(
                    self.position, screen_size)
                ox, oy = geometry.coordinates2position(
                    stimulus.position, screen_size)
            selfrect = pygame.Rect((0, 0), self.surface_size)
            if self.surface_size[0] % 2 == 0:
                sx += 1
            if self.surface_size[1] % 2 == 0:
                sy += 1
            selfrect.center = (sx, sy)
            stimrect = pygame.Rect((0, 0), stimulus.surface_size)
            if stimulus.surface_size[0] % 2 == 0:
                ox += 1
            if stimulus.surface_size[1] % 2 == 0:
                oy += 1
            stimrect.right = stimrect.right + 1
            stimrect.bottom = stimrect.bottom + 1
            stimrect.center = (ox, oy)
            if selfrect.colliderect(stimrect):
                return True, None
            else:
                return False, None

    def overlapping_with_position(self, position, mode="visible",
                                  use_absolute_position=True):
        """Check if stimulus is overlapping with a certain position.

        Parameters
        ----------
        position : (int, int)
            position to check for overlapping
        mode : mode (str), optional
            "visible": based on non-transparent pixels or
            "rectangle": based on pixels in pygame surface
            (default = visible")
        use_absolute_position : bool, optional
            use absolute_position of stimulus (default) instead of position

        Returns
        -------
        overlapping : bool

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        CAUTION: Please note that if a stimulus is plotted on another smaller
        stimulus, such that it is not fully visible on screen, this method will
        still check overlapping of the full stimulus! Due to a current bug in
        Pygame, we can right now not change this.

        """

        if mode == "visible":
            screen_size = _internals.active_exp.screen.surface.get_size()
            self_size = self.surface_size
            if use_absolute_position:
                self_pos = geometry.position2coordinates(
                    self.absolute_position, screen_size)
                self_pos[0] -= self_size[0] // 2
                self_pos[1] -= self_size[1] // 2
                if self_size[0] % 2 == 0:
                    self_pos[0] += 1
                if self_size[1] % 2 == 0:
                    self_pos[1] += 1

            else:
                self_pos = geometry.position2coordinates(
                    self.position, screen_size)
                self_pos[0] -= self_size[0] // 2
                self_pos[1] -= self_size[1] // 2
                if self_size[0] % 2 == 0:
                    self_pos[0] += 1
                if self_size[1] % 2 == 0:
                    self_pos[1] += 1

            pos = geometry.position2coordinates(position, screen_size)
            offset = (int(pos[0] - self_pos[0]), int(pos[1] - self_pos[1]))
            self_mask = pygame.mask.from_surface(self._get_surface())
            overlap = False
            if 0 <= offset[0] < self_size[0] and 0 <= offset[1] < self_size[1]:
                overlap = self_mask.get_at(offset)
                if overlap > 0:
                    overlap = True
                else:
                    overlap = False
            return overlap

        elif mode == "surface":
            screen_size = _internals.active_exp.screen.surface.get_size()
            if use_absolute_position:
                sx, sy = geometry.coordinates2position(self.absolute_position,
                                                       screen_size)
            else:
                sx, sy = geometry.coordinates2position(self.position,
                                                       screen_size)
            selfrect = pygame.Rect((0, 0), self.surface_size)
            if self.surface_size[0] % 2 == 0:
                sx += 1
            if self.surface_size[1] % 2 == 0:
                sy += 1
            selfrect.center = (sx, sy)
            p = geometry.coordinates2position(position, screen_size)
            p = (position[0] + screen_size[0] // 2,
                 position[1] + screen_size[1] // 2)
            p = geometry.coordinates2position(position, screen_size)
            if selfrect.collidepoint(p):
                return True
            else:
                return False

    def plot(self, stimulus):
        """Plot the stimulus on the surface of another stimulus.

        Use this to plot more than one stimulus and to present them at the
        same time afterwards by presenting the stimulus on which they were
        plotted on.

        Parameters
        ----------
        stimulus : expyriment stimulus
            stimulus to whose surface should be plotted

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        start = get_time()
        if not stimulus._set_surface(stimulus._get_surface()):
            raise RuntimeError(Visual._exception_message.format(
                "plot()"))
        stimulus.unload(keep_surface=True)
        self._parent = stimulus
        surface = self._get_surface()
        surface_size = surface.get_size()
        rect = pygame.Rect((0, 0), surface_size)
        x, y = geometry.position2coordinates(self.position,
                                             stimulus.surface_size)
        if surface_size[0] % 2 == 0:
            x += 1
        if surface_size[1] % 2 == 0:
            y += 1
        rect.center = (x, y)
        stimulus._get_surface().blit(surface, rect)
        if self._logging:
            _internals.active_exp._event_file_log(
                "Stimulus,plotted,{0},{1}".format(self.id, stimulus.id), 2)
        return int((get_time() - start) * 1000)

    def clear_surface(self):
        """Clear the stimulus surface.

        Surfaces are automatically created after any surface operation
        (presenting, plotting, rotating, scaling, flipping etc.) and preloading.
        If the stimulus was preloaded, this method unloads the stimulus.
        This method is functionally equivalent with unload(keep_surface=False).

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        start = get_time()
        if self.is_preloaded:
            self.unload(keep_surface=False)
        self._is_compressed = False
        self._set_surface(None)
        if self._logging:
            _internals.active_exp._event_file_log(
                            "Stimulus,surface cleared,{0}".format(self.id), 2)
        return int((get_time() - start) * 1000)

    def compress(self):
        """"Compress the stimulus.

        This will create a temporary file on the disk where the surface of the
        stimululs is written to.
        The surface will now be read from the disk to free memory.
        Compressed stimuli cannot do surface operations!
        Preloading comressed stimuli is possible and highly recommended.
        Depending on the size of the stimulus, this method may take some time
        to compute!

        Returns
        -------
        time : int
            the time it took to execute this method

        """

        start = get_time()
        if self.is_compressed is False:
            if self._compression_filename is None:
                fid, self._compression_filename = tempfile.mkstemp(
                    dir=defaults.tempdir, suffix=".tga")
                os.close(fid)
            pygame.image.save(self._get_surface(), self._compression_filename)
            self._is_compressed = True
            self._surface = None

            if self._logging:
                _internals.active_exp._event_file_log(
                                "Stimulus,compressed,{0}".format(self.id), 2)
        return int((get_time() - start) * 1000)

    def decompress(self):
        """Decompress the stimulus.

        This will decompress the stimulus.
        The surface will now be read from memory again.
        Depending on the size of the stimulus, this method may take some time
        to compute!

        Returns
        -------
        time : int
            the time it took to execute this method

        """

        start = get_time()
        if self.is_compressed:
            self._surface = pygame.image.load(
                self._compression_filename).convert_alpha()
            self._is_compressed = False

            if self._logging:
                _internals.active_exp._event_file_log(
                            "Stimulus,decompressed,{0}".format(self.id), 2)
        return int((get_time() - start) * 1000)

    def preload(self, inhibit_ogl_compress=False):
        """Preload the stimulus to memory.

        This will prepare the stimulus for a fast presentation.
        In OpenGL mode this method creates an OpenGL texture based on the
        surface of the stimulus.
        When OpenGL is switched off, this method will create a surface if it
        doesn't exists yet.
        If stimuli are not preloaded manually, this will happen
        automatically during presentation. However, stimulus presentation will
        take some time then!

        Always preload your stimuli when a timing accurate presentation is
        needed!

        Parameters
        ----------
        inhibit_ogl_compress : bool, optional
            inhibits OpenGL stimuli to be automatically compressed
            (default=False)

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        start = get_time()
        if not _internals.active_exp.is_initialized:
            message = "Can't preload stimulus. Expyriment needs to be " + \
                      "initialized before preloading a stimulus."
            raise RuntimeError(message)
        self._was_compressed_before_preload = self.is_compressed
        if not self.is_preloaded:
            if _internals.active_exp.screen.open_gl:
                self._ogl_screen = _LaminaPanelSurface(
                    self._get_surface(),
                    position=self.position)
                if not inhibit_ogl_compress:
                    self.compress()
            else:
                self.decompress()
                self._set_surface(self._get_surface())
            self._is_preloaded = True
        if self._logging:
            _internals.active_exp._event_file_log(
                                "Stimulus,preloaded,{0}".format(self.id), 2)

        return int((get_time() - start) * 1000)

    def unload(self, keep_surface=False):
        """Unload the stimulus from memory.

        This will unload preloaded stimuli.
        In OpenGL mode, this method will remove the reference to the OpenGL
        texture and the surface (when 'keep_surface' is False).
        When OpenGL is switched off, the reference to the surface will be
        removed (when 'keep_surface' is False).

        Parameters
        ----------
        keep_surface : bool, optional
            keep the surface after unload (default=False)

        Returns
        -------
        time : int
            the time it took to execute this method

        See Also
        --------
        clear_surface

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        start = get_time()
        if _internals.active_exp.screen.open_gl:
            self._ogl_screen = None
            if self.is_preloaded and not self._was_compressed_before_preload \
                and keep_surface:
                self.decompress()
        else:  # Pygame surface
            if self.is_preloaded and self._was_compressed_before_preload \
                and keep_surface:
                self.compress()
        if self.is_preloaded and self._logging:
            _internals.active_exp._event_file_log("Stimulus,unloaded,{0}"\
                                       .format(self.id), 2)
        if not keep_surface:
            self._is_compressed = False
            self._surface = None
            if self._logging:
                _internals.active_exp._event_file_log("Stimulus,surface cleared,{0}"\
                                       .format(self.id), 2)

        self._is_preloaded = False
        return int((get_time() - start) * 1000)

    @property
    def is_preloaded(self):
        """Getter for is_preloaded."""

        return self._is_preloaded

    def present(self, clear=True, update=True, log_event_tag=None):
        """Present the stimulus on the screen.

        This clears and updates the screen automatically.
        When not preloaded, depending on the size of the stimulus, this method
        can take some time to compute!

        Parameters
        ----------
        clear : bool, optional
            if True the screen will be cleared automatically
            (default = True)
        update : bool, optional
            if False the screen will be not be updated automatically
            (default = True)
        log_event_tag : numeral or string, optional
            if log_event_tag is defined and if logging is switched on for this
            stimulus (default), a summary of the inter-event-intervalls are
            appended at the end of the event file

        Returns
        -------
        time : int
            the time it took to execute this method

        """

        if not _internals.active_exp.is_initialized or\
                             _internals.active_exp.screen is None:
            raise RuntimeError("Cannot not find a screen!")

        start = get_time()
        preloading_required = not(self.is_preloaded)

        if clear:
            _internals.active_exp.screen.clear()
        if preloading_required:
            # Check if stimulus has surface
            keep_surface = self.has_surface
            self.preload(inhibit_ogl_compress=True)

        if _internals.active_exp.screen.open_gl:
            self._ogl_screen.display()
        else:
            screen = _internals.active_exp.screen.surface
            rect = pygame.Rect((0, 0), self.surface_size)
            screen_size = screen.get_size()
            x, y = geometry.position2coordinates(self.position, screen_size)
            if self.surface_size[0] % 2 == 0:
                x += 1
            if self.surface_size[1] % 2 == 0:
                y += 1
            rect.center = (x, y)
            screen.blit(self._get_surface(), rect)
        if self._logging:
            _internals.active_exp._event_file_log("Stimulus,drawn,{0}"\
                                   .format(self.id), 2,
                                 log_event_tag=log_event_tag)
        if update:
            _internals.active_exp.screen.update()
        if self._logging:
            _internals.active_exp._event_file_log("Stimulus,presented,{0}"\
                                   .format(self.id), 1,
                                 log_event_tag=log_event_tag)
        if preloading_required:
            self.unload(keep_surface=keep_surface)

        return int((get_time() - start) * 1000)

    def save(self, filename):
        """Save the stimulus as image.

        Parameters
        ----------
        filename : str
            name of the file to write (possible extensions are BMP, TGA, PNG,
            or JPEG with TGA being the default)

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        parts = filename.split(".")
        if len(parts) > 1:
            parts[-1] = parts[-1].lower()
        else:
            parts.append("tga")
        filename = ".".join(parts)
        pygame.image.save(self._get_surface(), unicode2byte(filename))

    def picture(self):
        """Return the stimulus as Picture stimulus.

        This will create a temporary file on the hard disk where the image is
        saved to.

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        from . import _picture
        fid, location = tempfile.mkstemp(dir=defaults.tempdir,
                                         suffix=".tga")
        os.close(fid)
        pygame.image.save(self._get_surface(), location)
        return _picture.Picture(filename=location)

    def rotate(self, degree, filter=True):
        """Rotate the stimulus.

        This is a surface operation. After this, a surface will be present!
        Rotating goes along with a quality loss. Thus, rotating an already
        rotated stimulus is not a good idea.

        Parameters
        ----------
        degree : int
            degree to rotate counterclockwise
        filter : bool, optional
            filter the surface content for better quality (default = True)

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        start = get_time()
        if not self._set_surface(self._get_surface()):
            raise RuntimeError(Visual._exception_message.format(
                "rotate()"))
        self.unload(keep_surface=True)
        if filter:
            self._set_surface(pygame.transform.rotozoom(self._get_surface(),
                                                        degree, 1.0))
        else:
            self._set_surface(pygame.transform.rotate(self._get_surface(),
                                                      degree))
        if self._logging:
            _internals.active_exp._event_file_log(
                "Stimulus,rotated,{0}, degree={1}".format(self.id, degree))
        return int((get_time() - start) * 1000)

    def scale(self, factors):
        """Scale the stimulus.

        This is a surface operation. After this, a surface will be present!
        Negative scaling values will flip the stimulus.
        Scaling goes along with a quality loss. Thus, scaling an already
        scaled stimulus is not a good idea.

        Parameters
        ----------
        factors : (int, int) or (float, float)
            tuple representing the x and y factors to scale or a single number.
            In the case of a single number x and y scaling will be the
            identical (i.e., proportional scaling)

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        start = get_time()
        if not self._set_surface(self._get_surface()):
            raise RuntimeError(Visual._exception_message.format(
                "scale()"))
        self.unload(keep_surface=True)
        flip = [False, False]
        if isinstance(factors, (int, float)):
            factors = [factors, factors]
        else:
            factors = list(factors)
        if factors[0] < 0:
            flip[0] = True
            factors[0] = abs(factors[0])
        if factors[1] < 0:
            flip[1] = True
            factors[1] = abs(factors[1])
        self._set_surface(pygame.transform.smoothscale(
            self._get_surface(),
            (int(misc.round(self.surface_size[0] * factors[0])),
             int(misc.round(self.surface_size[1] * factors[1])))))
        if True in flip:
            self.flip(flip)
        if self._logging:
            _internals.active_exp._event_file_log(
                "Stimulus,scaled,{0}, factors={1}".format(self.id, factors), 2)
        return int((get_time() - start) * 1000)

    def scale_to_fullscreen(self, keep_aspect_ratio=True):
        """Scale the stimulus to fullscreen.

        This is a surface operation. After this, a surface will be present!
        Scaling goes along with a quality loss. Thus, scaling an already
        scaled stimulus is not a good idea.

        Parameters
        ----------
        keep_aspect_ratio : boolean, optional
            if this boolean is False, stimulus will be stretched so that it
            fills out the whole screen (default = False)

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        start = get_time()
        if not self._set_surface(self._get_surface()):
            raise RuntimeError(Visual._exception_message.format(
                "scale_to_fullscreen()"))
        surface_size = self.surface_size
        screen_size = _internals.active_exp.screen.surface.get_size()
        scale = (screen_size[0]/float(surface_size[0]),
                     screen_size[1]/float(surface_size[1]))
        if keep_aspect_ratio:
            scale = [min(scale)]*2
        self.scale(factors=scale)
        return int((get_time() - start) * 1000)

    def flip(self, booleans):
        """Flip the stimulus.

        This is a surface operation. After this, a surface will be present!

        Parameters
        ----------
        booleans : (bool, bool)
            booleans to flip or not

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        start = get_time()
        if not self._set_surface(self._get_surface()):
            raise RuntimeError(Visual._exception_message.format(
                "flip()"))
        self.unload(keep_surface=True)
        self._set_surface(pygame.transform.flip(self._get_surface(),
                                                  booleans[0], booleans[1]))
        if self._logging:
            _internals.active_exp._event_file_log(
            "Stimulus,flipped,{0}, booleans={1}".format(self.id, booleans), 2)
        return int((get_time() - start) * 1000)

    def blur(self, level):
        """Blur the stimulus.

        This blurs the stimulus, by scaling it down and up by the factor of
        'level'.

        Parameters
        ----------
        level : int
            level of bluring

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        start = get_time()
        self.scale((1.0 / level, 1.0 / level))
        self.scale((level, level))
        if self._logging:
            _internals.active_exp._event_file_log(
                "Stimulus,blured,{0}, level={1}".format(self.id, level), 2)
        return int((get_time() - start) * 1000)

    def scramble(self, grain_size):
        """Scramble the stimulus.

        Attention: If the surface size is not a multiple of the grain size,
        you may loose some pixels on the edge.

        Parameters
        ----------
        grain_size : int or (int, int)
            size of a grain (use tuple of integers for different width & height)

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """

        start = get_time()
        if isinstance(grain_size, int):
            grain_size = [grain_size, grain_size]
        # Make Rect list
        if not self._set_surface(self._get_surface()):
            raise RuntimeError(Visual._exception_message.format(
                "scramble()"))
        s = self.surface_size
        source = []
        for r in range(s[1] // int(grain_size[1])):
            for c in range(s[0] // int(grain_size[0])):
                xy = (c * int(grain_size[0]), r * int(grain_size[1]))
                source.append(pygame.Rect(xy, grain_size))
        # Make copy and shuffle
        dest = copy.deepcopy(source)
        random.shuffle(dest)
        # Create a new surface
        tmp_surface = pygame.surface.Surface(
            s, pygame.SRCALPHA).convert_alpha()
        for n, s in enumerate(source):
            tmp_surface.blit(self._get_surface(), dest[n], s)
        self._set_surface(tmp_surface)

        if self._logging:
            _internals.active_exp._event_file_log(
                            "Stimulus,scrambled,{0}, grain_size={1}".format(
                                     self.id, grain_size), 2)
        return int((get_time() - start) * 1000)

    def add_noise(self, grain_size, percentage, colour):
        """Add visual noise on top of the stimulus.

        This function might take very long for large stimuli.

        Parameters
        ----------
        grain_size : int
            size of the grains for the noise
        percentage : int
            percentage of covered area
        colour : (int, int, int)
            colour (RGB) of the noise

        Returns
        -------
        time : int
            the time it took to execute this method

        Notes
        -----
        Depending on the size of the stimulus, this method may take some time
        to compute!

        """
        from . import _rectangle
        start = get_time()
        if not self._set_surface(self._get_surface()):
            raise RuntimeError(Visual._exception_message.format(
                "add_noise()"))
        self.unload(keep_surface=True)
        number_of_pixel_x = int(self.surface_size[0] // grain_size) + 1
        number_of_pixel_y = int(self.surface_size[1] // grain_size) + 1
        seq = list(range(number_of_pixel_x * number_of_pixel_y))
        random.seed()
        random.shuffle(seq)

        for idx in seq[:int(len(seq) * (percentage) / 100.0)]:
            x = (idx % number_of_pixel_x) * grain_size
            x = int(self.surface_size[0] // 2 - grain_size // 2 - x)
            y = (idx // number_of_pixel_x) * grain_size
            y = int(self.surface_size[1] // 2 - grain_size // 2 - y)
            dot = _rectangle.Rectangle(size=(grain_size, grain_size),
                            position=(x, y), colour=colour)
            dot.plot(self)
        if self._logging:
            _internals.active_exp._event_file_log(
                    "Stimulus,noise added,{0}, grain_size={1}, percentage={2}"\
                        .format(self.id, grain_size, percentage))
        return int((get_time() - start) * 1000)
