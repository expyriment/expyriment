"""An emulation of the csv.reader module.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

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
    return [
        [strn.strip() for strn in row.split(delimiter)]
        for row in the_file
    ]
