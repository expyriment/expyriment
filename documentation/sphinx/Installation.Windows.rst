Platform-specific instructions: Windows
=======================================

There are two different ways to install Expyriment. The recommended method
requires an active internet connection. If you need to install Expyriment on
a computer that has no internet connection (like lab PCs), please use the
alternative method. 


Default installation (online)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install `Python 3.12.1`_ (during installation, also select "Install launcher [...]"!)

2. In a command prompt, run::

    py -3 -m pip install -U expyriment[all]
    
   (Omit ``[all]`` to install without additional optional features)

3. To use parallel port communication, install inpout32_ or dlportio_
   (according to the instructions given at each link)


Alternative installation (offline)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**On an PC with internet connection (same OS, architecture and Python version!)**

1. On the Desktop, create a directory called ``Expyriment_Installation``

2. Download `Python 3.12.1`_ to ``Expyriment_Installation``

3. In a command prompt, run::

    py -3 -m pip download -d %userprofile%/Desktop/Expyriment_Installation expyriment[all]

   (Omit ``[all]`` to install without additional optional features)
   
4. To use enhanced video playback, download ffmpeg_ to ``Expyriment_Installation``

5. To use parallel port communication, download inpout32_ or dlportio_ to ``Expyriment_Installation``
   (according to the instructions given at each link)

6. Copy the directory ``Expyriment_Installation`` from the Desktop to a portable storage device


**On the target PC**

1. Copy the directory ``Expyriment_Installation`` from the portable storage device to the Desktop

2. Install ``Expyriment_Installation\python-3.12.1-amd64.exe``

3. In a command prompt, run::

    py -3 -m pip install --no-index --find-links %userprofile%/Desktop/Expyriment_Installation --upgrade expyriment[all]

   (Omit ``[all]`` to install without additional optional features)
   
4. To use enhanced video playback, unzip ``Expyriment_Installation\ffmpeg-latest-win32-static.zip`` and copy the
   file ``bin\ffmpeg.exe`` to a directory on the local hard drive (e.g. ``C:\ffmpeg\bin\``) and
   `add it to the environment variable PATH`_!)

5. To use parallel port communication, install inpout32_ or dlportio_
   (according to the instructions given at each link)


Notes
-----

**Do not start your experiments out of IDLE when testing participants**

    If you are using the IDLE editor that comes with the Python installation, 
    be aware that IDLE itself is written in Python. Starting your Expyriment 
    programme out of IDLE (by clicking on "Run" or by pressing F5), might thus 
    lead to improper timing!

    We therefore strongly suggest to run Expyriment programmes from the command 
    line when testing participants.

.. _`Python 3.12.1`: https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe
.. _inpout32: https://www.highrez.co.uk/Downloads/InpOut32/
.. _dlportio: https://real.kiev.ua/2010/11/29/dlportio-and-32-bit-windows/
.. _ffmpeg: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
.. _`add it to the environment variable PATH`: https://www.computerhope.com/issues/ch000549.htm
.. _`release page`: https://github.com/expyriment/expyriment/releases/
