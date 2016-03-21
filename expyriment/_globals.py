"""
Model with the system width global variable:
        active_exp

import ._globals to read and write _globals.active_exp

"""

from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

from . import design
active_exp = design.Experiment("None")
