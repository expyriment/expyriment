Defaults (settings)
===================
For each package of Expyriment, there are various default settings, defining
the behaviour of elements of that package.

Usage
-----
When changed, these settings alter the default behaviour of the related
functionality. Changing the default settings is hence a way to globally
customize Expyriment functionality.

expyriment.control.defaults_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The default settings of the control package is special, since it clusters
together several settings from other packages which are important for
experimental control in one central place. The settings here have preceedance!

expyriment.design.defaults_
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.design can be set via:
``expyriment.design.defaults.classname_parametername = x``

`expyriment.stimuli.defaults`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.stimuli can be set via:
``expyriment.stimuli.defaults.classname_parametername = x``

`expyriment.io.defaults`_
~~~~~~~~~~~~~~~~~~~~~~~~~
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.io can be set via:
``expyriment.io.defaults.classname_parametername = x``

`expyriment.misc.defaults`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.misc can be set via:
``expyriment.misc.defaults.classname_parametername = x``


.. _`expyriment.control.defaults`: expyriment.control.defaults.html 
.. _`expyriment.design.defaults`: expyriment.design.defaults.html
.. _`expyriment.stimuli.defaults`: expyriment.stimuli.defaults.html
.. _`expyriment.io.defaults`: expyriment.io.defaults.html
.. _`expyriment.misc.defaults`: expyriment.misc.defaults.html
