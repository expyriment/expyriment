Installation
============

Expyriment works with `Python`_ 2 and 3.


Dependencies
------------

Expyriment depends on the following Python packages:

* Future_ (>=0.15)
* Pygame_ (>=1.9)
* PyOpenGL_ (>=3.0)

Additional Python packages, which are optional and only required for some features of 
Expyriment are:

* NumPy_ (>=1.6) (to use data preprocessing)
* mediadecoder_ (>=0.1) (to use enhanced video playback)
* sounddevice_ (>=0.3) (to use enhanced video playback with audio)
* PySerial_ (>=3.0) (to use serial port communication)
* PyParallel_ (>=0.2) (to use parallel port communication on Linux)

Please be aware that Expyriment plugins (extras) might have further dependencies.


Installing with ``pip``
-----------------------

Expyriment (and its dependencies) can be installed with ``pip``::

    pip install expyriment[optional]

Omit ``[optional]`` to install without additional packages.

Replace ``pip`` with ``pip3`` when using Python3.


Platform-specific instructions
------------------------------

We provide more detailed platform-specific instructions for installing 
Expyriment here:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   Windows <Installation.Windows>
   Linux <Installation.Linux>
   Mac OS X <Installation.OSX>
   Android <Installation.Android>


.. _`Python`: http://www.python.org/
.. _Future: https://pypi.python.org/pypi/future
.. _Pygame: http://www.pygame.org/
.. _PyOpenGl: http://www.pyopengl.sourceforge.net
.. _sounddevice: http://python-sounddevice.readthedocs.io/en/0.3.3/
.. _mediadecoder: http://dschreij.github.io/python-mediadecoder/
   
.. _PyParallel: http://pyserial.sourceforge.net
.. _PySerial: http://pyserial.sourceforge.net/pyparallel.html
.. _Numpy: http://numpy.org/
.. _`release page`: https://github.com/expyriment/expyriment/releases
