Installation
============

How to install Expyriment?
--------------------------

Expyriment works with all current `Python`_ versions (2.7 or 3.5).
The latest release of Expyriment can be found at the `release page`_. Note, that
Expyriment depends on the following Python packages that have to be installed 
on your system:

* Future_ (>=0.15)
* Pygame_ (>=1.9)
* PyOpenGL_ (>=3.0)

Additional packages, which are optional and only required for some features of 
Expyriment are:

* NumPy_ (>=1.6)
* sounddevice_ (>=0.3)
* mediadecoder_ (>=0.1)
* PySerial_ (>=3.0) (to use serial port communication)
* PyParallel_ (>=0.2) (to use parallel port communication)

Please be aware that Expyriment plugins (extras) might have additional dependencies.

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
