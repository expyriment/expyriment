"""The design package.

This package provides several data structures for describing the design of an
experiment.  See also expyriment.design.extras for more design.

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
              Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from . import defaults
from . import permute
from . import randomize
from ._structure import Experiment, Block, Trial

from .. import _internals
_internals.active_exp = Experiment("None")

