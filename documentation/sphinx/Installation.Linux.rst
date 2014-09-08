.. _Linux:

Platform-specific instructions: Linux
=====================================


Debian, Ubuntu and derivatives
-------------------------------

We provide a `Debian`_ packages for Expyriment (``python-expyriment``).  We 
suggest to installed ``python-expyriment`` via `NeuroDebian`_, a platform 
providing a large collection of neuroscience research software.  For detailed 
instructions see:
`Installing Expyriment via Neurodebian <http://neuro.debian.net/pkgs/python-expyriment.html>`_

*Note*: If you have a previous version of Expyriment installed from source,
please first uninstall the old version using the following command (replace *X*
to match your Python version)::

    sudo rm /usr/local/lib/python2.X/dist-packages/expyriment

Unstable pre-releases of Expyriment for Ubuntu can be found in our `Expyriment PPA <https://launchpad.net/~lindemann09/+archive/expyriment>`_.


Other Linux distributions
-------------------------

For all other Linux distributions, you can download the file
expyriment-|release|.zip from the `release page`_ and install as described
here_. Alternatively, you can use the following command, which is doing this
for you::

    wget -P /tmp 'https://raw.github.com/expyriment/expyriment/master/tools/expyriment_online_install_linux.sh' && sh /tmp/expyriment_online_install_linux.sh

Don't forget to install all :doc:`required software packages </Installation>`.


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
