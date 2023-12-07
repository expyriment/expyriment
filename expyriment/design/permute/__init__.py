"""
The permute module.

This module implements permutation of blocks, trials and conditions.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from ._permute import is_permutation_type, P_RANDOM, P_CYCLED_LATIN_SQUARE, P_BALANCED_LATIN_SQUARE
from ._permute import balanced_latin_square, cycled_latin_square, latin_square
