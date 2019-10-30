The Expyriment plugin system (extras)
=====================================

Usage
-----
The design, stimuli, io and misc packages can be extended with plugins
(additional classes) that can be accessed via the 'extras' namespace of each
package. Expyriment will look for installed plugins in the following
locations within the ``.expyriment/extras`` (or ``~expyriment/extras``)
directory located in the current user's home directory:

- ``expyriment_extras_design``
- ``expyriment_extras_stmuli``
- ``expyriment_extras_io``
- ``expyriment_extras_misc``

Any plugins found will be integrated into the *.extras* namespace of each
package (e.g. ``expyriment.stimuli.extras.DotCloud``).

There are three ways to import extras:

1. Import all extras in one go::

    import expyriment
    expyriment.import_all_extras()

2. Import all extras from a specific package::

    import expyriment
    import expyriment.stimuli.extras

3. Import a specific plugin::

    import expyriment
    from expyriment_stimuli_extras.dotcloud import DotCloud

Download plugins from stash
---------------------------
Several extra plugins can be found in the `Expyriment stash`_. When Expyriment
has been installed with the option ``download`` (or ``all``), all plugins can be 
downloaded automatically by calling::

    expyriment.misc.download_from_stash(content="extras")

Alternatively, you can use the `Command Line Interface`_::

    expyriment -D
    
Development
-----------
When developing extra plugins, please consider making them available publicly in
the `Expyriment stash`_, by creating a pull request.

Basically, extra plugins are a simple Python module with a single class, where
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


.. _`Expyriment stash`: http://stash.expyriment.org
.. _`Command Line Interface`: CommandLineInterface.html
