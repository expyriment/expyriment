Using non-English characters
============================
Expyriment has full unicode support. This means that, in principle, non-English
characters can be used in strings throughout the library. Two different forms
of using non-English characters have to be dissociated::

1. Non-English characters in strings in the Expyriment script file
------------------------------------------------------------------
When attempting to use non-English characters in strings in your Expyriment
script file, the following three conditions have to be met:

a. Only use non-English charactes in unicode strings!
   
   For example: Use u"hello" instead of "hello".

b. Know the encoding with which your editor will save the script file!
   
   For example: IDLE will automatically suggest to save in utf-8 encoding when
   non-English characters are found in the script file.

c. Define the encoding with which the file will saved in one of the first two
   lines with::
     # -*- coding: <encoding> -*-
  where <encoding> is the encoding used!
  
  For example:::
   # -*- coding: utf-8 -*-

2. Non-English characters in other text files (e.g. stimuli lists)
------------------------------------------------------------------
When an Expyriment method saves a text file, it will always automatically add a
header line specifying the encoding with which the file was saved. Which
encoding this is depends on the system Expyriment is running on (it uses the
default encoding defined by the locale settings).

When an Expyriment method reads in a text file, it will always read the header
line first and decode the text automatically (into unicode strings). If no such
header is found, the encoding set by the system locale will be used (and if
this fails, utf-8).
