.. _Linux:

Platform-specific instructions: Linux
=====================================

Dependencies
------------
If you are in the lucky position of working on a Linux system, installing the
required packages can be easily done via your package manager. On Debian-based
systems the following command will install dependencies in one go::

    sudo apt-get install python python-pygame python-opengl python-serial python-parallel python-numpy

Installing from Debian or Ubuntu repository
--------------------------------------------
Under `Ubuntu`_, Expyriment can be installed via the Expyriment Personal
Package Archiv (PPA_). You merely have to add the repository and install
``python-expyriment``::

    sudo add-apt-repository ppa:lindemann09/expyriment
    sudo apt-get update
    sudo apt-get install python-expyriment

**Note**: If you have previous versions of Expyriment installed from source,
please first uninstall the old version using the following command (replace *X*
to match your Python version)::

    sudo rm usr/local/lib/python2.X/dist-packages/expyriment

The package ``python-expyriment`` is also part of the `NeuroDebian`_ software
platform, which provides a large collection of popular neuroscience research
software for the `Debian`_ operating system and derivatives. Please visit the
`Neurodebian`_ website for further instructions.


Installing from source
-----------------------
For all other Linux distributions, you can download the file
expyriment-|release|.zip from the `release page`_ and install as described
here_. Alternatively, you can use the following command, which is doing this
for you::

    wget -P /tmp 'https://raw.github.com/expyriment/expyriment-tools/master/expyriment_online_install_linux.sh' && sh /tmp/expyriment_online_install_linux.sh

.. FIXME installation script depends on unzip

Notes
-----
**Switch off desktop effects, when running an experiment**

    Several window managers nowadays come with a compositing engine to produce
    3D desktop effects. To get accurate timing of the visual stimulus
    presentation it is important to switch off desktop effects in your window
    manager!

..  _here: http://docs.python.org/install/index.html#the-new-standard-distutils
.. _`release page`: http://github.com/expyriment/expyriment/releases/latest
.. _`Debian`: https://www.debian.org/
.. _`NeuroDebian`: http://neuro.debian.net/
.. _`Ubuntu`: http://www.ubuntu.com/
.. _`PPA`: https://launchpad.net/~lindemann09/+archive/expyriment
