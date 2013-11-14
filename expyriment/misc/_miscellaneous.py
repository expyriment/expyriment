"""
The miscellaneous module.

This module contains miscellaneous functions for expyriment.

All classes in this module should be called directly via expyriment.misc.*:

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


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
        if input_code == standard_codes: # accounts also for (bitwise) 0==0 & None==None 
            return True
        elif bitwise_comparison:
            return (input_code & standard_codes)
        else:
            return False

def _list_android_fonts():
    """List all truetype fonts in /system/fonts."""
    
    import glob
    import os
    
    d = {}
    for font in glob.glob("/system/fonts/*.ttf"):
        font = unicode(font)
        name = os.path.split(font)[1]
        name = name.lower()
        name = name.replace("-", "")
        name = name.replace("_", "")
        name = name.replace(".ttf", "")
        d[name] = font
    return d

def list_fonts():
    """List all fonts installed on the system.

    Returns a dictionary where the key is the font name and the value is the
    absolute path to the font file.

    """

    try:
        import android
    except ImportError:
        android = None

    if android is not None:
        d = _list_android_fonts()
    else:
        import pygame
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

    try:
        import android
    except ImportError:
        android = None

    if android is not None:
        fonts = _list_android_fonts()
        if font in fonts.keys():
            return fonts(font)
        else:
            return ""

    else:
        import pygame
        pygame.font.init()

        try:
            pygame.font.Font(font, 10)
            return font
        except:
            font_file = pygame.font.match_font(font)
            if font_file is not None:
                return font_file
            else:
                return ""
