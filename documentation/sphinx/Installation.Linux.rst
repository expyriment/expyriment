.. _Linux:

Platform-specific instructions: Linux
=====================================

All Linux distributions
-----------------------

1. Use your distribution's package manager to install

  * Python 2
  * pip
  * Pygame

2. In a command line, run ::

    sudo pip install --upgrade pip
    sudo pip install --upgrade expyriment

For the alternative packages (optional):

3. Use your distribution's package manager to install

  * Numpy
  * PyParallel
  * PySerial


Debian, Ubuntu and derivatives
------------------------------

We provide a `Debian`_ packages for Expyriment (``python-expyriment``).  We 
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
