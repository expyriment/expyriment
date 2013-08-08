"""The expyriment randomize module.

This module contains various functions for randomizing data

"""

__author__ = 'Florian Krause <florian@expyriment.org>,\
              Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from copy import copy as _copy
import random as _random

_random.seed()


def rand_int_sequence(first_elem, last_elem):
    """Return a randomised sequence of integers in given range.

    Parameters
    ----------
    first_elem : int
        first element of the range
    last_elem : int
        last element of the range

    Results
    -------
    rnd_seq : list
        randomised sequence of integers in given range

    """

    list_ = range(first_elem, last_elem + 1)
    _random.shuffle(list_)
    return list_


def rand_int(a, b):
    """Return random integer in given range.

    Parameters
    ----------
    a : int
        first element of range
    b : int
        last element of range

    Results
    -------
    rnd : int

    """

    return _random.randint(a, b)

def rand_element(list_):
    """Return a random element from a list

    Parameter
    ---------
    list_ : list

    Results
    -------
    elem : a random element from the list

    """

    return list_[_random.randint(0, len(list_) - 1)]

def coin_flip():
    """Return randomly True or False.
    Returns
    -------
    rnd : bool

    """

    if _random.randint(1, 2) == 1:
        return True
    else:
        return False


def shuffle_list(list_):
    """Shuffle any list of objects.

    Parameters
    ----------
    list_ : int
        list to shuffle

    """

    _random.shuffle(list_)


def make_multiplied_shuffled_list(list_, xtimes):
    """Return the multiplied and shuffled (sectionwise) list.

    The function manifolds the list 'xtimes' and shuffles each
    and concatenates to the return new lists.

    Parameters
    ----------
    list_ : list
        list to be shuffled
    xtimes : int
        how often the list will be multiplied

    """

    newlist = []
    tmp = _copy(list_)
    for _i in range(0, xtimes):
        _random.shuffle(tmp)
        newlist.extend(tmp)
    return newlist
