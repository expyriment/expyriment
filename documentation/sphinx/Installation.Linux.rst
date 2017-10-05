.. _Linux:

Platform-specific instructions: Linux
=====================================

All Linux distributions
-----------------------

1. Use your distribution's package manager to install

  * Python or Python3
  * pip or pip3
  * build-essential (or equivalent)
  * libffi-dev
  * python-dev
  * PortAudio

2. In a command line, run::

    sudo pip install -U pip
    sudo pip install -U expyriment[all]
    
   (Omit ``[all]`` to install without additional optional features; replace ``pip`` with ``pip3`` when using Python 3)

For example, in Debian run::

    sudo apt-get install python python-pip build-essential libffi-dev python-dev libportaudio2
    sudo pip install -U pip
    sudo pip install -U expyriment[optional]
    

Notes
-----
**Switch off desktop effects, when running an experiment**

    Several window managers nowadays come with a compositing engine to produce
    3D desktop effects. To get accurate timing of the visual stimulus
    presentation it is important to switch off desktop effects in your window
    manager!

.. _`release page`: http://github.com/expyriment/expyriment/releases/latest
