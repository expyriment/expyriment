"""The io extra package.

Notes
-----
To us the extras module you have to import it manually by calling:
`import expyriment.io.extras`

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'

from ... import _internals

print("IO plugins:")
for name, code in _internals.import_plugins_code("io").items():
    print(" " + name)
    try:
        exec(code)
    except Exception as err:
        print("Warning: Could not import {}".format(name))
        print(" {}".format(err))

try:
    del (name, code)
except Exception:
    pass
