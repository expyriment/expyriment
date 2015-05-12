Installation
============

How to install Expyriment?
--------------------------

The latest releases of Expyriment can be downloaded from GitHub_. Note, that 
Expyriment depends on the following software packages that have to be installed 
on your system:

* `Python 2`_ (>=2.6)
* Pygame_ (>=1.9)
* PyOpenGL_ (>=3.0)

Additional packages, which are optional and only required for some features of 
Expyriment are:

* NumPy_ (>=1.6) (to use data preprocessing)
* PySerial_ (>=2.5) (to use serial port communication)
* PyParallel_ (>=0.2) (to use parallel port communication on Linux)
* Matplotlib_ (>=1.3), Pillow_ (>=1.0) and Pyxid_ (>=1.0) (for Expyriment plugins)

We provide more detailed platform-specific instructions for installing 
Expyriment here:

.. toctree::
   :maxdepth: 1
   :titlesonly:

   Windows <Installation.Windows>
   Linux <Installation.Linux>
   Mac OS X <Installation.OSX>
   Android <Installation.Android>


.. _`Python 2`: http://www.python.org/
.. _Pygame: http://www.pygame.org/
.. _PyOpenGl: http://www.pyopengl.sourceforge.net
   
.. _PyParallel: http://pyserial.sourceforge.net
.. _PySerial: http://pyserial.sourceforge.net/pyparallel.html
.. _NumPy: http://numpy.org/
.. _Matplotlib: http://matplotlib.org
.. _Pillow: https://pypi.python.org/pypi/Pillow/2.8.1
.. _Pyxid: https://pypi.python.org/pypi/pyxid/1.0
.. _GitHub: https://github.com/expyriment/expyriment/releases
