"""The expyriment randomise module.

This module contains various functions for randomizing data

"""

__author__ = 'Florian Krause <florian@expyriment.org>,\
              Oliver Lindemann <oliver@expyriment.org>'


from ._randomise import (
                         coin_flip,
                         make_multiplied_shuffled_list,
                         rand_element,
                         rand_int,
                         rand_int_sequence,
                         rand_norm,
                         shuffle_list,
)
