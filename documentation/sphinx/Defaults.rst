Defaults (settings)
==================
For each submodule of Expyriment, there are various default settings, defining
the behaviour of elements of that submodule.

Usage
-----
When changed, these settings alter the default behaviour of the related
functionality. Changing the default settings is hence a way to globally
customize Expyriment functionality.

expyriment.control.defaults_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The default settings of the control submodule is special, since it clusters
together several settings from other submodules which are important for
experimental control in one central place. The settings here have preceedance!

expyriment.design.defaults_
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.design can be set via:
```
expyriment.design.defaults.classname_parametername = x
```

expyriment.stimuli.defaults_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.stimuli can be set via:
```
expyriment.stimuli.defaults.classname_parametername = x
```

expyriment.io.defaults_
~~~~~~~~~~~~~~~~~~~~~~~
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.io can be set via:
```
expyriment.io.defaults.classname_parametername = x
```

expyriment.misc.defaults_
~~~~~~~~~~~~~~~~~~~~~~~~~
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.misc can be set via:
```
expyriment.misc.defaults.classname_parametername = x
```

Development
-----------
When developing Plugins_ default values can be integrated into extras.defaults.
Upon start, Expyriment will read all files in the extra folder that have the same
name as the plugin, followd by "_defaults.py" (e.g. dotcloud_defaults.py).
All variables within this file will be integrated into the namespace and will
be available in extras.defaults (e.g. expyriment.stimuli.extras.defaults).
