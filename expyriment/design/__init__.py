"""The design package.

This package provides several data structures for describing the design of an
experiment.  See also expyriment.design.extras for more design.

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
              Oliver Lindemann <oliver@expyriment.org>'


from .. import _internals

# randomize is DEPRECATED Use randomise.
from . import defaults, permute, randomise
from . import randomise as randomize
from ._structure import Block, Experiment, Trial

_internals.active_exp = Experiment("None")

