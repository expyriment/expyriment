Currently known problems and limitations
========================================

Here are some current problems and limitations of Expyriment you should be 
aware of. Where possible, we include suggestions on how to deal with or work 
around the issue.

No native 3D stimuli
--------------------
Right now Expyriment only offers static 2D visual stimuli.

While PyOpenGL can be used directly to create dynamic 3D stimuli, we are 
planning to add a dedicated 3D stimulus class in the future, to facilitate the 
creation of 3D stimuli.

Inaccurate visual stimulus timing on MacOS
------------------------------------------
It appears that MacOS uses a compositor in combination with an adaptive vsync
behaviour, over which Expyriment has no control. This makes it currently not
possible to block on the vertical retrace, which is crucial for accurate timing
(see :doc:`Timing`). While MacOS can still be used to create experiments, we
however don't recommend to use it for participant testing!
