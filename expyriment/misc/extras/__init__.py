"""The misc extra package.

Notes
-----
To us the extras module you have to import it manually by calling:
`import expyriment.misc.extras`

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'

from ... import _internals

print("Misc plugins:")
for name, code in _internals.import_plugins_code("misc").items():
    print(" " + name)
    try:
        exec(code)
    except Exception as err:
        print(f"Warning: Could not import {name}")
        print(f" {err}")

try:
    del (name, code)
except Exception:
    pass
