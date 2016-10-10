.. _Android:

Platform-specific instructions: Android
=======================================

Introduction
------------
With Python and Pygame being ported to Android (`PGS4A`_), it is in principle
possible to use Expyriment on Android devices, however, without OpenGL support.
This can be achieved by compiling Python, Pygame and Expyriment into a Java
app, using `PGS4A`_.
For ease of use, we provide the "Expyriment Android Runtime", an Android
application which can be used to directly run experiments on an Andoroid device
(with Android > 2.2).

Installing Expyriment
---------------------
The easiest way to run experiments on Android devices is to use our "Expyriment
Android Runtime" appplication.
You can download the current version from our `Android release
page`_.

Installing Expyriment scripts
-----------------------------
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

**Extra plugins not supported**

    The current version of the "Expyriment Android Runtime" does not support extras plugins.


.. _`PGS4A`: http://pygame.renpy.org
.. _`Android release page`: https://github.com/expyriment/expyriment-android-runtime/releases
