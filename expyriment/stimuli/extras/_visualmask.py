#!/usr/bin/env python

"""
A Visual Mask.

This module contains a class implementing a Visual Mask.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from random import shuffle
import tempfile
import os
from types import ModuleType

try:
    from PIL import Image, ImageDraw, ImageFilter #import PIL
except:
    Image = None

from ... import _internals, stimuli
from ...misc._timer import get_time
from ...stimuli._picture import Picture
from . import defaults


class VisualMask(Picture):
    """A class implementing a visual mask stimulus."""

    def __init__(self, size, position=None, dot_size=None,
                 background_colour=None, dot_colour=None,
                 dot_percentage=None, smoothing=None):
        """Create a visual mask.

        Parameters
        ----------
        size : (int, int)
            size (x, y) of the mask
        position   : (int, int), optional
            position of the mask stimulus
        dot_size : (int, int), optional
            size (x, y) of the dots
        background_colour : (int, int), optional
        dot_colour   : (int, int), optional
        dot_percentage : int, optional
            percentage of covered area by the dots (1 to 100)
        smoothing : int, optional
            smoothing (default=3)

        """

        if not isinstance(Image, ModuleType):
            message = """VisualMask can not be initialized.
The Python package 'Python Imaging Library (PIL)' is not installed."""
            raise ImportError(message)

        fid, filename = tempfile.mkstemp(
                    dir=stimuli.defaults.tempdir,
                    suffix=".png")
        os.close(fid)
        Picture.__init__(self, filename, position)

        self._size = size
        if dot_size is not None:
            self.dot_size = dot_size
        else:
            self.dot_size = defaults.visualmask_dot_size
        if background_colour is None:
            self.background_colour = defaults.visualmask_background_colour
        if background_colour is not None:
            self.background_colour = background_colour
        else:
            self.background_colour = _internals.active_exp.background_colour
        if dot_colour is None:
            self.dot_colour = defaults.visualmask_dot_colour
        if dot_colour is not None:
            self.dot_colour = dot_colour
        else:
            self.dot_colour = _internals.active_exp.foreground_colour
        if dot_percentage is not None:
            self.dot_percentage = dot_percentage
        else:
            self.dot_percentage = defaults.visualmask_dot_percentage
        if smoothing is not None:
            self.smoothing = smoothing
        else:
            self.smoothing = defaults.visualmask_smoothing

        self.create_mask()

    def create_mask(self):
        """Creates a new visual mask.

        Notes
        -----
        CAUTION: Depending on the size of the stimulus, this method may take
        some time to execute.

        Returns
        -------
        time  : int
            the time it took to execute this method in ms

        """

        start = get_time()
        was_preloaded = self.is_preloaded
        if was_preloaded:
            self.unload()

        s = (self._size[0] + 4 * self.smoothing,
             self._size[1] + 4 * self.smoothing) #somewhat larger mask 
        im = Image.new("RGB", s)
        draw = ImageDraw.Draw(im)
        draw.rectangle([(0, 0), s], outline=self.background_colour,
                       fill=self.background_colour)

        n_dots_x = int(s[0] / self.dot_size[0]) + 1
        n_dots_y = int(s[1] / self.dot_size[1]) + 1
        dots = list(range(n_dots_x * n_dots_y))
        shuffle(dots)
        for d in dots[:int(len(dots) * self.dot_percentage / 100)]:
            y = (d // n_dots_x) * self.dot_size[1]
            x = (d % n_dots_x) * self.dot_size[0]
            draw.rectangle([(x, y),
                            (x + self.dot_size[0], y + self.dot_size[1])],
                           outline=self.dot_colour, fill=self.dot_colour)

        for x in range(self.smoothing):
            im = im.filter(ImageFilter.BLUR).filter(ImageFilter.SMOOTH_MORE)

        #crop image and save
        c = (im.size[0] // 2, im.size[1] // 2)
        box = (c[0] - self._size[0] // 2, c[1] - self._size[1] // 2,
               c[0] + self._size[0] // 2, c[1] + self._size[1] // 2)
        im = im.crop(box)
        im.save(self._filename, format="png")

        if was_preloaded:
            self.preload()
        return int((get_time() - start) * 1000)


if __name__ == "__main__":
    from ... import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    mask = VisualMask(size=(200, 200))
    mask.present()
    print(mask.surface_size)
    exp.clock.wait(1000)
