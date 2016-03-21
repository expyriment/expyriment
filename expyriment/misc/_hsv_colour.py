"""
HSV Colour

This module contains a class implementing HSV colours [hue, saturation, value]

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

from colorsys import rgb_to_hsv, hsv_to_rgb

class HSVColour(object):
    """Class to handle HSV colours [hue, saturation, value]

    Note
    ----
    All methods in Expyriment that have a colour parameter require RGB
    colours. Use the property Colour.rgb. E.g.::

        my_colour = misc.HSVColour(hue=128, saturation=200, value = 128)
        stimuli.Circle(radius = 40, colour = my_colour.rgb).present()

    """

    def __init__(self, hue=0, saturation=0, value=0):
        """Initialize a HSV Colour.

        Parameters
        ----------
        hue : int (0-255), optional
            default = 0

        saturation : int (0-255), optional
            default = 0

        value : int (0-255), optional
            default = 0

        """

        self._rgb = None
        self.hsv = (hue, saturation, value)

    @property
    def hsv(self):
        """Getter for HSV value [hue, saturation, value]"""

        hsv = rgb_to_hsv(r = self._rgb[0], g = self._rgb[1],
                            b = self._rgb[2])
        return (hsv[0]*255.0, hsv[1]*255.0, hsv[2]*255.0)

    @hsv.setter
    def hsv(self, hsv_colour):
        """Setter for HSV value [hue, saturation, value]"""

        self._rgb = hsv_to_rgb(h = hsv_colour[0] / 255.0, s = hsv_colour[1] / 255.0,
                            v = hsv_colour[2] / 255.0)

    @property
    def rgb(self):
        """Getter for RGB value [red, green, blue]"""

        return (self._rgb[0]*255.0, self._rgb[1]*255.0, self._rgb[2]*255.0)

    @rgb.setter
    def rgb(self, rgb_colour):
        """Setter for RGB value [red, green, blue]"""

        self._rgb = (rgb_colour[0] / 255.0, rgb_colour[1] / 255.0,
                    rgb_colour[2] / 255.0)

    @property
    def hue(self):
        """Getter for hue"""

        return self.hsv[0]

    @property
    def saturation(self):
        """Getter for saturation"""

        return self.hsv[1]

    @property
    def value(self):
        """Getter for value"""

        return self.hsv[2]

    @hue.setter
    def hue(self, value):
        """Setter for hue"""

        hsv = self.hsv
        self.hsv = (value, hsv[1], hsv[2])

    @saturation.setter
    def saturation(self, value):
        """Setter for saturation"""

        hsv = self.hsv
        self.hsv = (hsv[0], value, hsv[2])

    @value.setter
    def value(self, value):
        """Setter for value"""

        hsv = self.hsv
        self.hsv = (hsv[0], hsv[1], value)

    def __str__(self):

        return "hsv={1}, rgb={0}".format(repr(self.rgb), repr(self.hsv))


if __name__ == "__main__":

    my_colour = HSVColour(hue=20, saturation=200, value = 128)
    print(my_colour)
