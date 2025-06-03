"""
The miscellaneous module.

This module contains miscellaneous functions for expyriment.

All classes in this module should be called directly via expyriment.misc.*:

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import os
import sys
import glob
import random
import colorsys
import math

import pygame
try:
    import pygame._sdl2.audio as sdl2_audio
except ImportError:
    sdl2_audio = None

from .._internals import active_exp, get_settings_folder, get_version

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


class MediaTime(float):
    """A class representing time as used in the context of media playback.

    Internally represents time in seconds as a float value (inherits from
    built-in float type), but can deal with multiple formats when creating and
    comparing time.

    Parameters
    ----------
    time : int, float, tuple, list or str
        the time to represent; can be any of the following formats:
            - float: seconds
            - tuple: (minutes, seconds) or (hours, minutes, seconds)
            - list: [minutes, seconds] or [hours, minutes, seconds]
            - str: 'hh:mm:ss', 'hh:mm:ss.sss', or 'mm:ss.sss'

    Examples
    --------
    >>> MediaTime(15.4)                # seconds
    >>> MediaTime((1, 21.5))           # (min, sec)
    >>> MediaTime((1, 1, 2))           # (hr, min, sec)
    >>> MediaTime('01:01:33.5')        # (hr:min:sec)
    >>> MediaTime('01:01:33.045')
    >>> MediaTime('01:01:33,5')        # comma works too 
    >>> MediaTime(3600) == '01:00:00'  # True

    """

    @staticmethod
    def convert_to_seconds(time):
        """Try to convert time specified in common media formats into seconds.

        Parameters
        ----------
        time : int, float, tuple, list or str
            the time to convert; can be any of the following formats:
                - float: seconds
                - tuple: (minutes, seconds) or (hours, minutes, seconds)
                - list: [minutes, seconds] or [hours, minutes, seconds]
                - str: 'hhrmm:ss', 'hh:mm:ss.sss', or 'mm:ss.sss'

        Returns
        -------
        float
            The media time in seconds.

        Examples
        --------
        >>> convert_to_seconds(15.4)          # seconds
        15.4
        >>> convert_to_seconds((1, 21.5))     # (min, sec)
        81.5
        >>> convert_to_seconds((1, 1, 2))     # (hr, min, sec)
        3662
        >>> convert_to_seconds('01:01:33.5')  # (hr:min:sec)
        3693.5
        >>> convert_to_seconds('01:01:33.045')
        3693.045
        >>> convert_to_seconds('01:01:33,5')  # comma works too
        3693.5

        """

        # The following code has been adapted from MoviePy
        # (https://zulko.github.io/moviepy/)

        factors = (1, 60, 3600)

        if isinstance(time, str):
            time = [float(part.replace(",", ".")) for part in time.split(":")]

        if not isinstance(time, (tuple, list)):
            return time  # Return as is, if not a valid format

        return sum(mult * part for mult, part in zip(factors, reversed(time)))

        # End of code from MoviePy

    def __new__(cls, time):
        seconds = cls.convert_to_seconds(time)  # Use the static method
        return super().__new__(cls, seconds)

    def __lt__(self, other):
        return float(self) < self.convert_to_seconds(other)

    def __le__(self, other):
        return float(self) <= self.convert_to_seconds(other)

    def __eq__(self, other):
        return float(self) == self.convert_to_seconds(other)

    def __gt__(self, other):
        return float(self) > self.convert_to_seconds(other)

    def __ge__(self, other):
        return float(self) >= self.convert_to_seconds(other)


def round(number, ndigits=0): # TODO: overrides Python's round, maybe renaming?
    """Round half away from zero.

    This method implements the Python 2 way of rounding.
    For "bankers rounding" (round half to even), please use the builtin `round`
    function in Python 3 or Numpy's `around` function.

    Parameters
    ----------
    number : int or float
        the number to be rounded
    ndigits : int
        the number of digits to round to (default = 0)

    Returns
    -------
    rounded_number : float
        the rounded number

    """

    p = 10 ** ndigits
    if number > 0:
        return float(math.floor((number * p) + 0.5))/p
    else:
        return float(math.ceil((number * p) - 0.5))/p


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
    if isinstance(s, str):
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

    If it is not a keypad digit code, no conversion takes place and the
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
    # a while. By having a watchdog thread, we can check if this is the case
    # and notify the user accordingly.

    import time
    import threading

    def watchdog_timer(state):
        time.sleep(1)
        if not state['completed']:
            m = "Initializing system fonts. This might take a couple of minutes..."
            sys.stdout.write(m + '\n')

    state = {'completed': False}
    watchdog = threading.Thread(target=watchdog_timer, args=(state,))
    watchdog.daemon = True
    watchdog.start()
    pygame.font.init()
    pygame.sysfont.initsysfonts()
    state['completed'] = True

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
        warn_message = "Failed to find font {0}!".format(font)
        print("Warning: " + warn_message)
        return ""


def get_display_info():
    """Return information about the available display(s).

    Return
    ------
    info : dict of dicts
        the information for each available display in the form
             "maximal_resolution": ...,  # highest possible or "native", tuple
             "desktop_resolution": ...}  # might differ (e.g. scaled), tuple

    """

    pygame.display.init()
    info = {}
    for x in range(pygame.display.get_num_displays()):
        info[x] = {
             "maximal_resolution": pygame.display.list_modes(display=x)[0],
             "desktop_resolution": pygame.display.get_desktop_sizes()[x]}

    return info


def get_monitor_resolution():
    """Returns the monitor resolution

    DEPRECATED! Use get_display_info instead.

    Returns
    -------
    resolution: (int, int)
        monitor resolution, screen resolution

    """

    pygame.display.init()
    if active_exp.is_initialized:
        return active_exp.screen.display_resolution
    else:
        return get_display_info[0]["maximal_resolution"]


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
    """Return if Python is running in interactive mode (such as IDLE or
    IPthon)

    Returns
    -------
    interactive_mode : boolean

    """

    # ps2 is only defined in interactive mode
    return hasattr(sys, "ps2") or is_idle_running() or is_ipython_running()


def is_android_running():
    """Return True if Exypriment runs on Android."""

    return hasattr(sys, "getandroidapilevel")


def has_internet_connection():
    """Return True if computer is connected to internet."""
    try:
        import socket
        host = socket.gethostbyname("google.com")
        socket.create_connection((host, 80), 2)
        return True
    except Exception:
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
    for i in range(0, 360, 360//amount):
        h = i / 360.0
        l = (50 + random.random() * 10) / 100
        s = (90 + random.random() * 10) / 100
        colours.append([int(x * 255) for x in colorsys.hls_to_rgb(h, l, s)])
    return colours


def which(programme):
    """Locate a programme file in the user's path.

    This mimics behaviour of UNIX's 'which' command.

    Parameters
    ----------
    programme : str
        the programme to file to locate

    Returns
    -------
    path : str or None
        the full path to the programme file or None if not found

    """

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(programme)
    if fpath:
        if is_exe(programme):
            return programme
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, programme)
            if is_exe(exe_file):
                return exe_file

    return None


def download_from_stash(content="all", branch=None):
    """Download content from the Expyriment stash.

    Content will be stored in an Expyriment settings directory (`.expyriment`
    or `~expyriment`, located in the current user's home directory).

    Parameters
    ----------
    content : str, optional
        the content to install ("examples", "extras", "tools", or "all")
        (default="all")
    branch : str, optional
        a specific branch to get the content from (if not set, the branch
        corresponding to the current Expyriment release is used)
        (default=None)

    """

    def show_progress(count, total, status=''):
        bar_len = 40
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + ' ' * (bar_len - filled_len)
        sys.stdout.write('{:5.1f}% [{}] {}\r'.format(percents, bar, status))
        sys.stdout.flush()

    from urllib.request import urlopen, Request
    from tempfile import TemporaryFile
    from zipfile import ZipFile
    from shutil import copyfileobj

    if branch is None:
        branch = get_version().split(" ")[0]
    url = "https://github.com/expyriment/expyriment-stash/archive/{0}.zip"
    url = url.format(branch)
    try:
        r = Request(url, headers={"Accept-Encoding": "gzip; deflate"})
        u = urlopen(r)
    except Exception:
        raise RuntimeError("Download of {0} failed!".format(url))

    with TemporaryFile() as f:
        try:
            file_size = int(u.getheader('Content-Length'))
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
                show_progress(file_size_dl, file_size,
                              "downloading stash ({0})".format(branch))
            sys.stdout.write("\n")
        except Exception:
            show_progress(0, 100,
                          "downloading stash ({0})".format(branch))
            chunk = u.read()
            while chunk:
                f.write(chunk)
                chunk = u.read()
            show_progress(100, 100,
                          "downloading stash ({0})".format(branch))

        if not os.path.isdir(get_settings_folder()):
            os.makedirs(get_settings_folder())
        path = get_settings_folder()

        f_zip = ZipFile(f)
        check = f_zip.testzip()
        if check is not None:
            raise RuntimeError("Download was corrupted!")
        if content == "all":
            content_ = ("examples", "extras", "tools")
        else:
            content_ = content
        if type(content_) not in (list, tuple):
            content_ = (content_,)
        files = []
        root = f_zip.namelist()[0]
        for c in content_:
            mask = os.path.join(root, c)
            files.extend([x for x in f_zip.namelist() if x.startswith(mask)])
        files_installed = 0
        for member in files:
            filename = os.path.basename(member)
            if not filename:
                try:
                    os.mkdir(os.path.join(path, os.path.relpath(member, root)))
                except Exception:
                    pass
                files_installed += 1
                continue
            source = f_zip.open(member)
            target = open(os.path.join(path, os.path.relpath(member, root)),
                          'wb')
            with source, target:
                copyfileobj(source, target)
            files_installed += 1
            show_progress(files_installed, len(files),
                          "installing content ({0})".format(content))
    print("")


def string_sort_array(array):
    """Sorts an array with different types using the string representation.
    Sorts in place!

    Returns
    -------
    array : list
        the sorted array

    """

    array.sort(key=_sorter_fnc)
    return array

def _sorter_fnc(x):
    """sorter function for py_sort"""
    if x is None:
        return ""
    else:
        return str(x)

def get_audio_devices(input_devices=False):
    """Get the names of available audio devices.

    Parameters
    ----------
    input_devices : bool, optional
        return input (instead of output) device names (default=False)

    Returns
    -------
    audio_devices : list
        a list of audio device names

    """

    if sdl2_audio is None:
        return

    is_initialized = pygame.mixer.get_init()
    if not is_initialized:
        pygame.mixer.init()

    audio_devices = sdl2_audio.get_audio_device_names(input_devices)

    if not is_initialized:
        pygame.mixer.quit()

    return audio_devices
