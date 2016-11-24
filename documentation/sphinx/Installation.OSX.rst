.. _OSX:

Platform-specific instructions: OS X
====================================

Expyriment can be installed for Python 2 or Python 3. In both cases there are
two different ways to install Expyriment. The recommended method requires an
active internet connection. If you need to install Expyriment on a computer that
has no internet connection (like lab PCs), please use the alternative method. 

Each method will rely on an additional (different) Python environment and will
not alter the Python environment provided by Apple.


Python 2
--------

Default installation (online)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install XQuartz_

2. Install Xcode Command Line Tools by running the following in a terminal::

   xcode-select --install

3. In a terminal, run::

   /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
   brew tap Homebrew/python
   brew update
   brew install python pygame
   sudo /usr/local/bin/python -m pip install --upgrade expyriment

4. To make the Homebrew Python the one that is called when typing "python", in a
terminal, add the following to ``~/.bash_profile``::

    export PATH=/usr/local/bin:$PATH

For the alternative packages (optional):

4. In a terminal, run ::

    sudo /usr/local/bin/python -m pip install --upgrade pyserial


Alternative installation (offline)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**On an PC with internet connection (same OS, architecture and Python version!)**

1. On the Desktop, create a directory called ``Expyriment_Installation``

2. Download `Python 2.7.11`_ to  ``Expyriment_Installation``

3. Download Tcl_ to ``Expyriment_Installation``

4. Download XQuartz_ to ``Expyriment_Installation``

5. Download Pygame_ to ``Expyriment_Installation``

7. In a terminal, run::

    sudo python -m pip download -d ~/Desktop/Expyriment_Installation expyriment
 
5. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device
    
For the additional packages (optional):

6. In a command prompt, run::

    sudo python -m pip download -d ~/Desktop/Expyriment_Installation 'pyserial>=3,<4'

7. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device


**On the target PC**

1. Copy the directory ``Expyriment_Installation`` from the portable storage device to the Desktop

2. Install ``Expyriment_Installation/python-2.7.12-macosx10.5.pkg``

3. Install ``Expyriment_Installation/ActiveTcl8.4.19.6.295590-macosx-universal-threaded.dmg``

4. Install ``Expyriment_Installation/XQuartz-2.7.9.dmg``

5. Install ``Expyriment_Installation/pygame-1.9.1release-python.org-32bit-py2.7-macosx10.3.dmg``

4. In a command prompt, run::

    python -m pip install --no-index --find-links ~/Desktop/Expyriment_Installation --upgrade expyriment

For the additional packages (optional):

5. In a command prompt, run::

    python -m pip install --no-index --find-links ~/Desktop/Expyriment_Installation --upgrade 'pyserial>=3,<4'


Python 3
--------

Default installation (online)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install XQuartz_

2. Install Xcode Command Line Tools by running the following in a terminal::

   xcode-select --install

3. In a terminal, run::

   /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
   brew tap Homebrew/python
   brew update
   brew install python3 pygame
   brew install pygame --without-python
   sudo /usr/local/bin/python3 -m pip install --upgrade expyriment

4. To make the Homebrew Python the one that is called when typing "python", in a
terminal, add the following to ``~/.bash_profile``::

    export PATH=/usr/local/bin:$PATH

For the alternative packages (optional):

4. In a terminal, run ::

    sudo /usr/local/bin/python3 -m pip install --upgrade pyserial


Alternative installation (offline)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**On an PC with internet connection (same OS, architecture and Python version!)**

1. On the Desktop, create a directory called ``Expyriment_Installation``

2. Download `Python 3.5.2`_ to  ``Expyriment_Installation``

3. Download Tcl_ to ``Expyriment_Installation``

4. Download XQuartz_ to ``Expyriment_Installation``

5. In a terminal, run::

    sudo python3 -m pip download -d ~/Desktop/Expyriment_Installation --pre pygame
 
6. In a terminal, run::

    sudo python3 -m pip download -d ~/Desktop/Expyriment_Installation expyriment
 
7. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device
    
For the additional packages (optional):

8. In a command prompt, run::

    sudo python3 -m pip download -d ~/Desktop/Expyriment_Installation 'pyserial>=3,<4'

9. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device


**On the target PC**

1. Copy the directory ``Expyriment_Installation`` from the portable storage device to the Desktop

2. Install ``Expyriment_Installation/python-3.5.2-macosx10.5.pkg``

3. Install ``Expyriment_Installation/ActiveTcl8.4.19.6.295590-macosx-universal-threaded.dmg``

4. Install ``Expyriment_Installation/XQuartz-2.7.9.dmg``

5. In a command prompt, run::

    python3 -m pip install --no-index --find-links ~/Desktop/Expyriment_Installation --upgrade --pre pygame

6. In a command prompt, run::

    python3 -m pip install --no-index --find-links ~/Desktop/Expyriment_Installation --upgrade expyriment

For the additional packages (optional):

7. In a command prompt, run::

    python3 -m pip install --no-index --find-links ~/Desktop/Expyriment_Installation --upgrade 'pyserial>=3,<4'


Notes
-----

**Be aware of multiple Python installations**

    If, after installation, you get errors about Expyriment (or one of its dependencies)
    not being installed, chances are you try to import Expyriment in the "wrong"
    (i.e. Apple's) Python environment.

    Make sure you are calling ``/usr/local/bin/python``.

**Do not start your experiments out of IDLE**

    If you are using the IDLE editor that comes with the Python installation, 
    be aware that IDLE itself is written in Python. Starting your Expyriment 
    programme out of IDLE (by clicking on "Run" or by pressing F5), might thus 
    lead to improper timing!

    We therefore strongly suggest to run Expyriment programmes from the command 
    line when testing participants.


.. _`Python 2.7.12`: https://www.python.org/ftp/python/2.7.12/python-2.7.12-macosx10.5.pkg
.. _`Python 3.5.2`: https://www.python.org/ftp/python/3.5.2/python-3.5.2-macosx10.5.pkg
.. _Tcl: http://www.activestate.com/activetcl/downloads/thank-you?dl=http://downloads.activestate.com/ActiveTcl/releases/8.4.19.6/ActiveTcl8.4.19.6.295590-macosx-universal-threaded.dmg
.. _XQuartz: https://dl.bintray.com/xquartz/downloads/XQuartz-2.7.9.dmg
.. _Pygame: http://pygame.org/ftp/pygame-1.9.1release-python.org-32bit-py2.7-macosx10.3.dmg
