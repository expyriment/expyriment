Installation
============

How to install Expyriment?
--------------------------

The latest release of Expyriment can be found at the `release page`_. Note, that
Expyriment depends on the following software packages that have to be installed 
on your system:

* `Python`_ (2.7 or 3.5)
* Pygame_ (>=1.9)
* PyOpenGL_ (>=3.0)
* NumPy_ (>=1.6)
* sounddevice_ (>=0.3)
* mediadecoder_ (>=0.1)

Additional packages, which are optional and only required for some features of 
Expyriment are:

* PySerial_ (>=3.0) (to use serial port communication)
* PyParallel_ (>=0.2) (to use parallel port communication on Linux)
* Inpout32_ or dlportio_ (to use parallel port communication on Windows)

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
.. _Pygame: http://www.pygame.org/
.. _PyOpenGl: http://www.pyopengl.sourceforge.net
.. _sounddevice: http://python-sounddevice.readthedocs.io/en/0.3.3/
.. _mediadecoder: http://dschreij.github.io/python-mediadecoder/
   
.. _PyParallel: http://pyserial.sourceforge.net
.. _PySerial: http://pyserial.sourceforge.net/pyparallel.html
.. _Numpy: http://numpy.org/
.. _inpout32: http://www.highrez.co.uk/Downloads/InpOut32/
.. _dlportio: http://real.kiev.ua/2010/11/29/dlportio-and-32-bit-windows/
.. _`release page`: https://github.com/expyriment/expyriment/releases
