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

    wget -P /tmp 'https://raw.github.com/expyriment/expyriment-tools/master/expyriment_online_install_linux.sh' && sh /tmp/expyriment_online_install_linux.sh

Alternatively, you can download "expyriment-|release|.zip from the
`Release page`_ and install as described here_.

(For Ubuntu, there is furthermore an Expyriment package available through the 
following third-party PPA: https://launchpad.net/~smathot/+archive/cogscinl.
Please note that we do not provide support for this package.)

Notes
-----
**Switch off desktop effects, when running an experiment**

    Several window managers nowadays come with a compositing engine to produce  
    3D desktop effects. To get accurate timing of the visual stimulus 
    presentation it is important to switch off desktop effects in your window 
    manager!

..  _here: http://docs.python.org/install/index.html#the-new-standard-distutils
.. _`Release page`: http://github.com/expyriment/expyriment/releases/latest
