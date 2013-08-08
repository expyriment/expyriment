"""
Default settings for design.extras.

This module contains default values for all optional arguments in the init
function of all classes in this package.

"""

__author__ = 'Florian Krause <florian@expyriment.org, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from expyriment import _importer_functions


for _plugins in [_importer_functions.import_plugin_defaults(__file__),
                _importer_functions.import_plugin_defaults_from_home(__file__)]:
    for _defaults in _plugins:
        exec(_defaults)
