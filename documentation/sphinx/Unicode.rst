Using non-English characters
============================
Expyriment has full `unicode support <http://docs.python.org/2/howto/unicode.html>`_.
This means that, in principle, non-English characters (such as umlaut, accent,
special character) can be used in strings throughout the library. Two
different forms of using non-English characters have to be dissociated.

Non-English characters in strings in the Expyriment script file
---------------------------------------------------------------
When attempting to use non-English characters in strings in your Expyriment
script file, the following three conditions have to be met:

1. **Only use non-English charactes in unicode strings (Python 2 only)!**
   For example: Use ``u"Überexperiment"`` instead of ``"Überexperiment"``.
   (In Python 3 you can use normal strings, as they are already unicode compatible.)

2. **Know the encoding used by your editor!**
   For example: IDLE will automatically suggest to save in utf-8 encoding when
   non-English characters are found in the script file. We suggest to always save in utf-8.

3. **Define the encoding in your Expyriment script file!**
   In one of the first two lines in the file the encoding has to be specified
   For example::

     # -*- coding: utf-8 -*-

Non-English characters in other text files (e.g. stimuli lists)
---------------------------------------------------------------
When an Expyriment method saves a text file, it will always automatically add a
header line specifying the encoding with which the file was saved. Which
encoding this is depends on the system Expyriment is running on (it uses the
default encoding defined by the locale settings).

When an Expyriment method reads in a text file, it will always read the header
line first and decode the text automatically (into unicode strings). If no such
header is found, the encoding set by the system locale will be used (and if
this fails, utf-8).
