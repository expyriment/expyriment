Currently known problems and limitations
========================================

Here are some current problems and limitations of Expyriment you should be 
aware of. Where possible, we include suggestions on how to deal with or work 
around the issue.

MPEG-1 video playback only
--------------------------
At the moment, only MPEG-1 video files can be played back.

This is a limitation of the underlying video system of Pygame. On the long run, 
we are planning to move to a different Python video package.

No native 3D stimuli
--------------------
Right now Expyriment only offers static 2D visual stimuli.

While PyOpenGL can be used direclty to create dynamic 3D stimuli, we are 
planning to add a dedicated 3D stimulus class in the future, to facilitate the 
creation of 3D stimuli.

No support for multiple monitors
--------------------------------
It is not possible to run Expyriment in fullscreen mode on a specific monitor,
since the underlying Pygame package is not aware of multiple monitors.

If the additional monitors are set to extend the desktop, then Expyriment will
treat everything as one big display (spanned over all monitors).

If you simply want to run an experiment on a different monitor (e.g. an external
monitor on a laptop), we suggest to set the additional monitor to clone the primary one.
