.. _OSX:

Platform-specific instructions: Mac OS X
========================================

Dependencies
------------
If you are using OS X, download the following installers and follow their 
instructions:

* `Python 2`_
* Tcl_
* Pygame_

and, if needed:

* NumPy_
* PyOpenGL_ and PySerial_ (has to be installed as described here_).


Installing Expyriment
---------------------
Download "expyriment-|release|.zip from the `Release page`_ and install as described here_.

Notes
-----
**Do not start your experiments out of IDLE**

    If you are using the IDLE editor that comes with the Python installation, 
    be aware that IDLE itself is written in Python. Starting your Expyriment 
    programme out of IDLE (by clicking on "Run" or by pressing F5), might thus 
    lead to improper timing!

    We therefore strongly suggest to run Expyriment programmes from the command 
    line when testing participants.

.. _`Python 2`: http://python.org/ftp/python/2.7.6/python-2.7.6-macosx10.3.dmg
.. _Tcl: http://www.activestate.com/activetcl/downloads/thank-you?dl=http://downloads.activestate.com/ActiveTcl/releases/8.4.19.6/ActiveTcl8.4.19.6.295590-macosx-universal-threaded.dmg
.. _Pygame: http://pygame.org/ftp/pygame-1.9.1release-python.org-32bit-py2.7-macosx10.3.dmg
.. _Numpy:  http://sourceforge.net/projects/numpy/files/NumPy/1.8.0/numpy-1.8.0-py2.7-python.org-macosx10.6.dmg/download
.. _PyOpenGL:  http://pypi.python.org/packages/source/P/PyOpenGL/PyOpenGL-3.0.2.zip
.. _PySerial: http://sourceforge.net/projects/pyserial/files/pyserial/2.7/pyserial-2.7.tar.gz/download
..  _here: http://docs.python.org/install/index.html#the-new-standard-distutils
.. _`Release page`: http://github.com/expyriment/expyriment/releases/latest
