.. _OSX:

Platform-specific instructions: OS X
====================================

There are different ways to install Expyriment on OS X.
The easiest way is to let MacPorts take care of all dependencies.
Alternatively, all dependencies can be downloaded and installed manually.
Both options will install an additional Python environment and will not alter
the Python environment provided by Apple.

**If, after installation, you get errors about Expyriment (or one of its dependencies)
not being installed, chances are you trying to import Expyriment in the "wrong"
(i.e. Apple's) Python environment.**

Using MacPorts (recommended)
----------------------------
After having installed MacPorts_ run the following command from the
terminal to install all dependencies::
    sudo port selfupdate && sudo port install xorg-server python27 py27-game py27-opengl py27-numpy py27-pil py27-serial

To make the MacPorts Python the one that is called when typing "python"
into a terminal, run the following command from the terminal::
    sudo port select --set python python27
(Please note that this can be reversed by calling the command again, substituting "python27" with "none").

To install Expyriment, download "expyriment-|release|.zip from the `Release page`_ and install as described here_.

Manually (alternative)
----------------------
To install basic dependencies, download the following installers and follow their instructions:

 * `Python 2`_
 * Tcl_
 * XQuartz_ (only for OS X 10.9 and higher)
 * Pygame_
 * NumPy_

In addition:

 * Download PyOpenGL_ and install as described here_
 * Download PySerial_ and install as described here_

Note, Expyriment only runs with a 32-bit version of Python 2. Also all required 
packages have to be 32-bit compiled!

To install Expyriment:

 * Download "expyriment-|release|.zip from the `Release page`_ and install as described here_

Notes
-----

**Do not start your experiments out of IDLE**

    If you are using the IDLE editor that comes with the Python installation, 
    be aware that IDLE itself is written in Python. Starting your Expyriment 
    programme out of IDLE (by clicking on "Run" or by pressing F5), might thus 
    lead to improper timing!

    We therefore strongly suggest to run Expyriment programmes from the command 
    line when testing participants.

.. _`MacPorts`: https://www.macports.org/install.php
.. _`Python 2`: http://python.org/ftp/python/2.7.6/python-2.7.6-macosx10.3.dmg
.. _Tcl: http://www.activestate.com/activetcl/downloads/thank-you?dl=http://downloads.activestate.com/ActiveTcl/releases/8.4.19.6/ActiveTcl8.4.19.6.295590-macosx-universal-threaded.dmg
.. _XQuartz: http://xquartz.macosforge.org/downloads/SL/XQuartz-2.7.7.dmg
.. _Pygame: http://pygame.org/ftp/pygame-1.9.1release-python.org-32bit-py2.7-macosx10.3.dmg
.. _Numpy:  http://sourceforge.net/projects/numpy/files/NumPy/1.8.0/numpy-1.8.0-py2.7-python.org-macosx10.6.dmg/download
.. _PyOpenGL:  http://pypi.python.org/packages/source/P/PyOpenGL/PyOpenGL-3.0.2.zip
.. _PySerial: http://sourceforge.net/projects/pyserial/files/pyserial/2.7/pyserial-2.7.tar.gz/download
..  _here: http://docs.python.org/install/index.html#the-new-standard-distutils
.. _`Release page`: http://github.com/expyriment/expyriment/releases/latest
