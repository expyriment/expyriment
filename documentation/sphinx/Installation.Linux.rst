.. _Linux:

Platform-specific instructions: Linux
=====================================

Dependencies
------------
If you are in the lucky position of working on a Linux system, installing the 
required packages can be easily done via your package manager. On Debian-based 
systems (e.g. Ubuntu) the following command will install everything in one go::

    sudo apt-get install python python-pygame python-opengl python-serial python-parallel python-numpy

Installing Expyriment
---------------------
You can then install Expyriment with the online installer::

    wget -P /tmp 'http://expyriment.googlecode.com/files/expyriment_online_install_linux.sh' && sh /tmp/expyriment_online_install_linux.sh

Alternatively, you can download the `Expyriment source`_ (.zip) and install as 
described here_.

For Ubuntu, there is furthermore an Expyriment package available through the 
following third-party PPA: https://launchpad.net/~smathot/+archive/cogscinl)

Notes
-----
**Switch off desktop effects, when running an experiment**

    Several window managers nowadays come with a compositing engine to produce  
    3D desktop effects. To get accurate timing of the visual stimulus 
    presentation it is important to switch off desktop effects in your window 
    manager!

.. _`Expyriment Source`: https://github.com/expyriment/expyriment/releases/latest
..  _here: http://docs.python.org/install/index.html#the-new-standard-distutils
