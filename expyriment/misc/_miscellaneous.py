"""
The miscellaneous module.

This module contains miscellaneous functions for expyriment.

All classes in this module should be called directly via expyriment.misc.*:

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

from sys import getfilesystemencoding
import os
import glob
import pygame
from .. import PYTHON3

try:
    from locale import getdefaultlocale
    LOCALE_ENC = getdefaultlocale()[1]
except ImportError:
    LOCALE_ENC = None  # Not available on Android

if LOCALE_ENC is None:
    LOCALE_ENC = 'utf-8'

FS_ENC = getfilesystemencoding()
if FS_ENC is None:
    FS_ENC = 'utf-8'


def compare_codes(input_code, standard_codes, bitwise_comparison=True):
    """Helper function to compare input_code with a standard codes.

    Returns a boolean and operates by default bitwise.

    Parameters
    ----------
    input_code : int
        code or bitpattern
    standard_codes : int or list
        code/bitpattern or list of codes/bitpattern
    bitwise_comparison : bool, optional
        (default = True)

    """

    if type(standard_codes) is list:
        for code in standard_codes:
            if compare_codes(input_code, code, bitwise_comparison):
                return True
        return False
    else:
        if input_code == standard_codes:  # accounts also for (bitwise) 0==0 &
                                          # None==None
            return True
        elif bitwise_comparison:
            return (input_code & standard_codes)
        else:
            return False


def byte2unicode(s, fse=False):
    if (PYTHON3 and isinstance(s, str)) or\
       (not PYTHON3 and isinstance(s, unicode)):
        return s

    if fse:
        try:
            u = s.decode(FS_ENC)
        except UnicodeDecodeError:
            u = s.decode('utf-8', 'replace')
    else:
        try:
            u = s.decode(LOCALE_ENC)
        except UnicodeDecodeError:
            u = s.decode('utf-8', 'replace')
    return u


def unicode2byte(u, fse=False):
    if isinstance(u, bytes):
        return u

    if fse:
        try:
            s = u.encode(FS_ENC)
        except UnicodeEncodeError:
            s = u.encode('utf-8', 'replace')
    else:
        try:
            s = u.encode(LOCALE_ENC)
        except UnicodeEncodeError:
            s = u.encode('utf-8', 'replace')
    return s


def str2unicode(s, fse=False):
    """Convert str to unicode.

    Converts an input str or unicode object to a unicode object without
    throwing an exception. If fse is False, the first encoding that is tried is
    the encoding according to the locale settings, falling back to utf-8
    encoding if this throws an error. If fse is True, the filesystem encoding
    is tried, falling back to utf-8. Unicode input objects are returned
    unmodified.

    Parameters
    ----------
    s : str or unicode
        input text
    fse : bool
        indicates whether the filesystem encoding should be tried first.
        (default = False)

    Returns
    -------
    A unicode-type string.
    """
    return byte2unicode(s, fse)

def unicode2str(u, fse=False):
    """Convert unicode to str.

    Converts an input str or unicode object to a str object without throwing
    an exception. If fse is False, the str is encoded according to the locale
    (with utf-8 as a fallback), otherwise it is encoded with the
    filesystemencoding. Str input objects are returned unmodified.

    Parameters
    ----------
    u : str or unicode
    input text
    fse : bool
    indicates whether the filesystem encoding should used.
    (default = False)

    Returns
    -------
    A str-type string.
    """

    return unicode2byte(u, fse)

def numpad_digit_code2ascii(keycode):
    """Convert numpad keycode to the ascii code of that particular number

    If it is not a keypad digit code, no convertion takes place and the
    same code will be returned.

    Returns
    -------
    ascii_code : int

    """

    from ..misc import constants
    if keycode in constants.K_ALL_KEYPAD_DIGITS:
        return keycode - (constants.K_KP1 - constants.K_1)
    else:
        return keycode

def add_fonts(folder):
    """Add fonts to Expyriment.

    All truetype fonts found in the given folder will be added to
    Expyriment, such that they are found when only giving their name
    (i.e. without the full path).

    Parameters
    ----------
    folder : str or unicode
        the full path to the folder to search for

    """

    pygame.font.init()
    pygame.sysfont.initsysfonts()

    for font in glob.glob(os.path.join(folder, "*")):
        if font[-4:].lower() in ['.ttf', '.ttc']:
            font = byte2unicode(font, fse=True)
            name = os.path.split(font)[1]
            bold = name.find('Bold') >= 0
            italic = name.find('Italic') >= 0
            oblique = name.find('Oblique') >= 0
            name = name.replace(".ttf", "")
            if name.endswith("Regular"):
                name = name.replace("Regular", "")
            if name.endswith("Bold"):
                name = name.replace("Bold", "")
            if name.endswith("Italic"):
                name = name.replace("Italic", "")
            if name.endswith("Oblique"):
                name = name.replace("Oblique", "")
            name = ''.join([c.lower() for c in name if c.isalnum()])
            pygame.sysfont._addfont(name, bold, italic or oblique, font,
                                    pygame.sysfont.Sysfonts)


def list_fonts():
    """List all fonts installed on the system.

    Returns a dictionary where the key is the font name and the value is the
    absolute path to the font file.

    """

    pygame.font.init()

    d = {}
    fonts = pygame.font.get_fonts()
    for font in fonts:
        d[font] = pygame.font.match_font(font)
    return d


def find_font(font):
    """Find an installed font given a font name.

    This will try to match a font installed on the system that is similar to
    the given font name.

    Parameters
    ----------
    font : str
        name of the font

    Returns
    -------
    font : str
        the font that is most similar
        If no font is found, an empty string will be returned.

    """

    pygame.font.init()

    try:
        if os.path.isfile(font):
            pygame.font.Font(unicode2byte(font, fse=True), 10)
        else:
            pygame.font.Font(unicode2byte(font), 10)
        return font
    except:
        font_file = pygame.font.match_font(font)
        if font_file is not None:
            return font_file
        else:
            return ""

def get_monitor_resolution():
    """Returns the monitor resolution

    Returns
    -------
    resolution: (int, int)
        monitor resolution, screen resolution

    """

    from .. import _globals
    if _globals.active_exp.is_initialized:
        return _globals.active_exp.screen.monitor_resolution
    else:
        pygame.display.init()
        return (pygame.display.Info().current_w,
                pygame.display.Info().current_h)
