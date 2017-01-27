.. _Linux:

Platform-specific instructions: Linux
=====================================

All Linux distributions (recommended)
-------------------------------------

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
    
     
Debian, Ubuntu and derivatives
------------------------------

We also provide `Debian`_ packages for Expyriment (``python-expyriment``).  We 
suggest to install ``python-expyriment`` via `NeuroDebian`_, a platform
providing a large collection of neuroscience research software. For detailed
instructions see:
`Installing Expyriment via Neurodebian <http://neuro.debian.net/pkgs/python-expyriment.html>`_

*Note*: If you have a previous version of Expyriment installed from source,
please first uninstall the old version using the following command (replace *X*
to match your Python version)::

    sudo rm /usr/local/lib/python2.X/dist-packages/expyriment


Notes
-----
**Switch off desktop effects, when running an experiment**

    Several window managers nowadays come with a compositing engine to produce
    3D desktop effects. To get accurate timing of the visual stimulus
    presentation it is important to switch off desktop effects in your window
    manager!

.. _`release page`: http://github.com/expyriment/expyriment/releases/latest
.. _`Debian`: https://www.debian.org/
.. _`NeuroDebian`: http://neuro.debian.net/
