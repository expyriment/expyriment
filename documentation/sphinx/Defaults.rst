Defaults (settings)
==================
For each submodule of Expyriment, there are various default settings that,
when changed, alter the default behaviour of the related functionality.
Changing the default settings is hence a way to globally customize
Expyriment functionality.

expyriment.control.defaults_
------------------------------
The default settings of the control submodule is special, since it clusters
together several settings from other submodules which are important for
experimental control in one central place. The settings here have preceedance!

expyriment.design.defaults_
---------------------------
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.design can be set via:
```
expyriment.design.defaults.classname_parametername = x
```

expyriment.stimuli.defaults_
----------------------------
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.stimuli can be set via:
```
expyriment.stimuli.defaults.classname_parametername = x
```

expyriment.io.defaults_
-----------------------
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.io can be set via:
```
expyriment.io.defaults.classname_parametername = x
```

expyriment.misc.defaults_
-------------------------
The parameters of every class' constructor (i.e. the parameters when creating
an instance of this class) within expyriment.misc can be set via:
```
expyriment.misc.defaults.classname_parametername = x
```
