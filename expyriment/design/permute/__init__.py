"""
The permute module.

This module implements permutation of blocks, trials and conditions.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from ._permute import (
                       P_BALANCED_LATIN_SQUARE,
                       P_CYCLED_LATIN_SQUARE,
                       P_RANDOM,
                       is_permutation_type,
                       latin_square,
)
