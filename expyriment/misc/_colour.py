"""Colour class.

This module contains a class implementing an RGB colour.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import colorsys

# The named colours are the 140 HTML colour names:
#    see https://www.w3schools.com/colors/colors_names.asp
# In addition, named colours including "gray" are also available in the
# British Enlgish spelling "grey".

_colours = {
    'aliceblue':                (240, 248, 255),
    'antiquewhite':             (250, 235, 215),
    'aqua':                     (0, 255, 255),
    'aquamarine':               (127, 255, 212),
    'azure':                    (240, 255, 255),
    'beige':                    (245, 245, 220),
    'bisque':                   (255, 228, 196),
    'black':                    (0, 0, 0),
    'blanchedalmond':           (255, 235, 205),
    'blue':                     (0, 0, 255),
    'blueviolet':               (138, 43, 226),
    'brown':                    (165, 42, 42),
    'burlywood':                (222, 184, 135),
    'cadetblue':                (95, 158, 160),
    'chartreuse':               (127, 255, 0),
    'chocolate':                (210, 105, 30),
    'coral':                    (255, 127, 80),
    'cornflowerblue':           (100, 149, 237),
    'cornsilk':                 (255, 248, 220),
    'crimson':                  (220, 20, 60),
    'cyan':                     (0, 255, 255),
    'darkblue':                 (0, 0, 139),
    'darkcyan':                 (0, 139, 139),
    'darkgoldenrod':            (184, 134, 11),
    'darkgray':                 (169, 169, 169),
    'darkgrey':                 (169, 169, 169),
    'darkgreen':                (0, 100, 0),
    'darkkhaki':                (189, 183, 107),
    'darkmagenta':              (139, 0, 139),
    'darkolivegreen':           (85, 107, 47),
    'darkorange':               (255, 140, 0),
    'darkorchid':               (153, 50, 204),
    'darkred':                  (139, 0, 0),
    'darksalmon':               (233, 150, 122),
    'darkseagreen':             (143, 188, 143),
    'darkslateblue':            (72, 61, 139),
    'darkslategray':            (47, 79, 79),
    'darkslategrey':            (47, 79, 79),
    'darkturquoise':            (0, 206, 209),
    'darkviolet':               (148, 0, 211),
    'deeppink':                 (255, 20, 147),
    'deepskyblue':              (0, 191, 255),
    'dimgray':                  (105, 105, 105),
    'dimgrey':                  (105, 105, 105),
    'dodgerblue':               (30, 144, 255),
    'firebrick':                (178, 34, 34),
    'floralwhite':              (255, 250, 240),
    'forestgreen':              (34, 139, 34),
    'fuchsia':                  (255, 0, 255),
    'gainsboro':                (220, 220, 220),
    'ghostwhite':               (248, 248, 255),
    'gold':                     (255, 215, 0),
    'goldenrod':                (218, 165, 32),
    'gray':                     (128, 128, 128),
    'grey':                     (128, 128, 128),
    'green':                    (0, 128, 0),
    'greenyellow':              (173, 255, 47),
    'honeydew':                 (240, 255, 240),
    'hotpink':                  (255, 105, 180),
    'indianred':                (205, 92, 92),
    'indigo':                   (75, 0, 130),
    'ivory':                    (255, 255, 240),
    'khaki':                    (240, 230, 140),
    'lavender':                 (230, 230, 250),
    'lavenderblush':            (255, 240, 245),
    'lawngreen':                (124, 252, 0),
    'lemonchiffon':             (255, 250, 205),
    'lightblue':                (173, 216, 230),
    'lightcoral':               (240, 128, 128),
    'lightcyan':                (224, 255, 255),
    'lightgoldenrodyellow':     (250, 250, 210),
    'lightgray':                (211, 211, 211),
    'lightgrey':                (211, 211, 211),
    'lightgreen':               (144, 238, 144),
    'lightpink':                (255, 182, 193),
    'lightsalmon':              (255, 160, 122),
    'lightseagreen':            (32, 178, 170),
    'lightskyblue':             (135, 206, 250),
    'lightslategray':           (119, 136, 153),
    'lightslategrey':           (119, 136, 153),
    'lightsteelblue':           (176, 196, 222),
    'lightyellow':              (255, 255, 224),
    'lime':                     (0, 255, 0),
    'limegreen':                (50, 205, 50),
    'linen':                    (250, 240, 230),
    'magenta':                  (255, 0, 255),
    'maroon':                   (128, 0, 0),
    'mediumaquamarine':         (102, 205, 170),
    'mediumblue':               (0, 0, 205),
    'mediumorchid':             (186, 85, 211),
    'mediumpurple':             (147, 112, 219),
    'mediumseagreen':           (60, 179, 113),
    'mediumslateblue':          (123, 104, 238),
    'mediumspringgreen':        (0, 250, 154),
    'mediumturquoise':          (72, 209, 204),
    'mediumvioletred':          (199, 21, 133),
    'midnightblue':             (25, 25, 112),
    'mintcream':                (245, 255, 250),
    'mistyrose':                (255, 228, 225),
    'moccasin':                 (255, 228, 181),
    'navajowhite':              (255, 222, 173),
    'navy':                     (0, 0, 128),
    'oldlace':                  (253, 245, 230),
    'olive':                    (128, 128, 0),
    'olivedrab':                (107, 142, 35),
    'orange':                   (255, 165, 0),
    'orangered':                (255, 69, 0),
    'orchid':                   (218, 112, 214),
    'palegoldenrod':            (238, 232, 170),
    'palegreen':                (152, 251, 152),
    'paleturquoise':            (175, 238, 238),
    'palevioletred':            (219, 112, 147),
    'papayawhip':               (255, 239, 213),
    'peachpuff':                (255, 218, 185),
    'peru':                     (205, 133, 63),
    'pink':                     (255, 192, 203),
    'plum':                     (221, 160, 221),
    'powderblue':               (176, 224, 230),
    'purple':                   (128, 0, 128),
    'red':                      (255, 0, 0),
    'rosybrown':                (188, 143, 143),
    'royalblue':                (65, 105, 225),
    'saddlebrown':              (139, 69, 19),
    'salmon':                   (250, 128, 114),
    'sandybrown':               (250, 164, 96),
    'seagreen':                 (46, 139, 87),
    'seashell':                 (255, 245, 238),
    'sienna':                   (160, 82, 45),
    'silver':                   (192, 192, 192),
    'skyblue':                  (135, 206, 235),
    'slateblue':                (106, 90, 205),
    'slategray':                (112, 128, 144),
    'slategrey':                (112, 128, 144),
    'snow':                     (255, 250, 250),
    'springgreen':              (0, 255, 127),
    'steelblue':                (70, 130, 180),
    'tan':                      (210, 180, 140),
    'teal':                     (0, 128, 128),
    'thistle':                  (216, 191, 216),
    'tomato':                   (255, 99, 71),
    'turquoise':                (64, 224, 208),
    'violet':                   (238, 130, 238),
    'wheat':                    (245, 222, 179),
    'white':                    (255, 255, 255),
    'whitesmoke':               (245, 245, 245),
    'yellow':                   (255, 255, 0),
    'yellowgreen':              (154, 205, 50),
}


class Colour:
    """Implements a class representing an RGB colour."""

    @staticmethod
    def get_colour_names():
        """Get a dictionary of all known colour names."""

        from collections import OrderedDict
        return OrderedDict(sorted(_colours.items(), key=lambda t: t[0]))

    @staticmethod
    def is_rgb(value):
        """Check for valid RGB tuple value.

        Parameters
        ----------
        value : iterable of length 3 (e.g. [255, 0, 0])
            the value to be checked

        Returns
        -------
        valid : bool
            whether the value is valid or not

        """

        if len(value) != 3:
            return False
        elif False in [isinstance(x, int) for x in value]:
            return False
        elif False in [0 <= x <= 255 for x in value]:
            return False
        else:
            return True

    @staticmethod
    def is_name(value):
        """Check for valid colour name value.

        Parameters
        ----------
        value : str (e.g. "red")
            the value to be checked

        Returns
        -------
        valid : bool
            whether the value is valid or not

        """

        if value not in _colours.keys():
            return False
        else:
            return True

    @staticmethod
    def is_hex(value):
        """Check for valid Hex triplet value.

        Parameters
        ----------
        value : string (e.g. "#FF0000")
            the value to be checked

        Returns
        -------
        valid : bool
            whether the value is valid or not

        """

        if not isinstance(value, str):
            return False

        value = value.lstrip("#")
        if len(value) != 6:
            return False
        else:
            for x in value.upper():
                if x not in "0123456789ABCDEF":
                    return False
        return True

    @staticmethod
    def is_hsv(value):
        """Check for valid HSV tuple value.

        Parameters
        ----------
        value : iterable of length 3 (e.g. [0, 100, 100])
            the value to be checked

        Returns
        -------
        valid : bool
            whether the value is valid or not

        """

        if len(value) != 3:
            return False
        elif False in [isinstance(x, int) for x in value]:
            return False
        elif not 0 <= value[0] <= 360:
            return False
        elif False in [0 <= x <= 100 for x in value[1:]]:
            return False
        else:
            return True

    @staticmethod
    def is_hsl(value):
        """Check for valid HSL tuple value.

        Parameters
        ----------
        value : iterable of length 3 (e.g. [0, 100, 50])
            the value to be checked

        Returns
        -------
        valid : bool
            whether the value is valid or not

        """

        return Colour.is_hsv(value)

    @staticmethod
    def is_colour(value):
        """Check for valid colour value.

        Parameters
        ----------
        value : any type
            the value to be checked

        Returns
        -------
        valid : bool
            whether the value is valid or not

        """

        return Colour.is_rgb(value) or\
            Colour.is_name(value) or \
            Colour.is_hex(value) or \
            Colour.is_hsv(value) or\
            Colour.is_hsl(value)

    def __init__(self, colour):
        """Create an RGB colour.

        Parameters
        ----------
        colour : list or tuple or str
            the colour to be created as either an RGB tuple (e.g.[255, 0, 0]),
            a Hex triplet (e.g. "#FF0000") or a colour name (e.g. "red").

        Notes
        -----
        All methods in Expyriment that have a colour parameter require RGB
        colours. This class also allows RGB colours to be defined via HSV/HSL
        values (hue [0-360], saturation [0-100], value/lightness [0-100]).To
        do so, use the hsv or hls property.

        """

        if Colour.is_rgb(colour):
            self.rgb = colour
        elif Colour.is_hex(colour):
            self.hex = colour
        elif Colour.is_name(colour):
            self.name = colour
        else:
            raise ValueError("'{}' is not a valid colour!".format(colour) + \
            "\nUse RGB tuple, Hex triplet or colour name.")

    def __str__(self):
        return "Colour(red={}, green={}, blue={})".format(self._rgb[0],
                                                             self._rgb[1],
                                                             self._rgb[2])

    def __eq__(self, other):
        return self._rgb == other._rgb

    def __ne__(self, other):
        return self._rgb != other._rgb

    def __getitem__(self, i):
        return self._rgb[i]

    def __len__(self):
        return len(self._rgb)

    @property
    def rgb(self):
        """Getter for colour in RGB format [red, green, blue]."""
        return self._rgb

    @rgb.setter
    def rgb(self, value):
        """Setter for colour in RGB format [red, green, blue]."""

        if Colour.is_rgb(value):
            self._rgb = tuple(value)
        else:
            raise ValueError("'{}' is not a valid RGB colour!".format(value))

    @property
    def hex(self):
        """Getter for colour in Hex format "#RRGGBB"."""

        return '#{:02X}{:02X}{:02X}'.format(self._rgb[0],
                                            self._rgb[1],
                                            self._rgb[2])
    @hex.setter
    def hex(self, value):
        """Setter for colour in Hex format "#RRGGBB"."""

        if Colour.is_hex(value):
            c = value.lstrip("#")
            self._rgb = tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
        else:
            raise ValueError("'{}' is not a valid Hex colour!".format(value))

    @property
    def name(self):
        """Getter for colour name (if available)."""

        for name, rgb in _colours.items():
            if rgb == self.rgb:
                return name
        return None

    @name.setter
    def name(self, value):
        """Setter for colour name."""

        if Colour.is_name(value):
            self._rgb = _colours[value.lower()]
        else:
            raise ValueError("'{}' is not a valid colour name!".format(value))

    @property
    def hsv(self):
        """Getter for colour in HSV format [hue, saturation, value]."""

        hsv = colorsys.rgb_to_hsv(*divide(self.rgb, 255.0))
        rtn = list(multiply([hsv[0]], 360))
        rtn.extend(multiply(hsv[1:], 100))
        return rtn

    @hsv.setter
    def hsv(self, value):
        """Setter for colour in HSV format [hue, saturation, value]."""

        if Colour.is_hsv(value):
            hsv = list(divide([value[0]], 360))
            hsv.extend(divide(value[1:], 100))
            self._rgb = multiply(colorsys.hsv_to_rgb(*hsv), 255)
        else:
            raise ValueError("'{}' is not a valid HSV colour!".format(value))

    @property
    def hsl(self):
        """Getter for colour in HSL format [hue, saturation, lightness]."""

        hsl = colorsys.rgb_to_hls(*divide(self.rgb, 255.0))
        rtn = list(multiply([hsl[0]], 360))
        rtn.extend(multiply(hsl[1:], 100))
        return rtn

    @hsl.setter
    def hsl(self, value):
        """Setter for colour in HSL format [hue, saturation, lightness]."""

        if Colour.is_hsv(value):
            hsl = list(divide([value[0]], 360))
            hsl.extend(divide(value[1:], 100))
            self._rgb = multiply(colorsys.hls_to_rgb(*hsl), 255)
        else:
            raise ValueError("'{}' is not a valid HSL colour!".format(value))


# Helper functions
def multiply(v, d):
    return tuple(map(lambda x:round(x*d), v))

def divide(v, d):
    return tuple(map(lambda x:x/float(d), v))
