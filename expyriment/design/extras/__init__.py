"""The design extra package.

Notes
-----
    To us the extras module you have to import it manually by calling:
    `import expyriment.design.extras`


"""

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import os as _os

from . import defaults
from ... import _internals


for _plugins in [_internals.import_plugins(__file__),
                _internals.import_plugins_from_settings_folder(__file__)]:
    for _plugin in _plugins:
        try:
            exec(_plugins[_plugin])
        except Exception as err:
            print("Warning: Could not import {0}".format(
                _os.path.dirname(__file__) + _os.sep + _plugin))
            print(" {0}".format(err))
