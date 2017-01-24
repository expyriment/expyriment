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

import os
import sys
import glob
import random
import colorsys

import pygame

from .._internals import PYTHON3, android

try:
    from locale import getdefaultlocale
    LOCALE_ENC = getdefaultlocale()[1]
except ImportError:
    LOCALE_ENC = None  # Not available on Android

if LOCALE_ENC is None:
    LOCALE_ENC = 'utf-8'

FS_ENC = sys.getfilesystemencoding()
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

    if isinstance(standard_codes, (list, tuple)):
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

    # If font cache has to be (re-)created, initializing system fonts can take
    # a while. By running this in a seperate process, we can check if this is
    # the case and notify the user accordingly.
    def init_sysfonts_process():
        pygame.font.init()
        pygame.sysfont.initsysfonts()
    
    import multiprocessing
    p = multiprocessing.Process(target=init_sysfonts_process)
    p.start()
    p.join(1)  # wait one second
    if p.is_alive():  # if process still active, notify user
        m = "Initializing system fonts. This might take a couple of minutes..."
        print(m)
        p.join()
    pygame.font.init()

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

    if os.path.isfile(font):
        return font
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

    from .. import _internals
    if _internals.active_exp.is_initialized:
        return _internals.active_exp.screen.monitor_resolution
    else:
        pygame.display.init()
        return (pygame.display.Info().current_w,
                pygame.display.Info().current_h)


def is_ipython_running():
    """Return True if IPython is running."""

    try:
        __IPYTHON__
        return True
    except NameError:
        return False


def is_idle_running():
    """Return True if IDLE is running."""

    return "idlelib.run" in sys.modules


def is_interactive_mode():
    """Returns if Python is running in interactive mode (such as IDLE or
    IPthon)

    Returns
    -------
    interactive_mode : boolean
    
    """

    # ps2 is only defined in interactive mode
    return hasattr(sys, "ps2") or is_idle_running() or is_ipython_running()


def is_android_running():
    """Return True if Exypriment runs on Android."""

    return android is not None


def has_internet_connection():
    """Return True if computer is connected to internet."""
    try:
        socket.gethostbyname("google.com")
        return True
    except:
        return False


def create_colours(amount):
    """Create different and equally spaced RGB colours.
    
    Parameters
    ----------
    amount : int
        the number of colours to create
        
    Returns
    -------
    colours : list
        a list of colours, each in the form [r, g, b]
        
    """
    
    colours = []
    for i in range(0, 360, 360/amount):
        h = i / 360.0
        l = (50 + random.random() * 10) / 100
        s = (90 + random.random() * 10) / 100
        colours.append([int(x * 255) for x in colorsys.hls_to_rgb(h, l, s)])
    return colours
