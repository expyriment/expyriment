"""The expyriment randomize module.

This module contains various functions for randomizing data

"""

__author__ = 'Florian Krause <florian@expyriment.org>,\
              Oliver Lindemann <oliver@expyriment.org>'


import random as _random
from copy import copy as _copy

_random.seed()


def rand_int_sequence(first_elem, last_elem):
    """Return a randomised sequence of integers in given range.

    Parameters
    ----------
    first_elem : int
        first element of the range
    last_elem : int
        last element of the range

    Returns
    -------
    rnd_seq : list
        randomised sequence of integers in given range

    """

    list_ = list(range(first_elem, last_elem + 1))
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

    Returns
    -------
    rnd : int

    """

    return _random.randint(a, b)


def rand_element(list_):
    """Return a random element from a list

    Parameters
    ----------
    list_ : list

    Returns
    -------
    elem : a random element from the list

    """

    list_ = list(list_)
    return list_[_random.randint(0, len(list_) - 1)]


def coin_flip(head_bias=0.5):
    """Return randomly True (head) or False (tail).

    Parameters
    ----------
    head_bias : numeric, optional
        bias in favor of head (default=0.5, fair coin)

    Returns
    -------
    rnd : bool

    """

    if head_bias < 0 or head_bias > 1:
        raise RuntimeError("Head bias must be between 0 and 1!")

    return _random.random() <= head_bias


def rand_norm(a, b, mu=None, sigma=None):
    """Normally distributed random number in given range.

    Parameters
    ----------
    a : numeric
        lowest number in range
    b : numeric
        highest number in range
    mu : numeric, optional
        distribution mean, default: mid point of the interval [a, b]
    sigma : numeric, optional
        distribution standard deviation, default: (b-a)/6.0

    Returns
    -------
    rnd : numeric

    """

    if mu is None:
        mu = a + (b-a) / 2.0
    if sigma is None:
        sigma = (b-a) / 6.0

    r = _random.normalvariate(mu=mu, sigma=sigma)
    if r < a or r > b:
        return rand_norm(a=a, b=b)

    return r


def _compare_items(a, b):
    """Helper function for `shuffle_list` to compare two elements of a list"""
    from .._structure import (  # needs to be imported here because of circular dependency
        Block,
        Trial,
    )
    if (isinstance(a, Trial) and isinstance(b, Trial)) or\
       (isinstance(a, Block) and isinstance(b, Block)):
        return a.compare(b)
    else:
        return a == b


def shuffle_list(list_, max_repetitions=-1, n_segments=0):
    """Shuffle any list of objects. In place randomization of the list.

    Parameters
    ----------
    list_ : list
        the list to shuffle; if not a list, TypeError is raised
    max_repetitions : int, optional
        maximum number of allowed repetitions of one identical items; if no
        solution can be found (i.e., Python's recursion limit is reached), the
        function returns `False` and the list will be randomized without
        constrains (see Notes); default = -1
    n_segments : int, optional
        randomize list per segment, i.e., list will be divided into n equal
        sized segments and the order of elements within each segment will be
        randomized; if n_segments is < 2, this parameter has no effect;
        default = 0

    Returns
    -------
    success : bool
        returns if randomization was successful and fulfilled the specified
        constrains (see max_repetitions)

    Notes
    -----
    When shuffling lists of trials or blocks, IDs and added stimuli will be
    ignored to determine repetitions, because trial or block comparisons are
    based on the `compare`method (see documentation of `Trial` or `Block`).

    """

    if not isinstance(list_, list):
        raise TypeError("The parameter 'list_' is a {0}, but has to be list. ".format(type(list_).__name__))

    if n_segments is None:
        n_segments = 0
    if max_repetitions is None:
        max_repetitions = -1

    if n_segments > 1:
        l = 1 + (len(list_) - 1) // int(n_segments)
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
                    except Exception:  # maximum recursion depth reached
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
        how often the list will be multiplied. If xtimes==0, an
        empty list will be returned.

    """

    newlist = []
    tmp = _copy(list(list_))
    for _i in range(0, xtimes):
        _random.shuffle(tmp)
        newlist.extend(tmp)
    return newlist

