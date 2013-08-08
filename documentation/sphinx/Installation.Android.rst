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
At the moment you can only download an experimental version from our `download
page`_. In the future, 
once a stable version is released, it will be available in the Google Play 
Store.

Notes
-----
**Experimental version**
    The current version of the "Expyriment Android Runtime" application is an 
    experimental version and in an early development stage! This means that not 
    all features are supported (e.g. no extras plugins) and that there might be
    bugs and other potential problems and limitations.

.. _`PGS4A`: http://pygame.renpy.org
.. _`download page`: http://code.google.com/p/expyriment/downloads/list
