"""
The stimuli extra package.

Notes
-----
    To us the extras module you have to import it manually by calling:
    `import expyriment.stimuli.extras`

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

from ... import _internals

print("Stimuli plugins:")
for name, code in _internals.import_plugins_code("stimuli").items():
    print(" " + name)
    try:
        exec(code)
    except Exception as err:
        print("Warning: Could not import {0}".format(name))
        print(" {0}".format(err))

try:
    del (name, code)
except Exception:
    pass
