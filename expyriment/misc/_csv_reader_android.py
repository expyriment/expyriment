"""An emulation of the csv.reader module.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


def reader(the_file):
    '''
    This is a 'dirty' emulation of the csv.reader module only used for 
    Expyriment loading designs under Android. The function reads in a csv file
    and returns a 2 dimensional array.
    
    Parameters
    ----------
    the_file: iterable
        The file to be parsed.
    
    Notes
    -----
    It is strongly suggested the use, if possible, the csv package from the 
    Python standard library.
   
    
    '''
    delimiter = ","
    rtn = []
    for row in the_file:
        rtn.append([strn.strip() for strn in row.split(delimiter)])
    return rtn

