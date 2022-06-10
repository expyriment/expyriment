"""
The permute module.

This module implements permutation of blocks, trials and conditions.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

from ...misc.constants import P_RANDOM, P_CYCLED_LATIN_SQUARE, P_BALANCED_LATIN_SQUARE

def _empty_square(n):
    square = []
    for x in range(0, n):
        square.append([])
        for _i in range(0, n):
            square[x].append(None)
    return square


def _square_of_elements(list_, idx_square):
    """Return a square array of elements.

    Returns
    -------
    square : list
        a square array with the elements from the list defined by
        idx_square e.g.; idx_square[a][b] is the list index of element[a][b].

    """

    square = _empty_square(len(list_))
    for c in range(0, len(list_)):
        for r in range(0, len(list_)):
            square[r][c] = list_[idx_square[r][c]]
    return square


def is_permutation_type(type_str):
    """Return true if the string or value is a know permutation type.

    Parameters
    ----------
    type_str : string
        permutation type string

    """

    return type_str == P_RANDOM or type_str == P_CYCLED_LATIN_SQUARE or type_str == P_BALANCED_LATIN_SQUARE


def _cycle_list(arr):
    rtn = arr[1:]
    rtn.append(arr[0])
    return rtn


def balanced_latin_square(elements):
    """A balanced latin square permutation of elements.

    If elements is an integer the elements=[0,..., elements] is used.

    Parameters
    ----------
    elements : int or list
        list of elements or a number

    """

    if isinstance(elements, (tuple, list)):
        idx = balanced_latin_square(len(elements))
        square = _square_of_elements(elements, idx)
    else:
        n = elements
        # Make n cycled columns [0,1,2,...n-1][1,2,3,...n-1,0][...]
        columns = cycled_latin_square(n)

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
        square = _empty_square(n)
        for c in range(0, n):
            for r in range(0, n):
                square[r][c] = columns[c_idx[c]][r]

    return square


def cycled_latin_square(elements):
    """"OBSOLETE METHOD: Please use 'latin_square'."""
    # TODO: make deprecated with 1.0

    return latin_square(elements, permutation_type=P_CYCLED_LATIN_SQUARE)


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
        P_BALANCED_LATIN_SQUARE, P_CYCLED_LATIN_SQUARE, and P_RANDOM



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

        return "TODO"

    else:
        # random
        # Make n cycled columns [0,1,2,...n-1][1,2,3,...n-1,0][...]
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
        square = _empty_square(n)
        for c in range(0, n):
            for r in range(0, n):
                square[r][c] = columns[c_idx[c]][r]

    if isinstance(elements, int):
        return square
    else:
        return _square_of_elements(elements, square)


