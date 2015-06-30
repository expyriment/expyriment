Presenting videos in Expyriment
===============================

Video formats
-------------
Expyriment only plays MPEG1 videos with MP3 audio right now (and unfortunately, the Pygame backend that is responsible for video playback seems to be very picky on the details of this).
To encode any video into the correct format, use ffmpeg (https://www.ffmpeg.org) and convert in the following way::

    ffmpeg -i <inputfile> -vcodec mpeg1video -acodec libmp3lame -intra -qscale 2  <outputfile.mpg>

The -qscale option is the quality setting. It can take values from 1 to 31. 1 is the best quality, but big file size. 31 is the worst quality, but small file size. Play around with this setting to get a good balance between quality and file size.

Usage
-----

1. Create a video object::

    my_video = expyriment.stimuli.Video("filename")

2. If the video has sound, then the audio system has to be stopped (temporarily), such that the video system can play sound)::

    expyriment.control.stop_audiosystem()

3. Preload the video into memory, before playing it back::

    my_video.preload()

4. To actually present the video on screen, understanding the various methods of the video object is crucial:

    - **play()** will simply start video playback in the background. This has no effect on the screen, no frames from the video are presented automatically. Use this, if you want to get each frame from the video manually and present them at your liking (using the update() method, see below).

    - **present()** will do a bit more. It will start video playback and it will present the very first frame of the video onto the screen for you. Just like present method of other visual stimuli in Expyriment, the method will only return, once the stimulus (in that case the first video frame) has actually been presented on the screen, giving you important information about when the participants are actually starting to see your video.

    - **update()** will take the current frame (from a playing video) and present it to the screen. As with present(), the method blocks until the frame is actually visible on the screen.

    - **wait_end()** will basically do, what update does, but continuously, for each frame, until the end of the video.

    - **wait_frame()** is the same as wait_end, but up to a specified frame only, instead until the end of the video.

    The perhaps most common situation is thus to use a combination of present() and wait_end().

Example
-------
The following example shows how to present a video from start to end::

    from expyriment import control, stimuli

    video = stimuli.Video("file")  # Create video object

    expyriment.control.stop_audiosystem()  # Stop audio system

    v.preload()  # Preload video
    v.present()  # Start video playback and present first frame
    v.wait_end() # Continuously present the next frame until video stops

