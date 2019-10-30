Presenting videos in Expyriment
===============================

Video formats
-------------
Since version 0.9.0 Expyriment uses FFMPEG (https://www.ffmpeg.org) by default to decode video files (the ``mediadecoder`` backend) if enhanced video playback support has been installed (see :doc:`Installation`). This means that a large variety of video formats are automatically supported.

The old video backend is still available as ``pygame``, and only plays MPEG1 videos with MP3 audio.
If you have to use the old backend, you can encode any video into this correct format using FFMPEG directly::

    ffmpeg -i <inputfile> -vcodec mpeg1video -acodec libmp3lame -intra -qscale 2  <outputfile.mpg>

The ``-qscale`` option is the quality setting. It can take values from 1 to 31. 1 is the best quality, but big file size. 31 is the worst quality, but small file size. Play around with this setting to get a good balance between quality and file size.

Usage
-----

1. Create a video object::

    my_video = expyriment.stimuli.Video("filename")

2. If the video has sound, then the audio system has to be stopped (temporarily), such that the video system can play sound)::

    expyriment.control.stop_audiosystem()

3. Preload the video into memory, before playing it back::

    my_video.preload()

4. To actually present the video on screen, understanding the various methods of the video object is crucial:

   ``play()``
       will simply start video (and audio) playback in the background. This has no effect on the screen, no frames from the video are presented automatically.

   ``present()``
        waits for a new frame, then presents this frame on the screen. The method blocks until the new frame has been presented on the screen (if in OpenGL mode).

   ``update()``
        presents the currently available frame immediately (i.e. without waiting for a new one). The methods blocks until the currently available frame has been presented on the screen (if in OpenGL mode).

   ``wait_end()``
        continuously presents frames until the last frame of the video is reached. Dropped frames will be reported (in the terminal as well as in the event file). The keyboard is monitored during this, such that hitting ESC will pause playback, and then choosing "n" will resume it (while choosing "y" will quit of course).

   ``wait_frame()``
        behaves like ``wait_end()``, with the difference that it waits until frame number `frame` instead of the last frame.

   The perhaps most common situation is thus to use a combination of ``play()``, ``present()`` and ``wait_end()``.
   
5. When done, delete the video stimulus::

    del my_video


Example
-------

Simple example::

    import expyriment as xpy

    exp = xpy.control.initialize()
    v = xpy.stimuli.Video("file.mpg")
    v.preload()

    v.play()
    v.present()
    video_presentation_time = exp.clock.time
    v.wait_end()
    v.stop()


If key presses (other than the control keys) need to be checked during the video playback::

    import expyriment as xpy

    exp = xpy.control.initialize()
    v = xpy.stimuli.Video("file.mpg")
    v.preload()

    v.play()
    v.present()
    video_presentation_time = exp.clock.time
    while v.is_playing:
        while not v.new_frame_available:
            key = exp.keyboard.check(xpy.misc.constants.K_SPACE)
            if key is not None:
                key_pressed = True
        v.update()
    v.stop()
    
**NOTE**: Do not infer reaction times from this!
