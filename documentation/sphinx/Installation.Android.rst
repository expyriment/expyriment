.. _Android:

Platform-specific instructions: Android
=======================================

Introduction
------------
With Python and Pygame being ported to Android, it is in principle possible to
use Expyriment on Android devices, however, without OpenGL and extras support.
This is achived by compiling Python, Pygame and Expyriment into a Java app,
for intance by using `PGS4A`_.


Option 1: Pydroid3
------------------
The easiest way to run experiments on Android devices is to install the already
available `Pydroid3`_.

Once installed, go to the menu option "Pip", type in "expyriment" as the library name and click "INSTALL".
Expyriment scripts can then be opened and run from the main view.

(At first usage, it seems to be necessary to import Pygame once with
``import pygame`` before importing Expyriment).

Option 2: Expyriment Android Runtime
------------------------------------
We also provide the "Expyriment Android Runtime", an Android application which
can be used to directly run experiments on an Andoroid device (with Android >
2.2). You can download the current version from our `Android release
page`_.

**Please note, however, that this is only available for an older version of
Expyriment (0.7.0)!**

Once installed, the application will look for Expyriment scripts (each in its own
subdirectory) in a directory called 'expyriment', located at the root level of
either storage device under 'mnt' (i.e. the internal or external SD card).
Examples of correctly located Expyriment scripts include::

    /mnt/sdcard0/expyriment/exp1/exp1.py
    
    /mnt/sdcard0/expyriment/exp2/exp2.py
    
    /mnt/extSdCard/expyriment/exp3/exp3.py
    
    /mnt/extSdCard/expyriment/exp4/exp4.py

Notes
-----

**OpenGL not supported**
Currently, OpenGL mode is not supported on Android. This will affect the timing
of visual stimuli as blocking on the vertical retrace is not possible (see also
`Timing`_). To run a script without OpenGL mode, ``expyriment.control.defaults.opengl`` needs to be set to ``0``.

**Extras not supported**
Currently, extras are not supported on Android. This also means that the plugin
system is not available.


.. _`PGS4A`: https://github.com/startgridsrc/pgs4a
.. _`Pydroid3`: https://play.google.com/store/apps/details?id=ru.iiec.pydroid3&gl=US
.. _`Android release page`: https://github.com/expyriment/expyriment-android-runtime/releases
.. _`Timing`: Timing.html
