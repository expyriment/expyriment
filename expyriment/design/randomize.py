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
import _structure

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

def _compare_items(a, b):
    """Helper function for `shuffle_list` to compare two elements of a list"""
    if (isinstance(a, _structure.Trial) and isinstance(b, _structure.Trial)) or\
       (isinstance(a, _structure.Block) and isinstance(b, _structure.Block)):
        return a.compare(b)
    else:
        return a == b

def shuffle_list(list_, max_repetitions=None, n_segments=None):
    """Shuffle any list of objects. In place randomization of the list.

    Parameters
    ----------
    list_ : int
        list to shuffle
    max_repetitions : int, optional
        maximum number of allowed repetitions of one identical items; if no
        solution can be found (i.e., Python's recursion limit is reached), the
        function returns `False` and the list will be randomized without
        constrains (see Notes); default = None
    n_segments : int, optional
        randomize list per segment, i.e., list will be divided into n equal
        sized segments and the order of elements within each segment will be
        randomized; if n_segments is None or < 2, this parameter has no effect;
        default = None

    Returns
    -------
    success : bool
        returns if randomization was successful and fulfilled the specified
        constrains (see max_repetitions)

    Note
    ----
    When shuffling lists of trials or blocks, IDs and added stimuli will be
    ignored to determine repetitions, because trial or block comparisons are
    based on the `compare`method (see documentation of `Trial` or `Block`).

    """

    if n_segments > 1:
        l = 1 + (len(list_) - 1) / int(n_segments)
        for x in range(n_segments):
            t = (x + 1) * l
            if t > len(list_):
                t = len(list_)
            a = list_[l * x:t]
            _random.shuffle(a)
            list_[l * x:t] = a
    else:
        _random.shuffle(list_)

    if max_repetitions >= 0:
        # check constrains and remix
        reps = 0
        for i in range(len(list_)-1):
            if _compare_items(list_[i], list_[i+1]):
                reps += 1
                if reps > max_repetitions:
                    try:
                        return shuffle_list(list_=list_,
                                max_repetitions=max_repetitions,
                                n_segments=n_segments)
                    except: # maximum recursion depth reached
                        return False
            else:
                reps = 0
    return True


def make_multiplied_shuffled_list(list_, xtimes):
    """Return the multiplied and shuffled (sectionwise) list.

    The function manifolds the list 'x times' and shuffles each
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
