Platform-specific instructions: Windows
=======================================

There are two different ways to install Expyriment on Windows. If you need to install
Expyriment on a computer that has no network connection (like lab PCs), please use 
method 2. 


1) Using PyPi (recommended)
---------------------------

1. Install `Python 2.7.10`_ (during installation, also select "Add python.exe to Path"!)
2. Install Pygame_
3. In a command prompt, run ::

    python -m pip install --upgrade pip
    python -m pip install --upgrade expyriment

For the additional packages (optional):

4. Install NumPy_
5. In a command prompt, run ::

      python -m pip install pyserial

6. Install Inpout32_ or dlportio_


2) Manually (alternative)
--------------------------

1. Install `Python 2.7.10`_
2. Install Pygame_
3. Install PyOpenGL_
4. Download |expyriment-wheel-code| from the `release page`_ and install it in a command prompt with

   .. parsed-literal::

       python -m pip install |expyriment-wheel|

For the additional packages (optional):

5. Install Numpy_
6. Install PySerial_
7. Install Inpout32_ or dlportio_


Notes
-----

**Make sure python.exe is in your Path**
    If you get an an error that `'python' is not recognized as an internal or
    external command, operable program or batch file`, Windows does not know
    where to find the Python interpreter. To fix this, add python.exe to the
    Path, as described `here <https://docs.python.org/2/using/windows.html#setting-envvars>`_.

**Do not start your experiments out of IDLE when testing participants**

    If you are using the IDLE editor that comes with the Python installation, 
    be aware that IDLE itself is written in Python. Starting your Expyriment 
    programme out of IDLE (by clicking on "Run" or by pressing F5), might thus 
    lead to improper timing!

    We therefore strongly suggest to run Expyriment programmes from the command 
    line when testing participants.

.. _`Python 2.7.10`: https://www.python.org/ftp/python/2.7.10/python-2.7.10.msi
.. _Pygame: http://pygame.org/ftp/pygame-1.9.1.win32-py2.7.msi
.. _PyOpenGL: https://pypi.python.org/packages/any/P/PyOpenGL/PyOpenGL-3.1.0.win32.exe#md5=f175505f4f9e21c8c5c6adc794296d81
.. _Numpy:  http://sourceforge.net/projects/numpy/files/NumPy/1.9.2/numpy-1.9.2-win32-superpack-python2.7.exe
.. _PySerial: http://sourceforge.net/projects/pyserial/files/pyserial/2.7/pyserial-2.7.win32.exe/download
.. _inpout32: http://www.highrez.co.uk/Downloads/InpOut32/
.. _dlportio: http://real.kiev.ua/2010/11/29/dlportio-and-32-bit-windows/
.. _`release page`: http://github.com/expyriment/expyriment/releases/
