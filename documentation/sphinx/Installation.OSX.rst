.. _OSX:

Platform-specific instructions: OS X
====================================

There are two different ways to install Expyriment on OS X.

Each will rely on an additional (different) Python environment and will not alter
the Python environment provided by Apple.


Using MacPorts and PyPi (recommended)
-------------------------------------

1. Install MacPorts_
2. In a terminal, run ::

    sudo port selfupdate
    sudo port install xorg-server tcl python27 py27-pip py27-game
    sudo /opt/local/bin/python2.7 -m pip install expyriment

3. To make the MacPorts Python the one that is called when typing "python", in a terminal, run ::

    sudo port select --set python python27

   (Please note that this can be reversed by calling the command again, substituting "python27" with "none").

For the alternative packages (optional):

4. In a terminal, run ::

    sudo port selfupdate
    sudo port install py27-serial
    sudo /opt/local/bin/python2.7 -m pip install matplotlib numpy pillow pyxid


Manually (alternative)
----------------------

1. Install `Python 2.7.9`_
2. Install Tcl_
3. Install XQuartz_ (only for OS X 10.9 and higher)
4. Install Pygame_
5. Install PyOpenGL_
6. In a terminal, run ::

   sudo /usr/local/bin/python -m pip expyriment

For the additional packages (optional):

7. Download Matplotlib_ and install it in a terminal with ::

    sudo /usr/local/bin/python -m pip install <downloaded file>

8. Download Numpy_ and install it in a terminal with ::

    sudo /usr/local/bin/python -m pip install <downloaded file>

9. Download Pillow_ and install it in a terminal with ::

    sudo /usr/local/bin/python -m pip install <downloaded file>

10. Download PySerial_, unpack it, and install it in a terminal with ::

    sudo /usr/local/bin/python setup.py install

11. Download Pyxid_, unpack it, and install it in a terminal with ::

    sudo /usr/local/bin/python setup.py install


Notes
-----

**Be aware of multiple Python installations**

    If, after installation, you get errors about Expyriment (or one of its dependencies)
    not being installed, chances are you try to import Expyriment in the "wrong"
    (i.e. Apple's) Python environment.

    Make sure you are calling ``/opt/local/bin/python2.7``
    or ``/usr/local/bin/python``, depending on how you installed Expyriment.

**Do not start your experiments out of IDLE**

    If you are using the IDLE editor that comes with the Python installation, 
    be aware that IDLE itself is written in Python. Starting your Expyriment 
    programme out of IDLE (by clicking on "Run" or by pressing F5), might thus 
    lead to improper timing!

    We therefore strongly suggest to run Expyriment programmes from the command 
    line when testing participants.


.. _`MacPorts`: https://www.macports.org/install.php
.. _`Python 2.7.9`: https://www.python.org/ftp/python/2.7.9/python-2.7.9-macosx10.5.pkg
.. _Tcl: http://www.activestate.com/activetcl/downloads/thank-you?dl=http://downloads.activestate.com/ActiveTcl/releases/8.4.19.6/ActiveTcl8.4.19.6.295590-macosx-universal-threaded.dmg
.. _XQuartz: http://xquartz.macosforge.org/downloads/SL/XQuartz-2.7.7.dmg
.. _Pygame: http://pygame.org/ftp/pygame-1.9.1release-python.org-32bit-py2.7-macosx10.3.dmg
.. _PyOpenGL:  http://pypi.python.org/packages/source/P/PyOpenGL/PyOpenGL-3.0.2.zip
.. _Matplotlib: https://downloads.sourceforge.net/project/matplotlib/matplotlib/matplotlib-1.4.3/mac/matplotlib-1.4.3-cp27-none-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl
.. _Numpy: https://pypi.python.org/packages/cp27/n/numpy/numpy-1.9.2-cp27-none-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl#md5=296f576bb648b8195b379b0bf39791ce
.. _Pillow: https://pypi.python.org/packages/cp27/P/Pillow/Pillow-2.8.1-cp27-none-macosx_10_6_intel.macosx_10_9_intel.macosx_10_9_x86_64.macosx_10_10_intel.macosx_10_10_x86_64.whl#md5=e1486bbd4777e6c9f35ad14081212f6f
.. _PySerial: http://sourceforge.net/projects/pyserial/files/pyserial/2.7/pyserial-2.7.tar.gz/download
.. _Pyxid: https://pypi.python.org/packages/source/p/pyxid/pyxid-1.0.tar.gz
.. _`Release page`: http://github.com/expyriment/expyriment/releases/latest
