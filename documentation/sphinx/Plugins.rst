The Expyriment plugin system (extras)
=====================================

Usage
-----
The design, stimuli, io and misc packages can be extended with plugins
(additional classes) that can be accessed via the 'extras' namespace of each
package. There are two locations Expyriment will look for installed plugins:

1. In the ``extras`` directories of the corresponding packages of the
   Expyriment installation.
2. In the ``design``, ``stmuli``, ``io`` and ``misc`` directories within a
   ``.expyriment`` or ``~expyriment`` directory located in the current user's
   home directory

In both cases, plugins will be integrated into the *.extras* namespace of each
package (e.g. ``expyriment.stimuli.extras.DotCloud``).

Development
-----------
Basically, extra plugins are a simple python module with a single class, where
the filename is the class name in lowercase. Additionally a file called
``classname_defaults.py`` can be created which will hold the default values for
all parameters given when initializing the class. The naming convention is
``classname_parameter``.
For design and misc extras this is all there is, but for io and stimuli plugins,
additional conventions need to be taken care of.

io.extras
~~~~~~~~~
IO plugins have to inherit from ``expyriment.io.Input`` or ``expyriment.io.Output``
or both. This means they can also inherit from any other io class.

stimuli.extras
~~~~~~~~~~~~~~
Stimulus plugins have to inherit from ``expyriment.stimuli.Stimulus``. This means
they can also inherit from any other stimulus class.
Additionally, every visual extra stimulus class (inherited from ``expyriment.stimuli.Visual``)
needs a ``_create_surface`` method that defines what happens when the stimulus is preloaded,
plotted or presented.
