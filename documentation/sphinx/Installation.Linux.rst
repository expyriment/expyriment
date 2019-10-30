.. _Linux:

Platform-specific instructions: Linux
=====================================

All Linux distributions
-----------------------

1. Use your distribution's package manager to install

  * Python or Python3
  * setuptools
  * pip or pip3
  * build-essential (or equivalent)
  * libffi-dev
  * python-dev or python3-dev
  * PortAudio
  * ffmpeg (for enhanced video support, optional)

2. In a command line, run::

    sudo pip install -U pip
    sudo pip install -U expyriment[all]
    
   (Omit ``[all]`` to install without additional optional features; replace ``pip`` with ``pip3`` when using Python 3)

For example, in Debian run::

    sudo apt-get install python3 python3-pip python3-setuptools build-essential libffi-dev python3-dev libportaudio2 ffmpeg
    sudo pip3 install -U pip
    sudo pip3 install -U expyriment[all]
    

Notes
-----
**Switch off desktop effects, when running an experiment**

    Several window managers nowadays come with a compositing engine to produce
    3D desktop effects. To get accurate timing of the visual stimulus
    presentation it is important to switch off desktop effects in your window
    manager!

.. _`release page`: http://github.com/expyriment/expyriment/releases/latest
