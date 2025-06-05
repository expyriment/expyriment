"""
The misc extra package.

Notes
-----
    To us the extras module you have to import it manually by calling:
    `import expyriment.misc.extras`

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'

import contextlib

from ... import _internals

print("Misc plugins:")
for name, code in _internals.import_plugins_code("misc").items():
    print(" " + name)
    try:
        exec(code)
    except Exception as err:
        print("Warning: Could not import {0}".format(name))
        print(" {0}".format(err))

with contextlib.suppress(Exception):
    del (name, code)
