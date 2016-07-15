Platform-specific instructions: Windows
=======================================

There are two different ways to install Expyriment on Windows. If you need to install
Expyriment on a computer that has no network connection (like lab PCs), please use 
method 2. 


1) Using PYPI (recommended)
---------------------------

1. Install `Python 2.7.11`_ (during installation, also select "Add python.exe to Path"!)

2. Install Pygame_

3. In a command prompt, run::

    python -m pip install --upgrade expyriment

For the additional packages (optional):

4. In a command prompt, run::

      python -m pip install --upgrade 'pyserial>=3,<4'

5. Install Inpout32_ or dlportio_


2) Manually (alternative)
--------------------------

On an PC with internet connection (same OS, architecture and Python version!)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. On the Desktop, create a directory called ``Expyriment_Installation``

2. Download `Python 2.7.11`_ to ``Expyriment_Installation``

3. Download Pygame_ to ``Expyriment_Installation``

4. In a command prompt, run::

    python -m pip download -d %userprofile%/Desktop/Expyriment_Installation expyriment
    
5. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device
    
For the additional packages (optional):

6. Download Inpout32_ or dlportio_ to ``Expyriment_Installation``

7. In a command prompt, run::

    python -m pip download -d %userprofile%/Desktop/Expyriment_Installation 'pyserial>=3,<4'

8. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device


On the target PC
~~~~~~~~~~~~~~~~

1. Copy the directory ``Expyriment_Installation`` from the portable storage device to the Desktop

2. Install ``Expyriment_Installation\python-2.7.11.msi``

3. Install ``Expyriment_Installation\pygame-1.9.1.win32-py2.7.msi``

4. In a command prompt, run::

    python -m pip install --no-index --find-links %userprofile%/Desktop/Expyriment_Installation expyriment

For the additional packages (optional):

a. In a command prompt, run::

    python -m pip install --no-index --find-links %userprofile%/Desktop/Expyriment_Installation 'pyserial>=3,<4'

b. Install Inpout32_ or dlportio_


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

.. _`Python 2.7.11`: https://www.python.org/ftp/python/2.7.11/python-2.7.11.msi
.. _`Python 3.5.2`: https://www.python.org/ftp/python/3.5.2/python-3.5.2.exe
.. _Pygame: http://pygame.org/ftp/pygame-1.9.1.win32-py2.7.msi
.. _PyOpenGL: https://pypi.python.org/packages/any/P/PyOpenGL/PyOpenGL-3.1.0.win32.exe#md5=f175505f4f9e21c8c5c6adc794296d81
.. _Numpy:  http://sourceforge.net/projects/numpy/files/NumPy/1.9.2/numpy-1.9.2-win32-superpack-python2.7.exe
.. _PySerial: http://sourceforge.net/projects/pyserial/files/pyserial/2.7/pyserial-2.7.win32.exe/download
.. _inpout32: http://www.highrez.co.uk/Downloads/InpOut32/
.. _dlportio: http://real.kiev.ua/2010/11/29/dlportio-and-32-bit-windows/
.. _`release page`: http://github.com/expyriment/expyriment/releases/
