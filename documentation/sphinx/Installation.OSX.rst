.. _OSX:

Platform-specific instructions: macOS
=====================================

There are two different ways to install Expyriment. The recommended method
requires an active internet connection. If you need to install Expyriment on a
computer that has no internet connection (like lab PCs), please use the
alternative method. 

Each method will rely on an additional (different) Python environment and will
not alter the Python environment provided by Apple.


Default installation (online)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install `Python 3.10.6`_

2. In a terminal, run::

    sudo python3 -m pip install -U expyriment[all]
   
   (Omit ``[all]`` to install without additional optional features)

    
Alternative installation (offline)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**On an PC with internet connection (same OS, architecture and Python version!)**

1. On the Desktop, create a directory called ``Expyriment_Installation``

2. Download `Python 3.10.6`_ to  ``Expyriment_Installation``

3. In a terminal, run::

    sudo python3 -m pip download -d ~/Desktop/Expyriment_Installation expyriment[all]
   
   (Omit ``[all]`` to install without additional optional features)
 
6. To use enhanced video playback, download ffmpeg_ to ``Expyriment_Installation``

7. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device


**On the target PC**

1. Copy the directory ``Expyriment_Installation`` from the portable storage device to the Desktop

2. Install ``Expyriment_Installation/python-3.10.6-macos11.pkg``

3. In a command prompt, run::

    sudo python3 -m pip install --no-index --find-links ~/Desktop/Expyriment_Installation -U expyriment[all]
    
   (Omit ``[all]`` to install without additional optional features)

6. To use enhanced video playback, run::

    mkdir -p ~/.local/bin
    cd ~/Desktop/Expyriment_Installation
    tar -xf ffmpeg-5.1.zip
    mv ffmpeg ffprobe ffserver ~/.local/bin
    echo 'export PATH=$PATH:~/.local/bin' >> ~/.bash_profile
    source ~/.bash_profile



Notes
-----

**Be aware of multiple Python installations**

    If, after installation, you get errors about Expyriment (or one of its dependencies)
    not being installed, chances are you try to import Expyriment in the "wrong"
    (i.e. Apple's) Python environment.

    Make sure you are calling ``python3``.

**Do not start your experiments out of IDLE**

    If you are using the IDLE editor that comes with the Python installation, 
    be aware that IDLE itself is written in Python. Starting your Expyriment 
    programme out of IDLE (by clicking on "Run" or by pressing F5), might thus 
    lead to improper timing!

    We therefore strongly suggest to run Expyriment programmes from the command 
    line when testing participants.


.. _Python 3.10.6: https://www.python.org/ftp/python/3.10.6/python-3.10.6-macos11.pkg
.. _ffmpeg: https://evermeet.cx/ffmpeg/ffmpeg-5.1.zip
