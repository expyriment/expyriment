"""
Default settings for design.extras.

This module contains default values for all optional arguments in the init
function of all classes in this package.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from ... import _internals

from ... import _internals
for code in _internals.import_plugins_defaults_code("design"):
    exec(code)
