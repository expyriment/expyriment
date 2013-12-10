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

import sys

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


def list_fonts():
    """List all fonts installed on the system.

    Returns a dictionary where the key is the font name and the value is the
    absolute path to the font file.

    """

    import pygame
    pygame.font.init()

    fonts = pygame.font.get_fonts()
    d = {}
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
            
def to_str(u, fse=False):

    """
    Converts an input str or unicode object to a str object without throwing
    an exception. If fse is False, the str is utf-8 encoded, otherwise it is
    encoded with the filesystemencoding. Str input objects are return unmodified.
    
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
    
    if isinstance(u, str):
        return u
        
    fs_enc = sys.getfilesystemencoding()
    if fs_enc == None:
        fs_enc = u'utf-8'
    if fse:
        s = u.encode(fs_enc)        
    else:
        s = u.encode(u'utf-8')
    return s

def to_unicode(s, fse=False):

    """
    Converts an input str or unicode object to a unicode object without throwing
    an exception. If fse is False, the first encoding that is tried is utf-8,
    falling back to the filesystem encoding if this throws an error. If fse is
    True, the filesystem encoding is tried, falling back to utf-8. Unicode
    input objects are return unmodified.
    
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
    
    if isinstance(s, unicode):
        return s
        
    fs_enc = sys.getfilesystemencoding()
    if fs_enc == None:
        fs_enc = u'utf-8'
    if fse:
        try:
            u = s.decode(fs_enc)
        except UnicodeDecodeError:
            u = s.decode(u'utf-8', u'ignore')
    else:
        try:
            u = s.decode(u'utf-8')
        except UnicodeDecodeError:
            u = s.decode(fs_enc, u'ignore')
    return u
