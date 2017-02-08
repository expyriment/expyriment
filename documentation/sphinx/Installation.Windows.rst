Platform-specific instructions: Windows
=======================================

Expyriment can be installed for Python 2 or Python 3. In both cases there are
two different ways to install Expyriment. The recommended method requires an
active internet connection. If you need to install Expyriment on a computer that
has no internet connection (like lab PCs), please use the alternative method. 


Python 2
--------

Default installation (online)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install `Python 2.7.13`_ (during installation, also select "Add python.exe to Path"!)

2. In a command prompt, run::

    python -m pip install -U expyriment[all]

   (Omit ``[all]`` to install without additional optional features)

3. To use parallel port communication, install inpout32_ or dlportio_
   (according to the instructions given at each link)


Alternative installation (offline)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**On an PC with internet connection (same OS, architecture and Python version!)**

1. On the Desktop, create a directory called ``Expyriment_Installation``

2. Download `Python 2.7.13`_ to ``Expyriment_Installation``

3. In a command prompt, run::

    python -m pip download -d %userprofile%/Desktop/Expyriment_Installation expyriment[all]
    
   (Omit ``[all]`` to install without additional optional features)

4. To use enhanced video playback, download ffmpeg_ to ``Expyriment_Installation``

5. To use parallel port communication, download inpout32_ or dlportio_ to ``Expyriment_Installation``
   (according to the instructions given at each link)

6. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device


**On the target PC**

1. Copy the directory ``Expyriment_Installation`` from the portable storage device to the Desktop

2. Install ``Expyriment_Installation\python-2.7.13.msi``

3. In a command prompt, run::

    python -m pip install --no-index --find-links %userprofile%/Desktop/Expyriment_Installation -U expyriment[all]
    
   (Omit ``[all]`` to install without additional optional features)

4. To use enhanced video playback, unzip ``Expyriment_Installation\ffmpeg-20160803-d3426fb-win32-static.zip`` and copy the
   file ``bin\ffmpeg.exe`` to a directory on the local hard drive (e.g. ``C:\ffmpeg\bin\``) and
   `add it to the environment variable PATH`_!)

5. To use parallel port communication, install the downloaded inpout32_ or dlportio_
   (according to the instructions given at each link)


Python 3
--------

Default installation (online)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install `Python 3.6.0`_ (during installation, also select "Add python.exe to Path"!)

2. In a command prompt, run::

    python3 -m pip install -U expyriment[all]
    
   (Omit ``[all]`` to install without additional optional features)

3. To use parallel port communication, install inpout32_ or dlportio_
   (according to the instructions given at each link)


Alternative installation (offline)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**On an PC with internet connection (same OS, architecture and Python version!)**

1. On the Desktop, create a directory called ``Expyriment_Installation``

2. Download `Python 3.6.0`_ to ``Expyriment_Installation``

3. In a command prompt, run::

    python3 -m pip download -d %userprofile%/Desktop/Expyriment_Installation expyriment[all]

   (Omit ``[all]`` to install without additional optional features)
   
4. To use enhanced video playback, download ffmpeg_ to ``Expyriment_Installation``

5. To use parallel port communication, download inpout32_ or dlportio_ to ``Expyriment_Installation``
   (according to the instructions given at each link)

6. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device


**On the target PC**

1. Copy the directory ``Expyriment_Installation`` from the portable storage device to the Desktop

2. Install ``Expyriment_Installation\python-3.6.0.exe``

3. In a command prompt, run::

    python3 -m pip install --no-index --find-links %userprofile%/Desktop/Expyriment_Installation --upgrade expyriment[all]

   (Omit ``[all]`` to install without additional optional features)
   
4. To use enhanced video playback, unzip ``Expyriment_Installation\ffmpeg-20160803-d3426fb-win32-static.zip`` and copy the
   file ``bin\ffmpeg.exe`` to a directory on the local hard drive (e.g. ``C:\ffmpeg\bin\``) and
   `add it to the environment variable PATH`_!)

5. To use parallel port communication, install inpout32_ or dlportio_
   (according to the instructions given at each link)


Notes
-----

**Make sure python.exe is in your Path**

    If you get an an error that `'python' is not recognized as an internal or
    external command, operable program or batch file`, Windows does not know
    where to find the Python interpreter. To fix this, find the directory that
    includes ``python.exe`` and `add it to the environment variable PATH`_.

**Do not start your experiments out of IDLE when testing participants**

    If you are using the IDLE editor that comes with the Python installation, 
    be aware that IDLE itself is written in Python. Starting your Expyriment 
    programme out of IDLE (by clicking on "Run" or by pressing F5), might thus 
    lead to improper timing!

    We therefore strongly suggest to run Expyriment programmes from the command 
    line when testing participants.

.. _`Python 2.7.13`: https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi
.. _`Python 3.6.0`: https://www.python.org/ftp/python/3.6.0/python-3.6.0.exe
.. _PyOpenGL: https://pypi.python.org/packages/any/P/PyOpenGL/PyOpenGL-3.1.0.win32.exe#md5=f175505f4f9e21c8c5c6adc794296d81
.. _Numpy:  http://sourceforge.net/projects/numpy/files/NumPy/1.9.2/numpy-1.9.2-win32-superpack-python2.7.exe
.. _PySerial: http://sourceforge.net/projects/pyserial/files/pyserial/2.7/pyserial-2.7.win32.exe/download
.. _inpout32: http://www.highrez.co.uk/Downloads/InpOut32/
.. _dlportio: http://real.kiev.ua/2010/11/29/dlportio-and-32-bit-windows/
.. _ffmpeg: https://ffmpeg.zeranoe.com/builds/win32/static/ffmpeg-20160803-d3426fb-win32-static.zip
.. _`add it to the environment variable PATH`: http://www.computerhope.com/issues/ch000549.htm
.. _`release page`: http://github.com/expyriment/expyriment/releases/
