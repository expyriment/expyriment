"""
Provides the access to the currently active experiment

import ._active to read and write _active.exp

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

exp = None  # expyriment.design.__init__ sets active_exp to design.Experiment("None")
