"""
Default settings for the control package. ::

    audiosystem_autostart : bool
        start the audiosystem when Expyriment is initialised

    audiosystem_bit_depth : int
        8   = 8 bit unsigned integer (8-bit audio)
        -8  = 8 bit signed integer (uncommon)
        16  = 16 bit unsigned integer (uncommon)
        -16 = 16 bit signed integer (16-bit audio)
        32  = 32 bit floating point (32-bit float audio)

    audiosystem_buffer_size: int
        the audio buffer size in samples

        NOTE
        ====
        Smaller buffer sizes reduce the delay in audio playback, but a too
        small buffer size might result in distorted audio. The optimal buffer
        size is the smallest one that does not distort the audio, and can
        differ between systems.

    audiosystem_channels : int
        the number of audio channels

    audiosystem_device : str
        the name of the audio device to use

    audiosystem_sample_rate : int
        the audio sample rate

    auto_create_subject_id : bool
        create a subject id automatically when starting an experiment

    display : int
        the display index to show the screen on

    display_resolution : (int, int) or None
        the resolution of the display the screen is shown on

        NOTES
        =====
        When set to None, Expyriment will attempt to set the resolution to the
        highest available resolution for that display.

    event_logging : int or bool
        O/False = no event logging
        1/True  = normal event logging (logging of all input & output events)
        2       = intensive logging; logs much more; use only for debugging
                  purposes

        NOTES
        =====
        In most cases, it should be avoided to switch of logging (loglevel=0).
        If log files become to big due to certain repetitive events, it is
        suggested to switch of the logging of individual stimuli or IO event
        (see the method .set_logging() of this object).
        The logging of all events can also be changed via
        expyriment.design.Experiment().set_logging.

    fast_quit : bool
        quit immediately without showing a goodbye message

    goodbye_delay : int
        duration (in milliseconds) to show the goodbye text

    goodbye_text : str
        the text to be shown when ending an experiment

    initialise_delay : int
        a delay (in seconds) to wait before running an experiment to give
        Python time to start properly

        NOTES
        =====
        Python needs about 10 seconds to start up properly. Before that,
        timing accuracy can be worse.

    opengl : int or bool
        0/False = no OpenGL (no vsync / no blocking)
        1       = OpenGL (vsync / no blocking)
        2/True  = OpenGL (vsync / blocking)

        NOTES
        =====
        no OpenGL (no vsync / no blocking)
        ----------------------------------
        * Short preloading times
            Pygame is used to write directly to the display
        * Unsynchronized display updating
            Pixels are starting to change at wherever the vertical retrace is
            at the moment of presentation

        This mode can be useful for dynamic displays, where an accurate
        stimulus timing is not required, but rather very fast display changes
        have high priority and stimuli have to be created and on the fly (e.g.
        questionnaires, video game-like scenarios).

        OpenGL (vsync / no blocking)
        ----------------------------
        * Longer preloading times
            OpenGL is used to write to the display and a conversion to an
            OpenGL texture is needed
        * Synchronized display updating
            Pixels are starting to change always when the vertical retrace is
            at the left top corner
        * Inaccurate presentation time reporting
            Exact time of pixels changing on screen is not known

        This mode can be useful for dynamic displays, where an accurate
        stimulus timing is not required, but rather fast and fluid (e.g.
        non-tearing) display changes have high priority and preloaded stimuli
        can be used (e.g. well-controlled motion stimuli).

        OpenGL (vsync / blocking)
        -------------------------
        * Longer preloading times
            OpenGL is used to write to the display and a conversion to an
            OpenGL texture is needed
        * Synchronized display updating
            Pixels are starting to change always when the vertical retrace is
            at the left top corner
        * Accurate presentation time reporting
            present() method will only return when all drawing has been
            finished and the then empty back buffer is available for drawing
            on it again

        This can be useful for static stimulus presentation, where getting an
        accurate  presentation time report is of highest priority. Since this
        will be the case for most psychological and neuroscientific settings,
        it is the default mode used by Expyriment.

    quit_key : int
        the key to be used for ending an experiment

    refresh_key : int
        the key to be used for refreshing the screen

    stdout_logging: bool
        log errors and warnings which go to the standard output (terminal
        window)

    window_mode : bool
        run experiment in window instead of fullscreen

    window_size : (int, int)
        the size of the window when running in window mode

    window_no_frame : bool
        if True windows in window mode will be displayed without a frame;
        this parameter does not affect fullscreen mode

"""

__author__ = 'Florian Krause <florian@expyriment.org, \
Oliver Lindemann <oliver@expyriment.org>'


from ..misc import constants as _constants

initialise_delay = 10  # After approximately 10 seconds Python is timecritical
auto_create_subject_id = False
goodbye_text = "Ending experiment..."
goodbye_delay = 3000
fast_quit = False
quit_key = _constants.K_ESCAPE

display = 0
display_resolution = None
opengl = 2
window_mode = False
window_size = (800, 600)
window_no_frame = False

event_logging = 1  # 1 = default, 2 = extensive, 0 or False = off
stdout_logging = True

audiosystem_autostart = True
audiosystem_sample_rate = 44100
audiosystem_bit_depth = -16  # Negative values mean signed sample values
audiosystem_channels = 2
audiosystem_buffer_size = 512
audiosystem_device = None

_mode_settings = None

