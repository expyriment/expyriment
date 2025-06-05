"""
The permute module.

This module implements permutation of blocks, trials and conditions.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

from ...misc.constants import P_RANDOM, P_CYCLED_LATIN_SQUARE, P_BALANCED_LATIN_SQUARE
from ..randomize import rand_int_sequence


def _empty_rect(n_rows, n_columns):
    rtn = []
    for _ in range(n_rows):
        rtn.append([None] * n_columns)
    return rtn


def _square_of_elements(list_, idx_square):
    """Return a square array of elements.

    Returns
    -------
    square : list
        a square array with the elements from the list defined by
        idx_square e.g.; idx_square[a][b] is the list index of element[a][b].

    """

    square = []
    for idx_row in idx_square:
        square.append([list_[i] for i in idx_row])
    return square


def is_permutation_type(type_str):
    """Return true if the string or value is a know permutation type.

    Parameters
    ----------
    type_str : string
        permutation type string

    """

    return type_str in (P_RANDOM, P_CYCLED_LATIN_SQUARE, P_BALANCED_LATIN_SQUARE)


def _cycle_list(arr):
    rtn = arr[1:]
    rtn.append(arr[0])
    return rtn


def _balanced_latin_square_sequence(n_elements, row):
    """helper function: creates a sequence for a balanced latin square

    Based on "Bradley, J. V. Complete counterbalancing of immediate sequential effects in a Latin square design. J. Amer. Statist. Ass.,.1958, 53, 525-528. "
    """

    result = []
    j = 0
    h = 0

    for i in range(n_elements):
        if i < 2 or i % 2 != 0:
            val = j
            j += 1
        else:
            val = n_elements - h - 1
            h += 1

        result.append((val + row) % n_elements)

    if n_elements % 2 != 0 and row % 2 != 0:
        return list(reversed(result))
    else:
        return result


def latin_square(elements, permutation_type=P_RANDOM):
    """A latin square permutation of elements.

    If elements is a integer the elements=[0,..., elements] is used.

    Parameters
    ----------
    elements : int or list
        list of elements or a number
    permutation_type : str (default='random')
        type of permutation (permutation type); 'random', 'cycled' or 'balanced'
        permutation types defined in misc.constants and design.permute:
        P_BALANCED_LATIN_SQUARE, P_CYCLED_LATIN_SQUARE and P_RANDOM

    Returns
    -------
    permutations : list of list

    Notes
    -----
    see "Bradley, J. V. Complete counterbalancing of immediate sequential effects in a Latin square design. J. Amer. Statist. Ass.,.1958, 53, 525-528. "

    """

    if not is_permutation_type(permutation_type):
        raise AttributeError("'{0}' is an unknown permutation type".format(permutation_type))

    assert isinstance(elements, (list, tuple, int))

    if isinstance(elements, int):
        n = elements
    else:
        n = len(elements)

    if permutation_type == P_CYCLED_LATIN_SQUARE:
        # cycled square
        # Make n cycled columns [0,1,2,...n-1][1,2,3,...n-1,0][...]
        square = [list(range(0, n))]
        for r in range(0, n - 1):
            square.append(_cycle_list(square[r]))

    elif permutation_type == P_BALANCED_LATIN_SQUARE:
        # balanced square
        if n%2 == 0:
            rows = range(n)
        else:
            rows = range(n*2)

        square = [_balanced_latin_square_sequence(n, x) for x in rows]

    else:
        # random
        columns = latin_square(n, permutation_type=P_CYCLED_LATIN_SQUARE)

        # Make index list to sort columns [0,1,n-1,3,n-2,4,...]
        c_idx = [0, 1]
        take_last = True
        tmp = list(range(2, n))
        for _i in range(2, n):
            if take_last:
                c_idx.append(tmp.pop())
            else:
                c_idx.append(tmp.pop(0))
            take_last = not take_last

        # Write sorted columns to square
        square = _empty_rect(n, n)
        for c in range(n):
            for r in range(n):
                square[r][c] = columns[c_idx[c]][r]

        # randomize counter elements
        square = _square_of_elements(rand_int_sequence(0, n - 1), idx_square=square)

    if isinstance(elements, int):
        return square
    else:
        return _square_of_elements(elements, square)


def balanced_latin_square(elements):
    """"OBSOLETE METHOD: Please use 'latin_square'."""
    # TODO: make deprecated with 1.0

    return latin_square(elements, permutation_type=P_BALANCED_LATIN_SQUARE)


def cycled_latin_square(elements):
    """"OBSOLETE METHOD: Please use 'latin_square'."""
    # TODO: make deprecated with 1.0

    return latin_square(elements, permutation_type=P_CYCLED_LATIN_SQUARE)

