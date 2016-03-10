"""
The statistics module.

This module contains miscellaneous stastistical functions for expyriment.

"""
from __future__ import division


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


def sum(data):
    """Returns the sum of data.

    The function ignores all non-numerical elements in the data and returns
    None if no numerical element has been found. In contrast to standard math
    and numpy functions, this function is robust against type violations.

    Parameters
    ----------
    data : list
        list of numerical data

    Returns
    -------
    out : float or None

    """

    s = 0
    elem_found = False
    for v in data:
        try:
            s += v
            elem_found = True
        except:
            pass
    if elem_found:
        return s
    else:
        return None


def mode(data):
    """Returns the mode, that is, the most frequent value in data.

    Parameters
    ----------
    data : list
        list of numerical data

    Returns
    -------
    out : float or None

    """

    freq = frequence_table(data)
    Fmax = max(freq.values())
    for x, f in freq.items():
        if f == Fmax:
            break
    return x

def mean(data):
    """Returns the mean of data.

    Notes
    -----
    The function ignores all non-numerical elements in the data and returns
    None if no numerical element has been found. In contrast to standard math
    and numpy functions, this function is robust against type violations.

    Parameters
    ----------
    data : list
        list of numerical data

    Returns
    -------
    out : float or None

    """

    s = 0
    cnt = 0
    for v in data:
        try:
            s += v
            cnt += 1
        except:
            pass
    if cnt == 0:
        return None
    else:
        return float(s) / float(cnt)

def median(data):
    """Returns the median of data.

    Notes
    -----
    The function ignores all non-numerical elements in the data and returns
    None if no numerical element has been found. In contrast to standard math
    and numpy functions, this function is robust against type violations.

    Parameters
    ----------
    data : list
        list of numerical data

    Returns
    -------
    out : float or None

    """

    tmp = []
    for elem in data: # remove non numerics
        if isinstance(elem, (int, long, float)):
            tmp.append(elem)
    data = sorted(tmp)
    if len(data) % 2 == 1:
        return data[(len(data) - 1) // 2 ]
    else:
        lower = data[len(data) // 2 - 1]
        upper = data[len(data) // 2]
        return (float(lower + upper)) / 2.0

def frequence_table(data):
    """Returns the frequency table of the data as dictionary.

    Parameters
    ----------
    data : list
        list of numerical data

    Returns
    -------
    out : dict
        `dict.keys` : values, `dict.values` : frequencies


    """

    freq = {}
    for x in data:
        freq[x] = freq.get(x, 0) + 1
    return freq

