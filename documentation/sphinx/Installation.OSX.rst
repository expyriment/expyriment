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
    brew install python
    sudo /usr/local/bin/python -m pip install --upgrade expyriment[all]

   (Omit ``[all]`` to install without additional optional features)
   
4. To make the Homebrew Python the one that is called when typing "python", in a
   terminal, add the following to ``~/.bash_profile``::

    export PATH=/usr/local/bin:$PATH


Alternative installation (offline)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**On an PC with internet connection (same OS, architecture and Python version!)**

1. On the Desktop, create a directory called ``Expyriment_Installation``

2. Download `Python 2.7.13`_ to ``Expyriment_Installation``

3. Download Tcl_ to ``Expyriment_Installation``

4. Download XQuartz_ to ``Expyriment_Installation``

5. In a terminal, run::

    sudo python -m pip download -d ~/Desktop/Expyriment_Installation expyriment[all]
    
   (Omit ``[all]`` to install without additional optional features)
 
6. To use enhanced video playback, download ffmpeg_ to ``Expyriment_Installation``

7. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device


**On the target PC**

1. Copy the directory ``Expyriment_Installation`` from the portable storage device to the Desktop

2. Install ``Expyriment_Installation/python-2.7.13-macosx10.5.pkg``

3. Install ``Expyriment_Installation/ActiveTcl8.4.19.6.295590-macosx-universal-threaded.dmg``

4. Install ``Expyriment_Installation/XQuartz-2.7.9.dmg``

5. In a command prompt, run::

    python -m pip install --no-index --find-links ~/Desktop/Expyriment_Installation --upgrade expyriment[all]

   (Omit ``[all]`` to install without additional optional features)
   
6. To use enhanced video playback, run::

    mkdir -p ~/.local/bin
    cd ~/Desktop/Expyriment_Installation
    tar -xf Lion_Mountain_Lion_Mavericks_Yosemite_El-Captain_08.12.2016.zip
    mv ffmpeg ffprobe ffserver ~/.local/bin
    echo 'export PATH=$PATH:~/.local/bin' >> ~/.bash_profile
    source ~/.bash_profile


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
    brew install python3
    brew install pygame --without-python
    sudo /usr/local/bin/python3 -m pip install --upgrade expyriment[all]
   
  (Omit ``[all]`` to install without additional optional features)

4. To make the Homebrew Python the one that is called when typing "python", in a
   terminal, add the following to ``~/.bash_profile``::

    export PATH=/usr/local/bin:$PATH


Alternative installation (offline)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**On an PC with internet connection (same OS, architecture and Python version!)**

1. On the Desktop, create a directory called ``Expyriment_Installation``

2. Download `Python 3.6.0`_ to  ``Expyriment_Installation``

3. Download Tcl_ to ``Expyriment_Installation``

4. Download XQuartz_ to ``Expyriment_Installation``

5. In a terminal, run::

    sudo python3 -m pip download -d ~/Desktop/Expyriment_Installation expyriment[all]
   
   (Omit ``[all]`` to install without additional optional features)
 
6. To use enhanced video playback, download ffmpeg_ to ``Expyriment_Installation``

7. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device


**On the target PC**

1. Copy the directory ``Expyriment_Installation`` from the portable storage device to the Desktop

2. Install ``Expyriment_Installation/python-3.6.0-macosx10.5.pkg``

3. Install ``Expyriment_Installation/ActiveTcl8.4.19.6.295590-macosx-universal-threaded.dmg``

4. Install ``Expyriment_Installation/XQuartz-2.7.9.dmg``

5. In a command prompt, run::

    python3 -m pip install --no-index --find-links ~/Desktop/Expyriment_Installation --upgrade expyriment[all]
    
   (Omit ``[all]`` to install without additional optional features)

6. To use enhanced video playback, run::

    mkdir -p ~/.local/bin
    cd ~/Desktop/Expyriment_Installation
    tar -xf Lion_Mountain_Lion_Mavericks_Yosemite_El-Captain_08.12.2016.zip
    mv ffmpeg ffprobe ffserver ~/.local/bin
    echo 'export PATH=$PATH:~/.local/bin' >> ~/.bash_profile
    source ~/.bash_profile



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


.. _`Python 2.7.13`: https://www.python.org/ftp/python/2.7.13/python-2.7.13-macosx10.5.pkg
.. _`Python 3.6.0`: https://www.python.org/ftp/python/3.6.0/python-3.6.0-macosx10.6.pkg
.. _Tcl: http://www.activestate.com/activetcl/downloads/thank-you?dl=http://downloads.activestate.com/ActiveTcl/releases/8.4.19.6/ActiveTcl8.4.19.6.295590-macosx-universal-threaded.dmg
.. _XQuartz: https://dl.bintray.com/xquartz/downloads/XQuartz-2.7.9.dmg
.. _ffmpeg: http://www.ffmpegmac.net/resources/Lion_Mountain_Lion_Mavericks_Yosemite_El-Captain_08.12.2016.zip
