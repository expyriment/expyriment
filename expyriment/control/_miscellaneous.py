"""
The control._miscellaneous module of expyriment.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import sys
import pygame

import defaults
import expyriment
from expyriment.control import defaults as control_defaults


def start_audiosystem():
    """Start the audio system."""

    pygame.mixer.init()

def stop_audiosystem():
    """Stop the audio system."""

    pygame.mixer.quit()

def get_audiosystem_is_playing(channel=None):
    """Check if the audiosystem is busy playing sounds.

    Parameters
    ----------
    channel : pygame.mixer.Channel, optional
        specific channel to check

    Returns
    -------
    out : bool
        Returns True if any sound is playing.

    """

    if channel is None:
        rtn = pygame.mixer.get_busy()
    else:
        rtn = channel.get_busy()
    if rtn == 0:
        rtn = False
    elif rtn > 0:
        rtn = True
    return rtn

def wait_end_audiosystem(channel=None):
    """Wait until audiosystem has ended playing sounds.

    Blocks until the audiosystem is not busy anymore and only returns then.

    Parameters
    ----------
    channel : pygame.mixer.Channel, optional
        specific channel to wait for end of playing

    """

    while get_audiosystem_is_playing(channel):
            for event in pygame.event.get(pygame.KEYDOWN):
                if event.type == pygame.KEYDOWN and (\
                   event.key == control_defaults.quit_key or \
                   event.key == control_defaults.pause_key):
                    if channel is None:
                        pygame.mixer.stop()
                    else:
                        channel.stop()
                    expyriment.io.Keyboard.process_control_keys(event)

def set_develop_mode(onoff, intensive_logging=False):
    """Set defaults for a more convenient develop mode.

    Notes
    -----
    The function set the following global variables

    >>> expyriment.control.defaults.initialize_delay = 0
    >>> expyriment.control.defaults.window_mode = True
    >>> expyriment.control.defaults.fast_quit = True
    >>> exypriment.control.defaults.auto_create_subject_id = True
    >>> expyriment.io.defaults.outputfile_time_stamp = False

    Parameters
    ----------
    onoff : bool
        set develop_mode on (True) or off (False)
    intensive_logging : bool, optional
        True sets expyriment.io.defaults.event_logging=2
        (default = False)

"""

    if onoff:
        defaults._mode_settings = [defaults.initialize_delay,
                                   defaults.window_mode,
                                   defaults.fast_quit,
                                   expyriment.io.defaults.outputfile_time_stamp,
                                   defaults.auto_create_subject_id]

        print "*** DEVELOP MODE ***"
        defaults.initialize_delay = 0
        defaults.window_mode = True
        defaults.fast_quit = True
        expyriment.io.defaults.outputfile_time_stamp = False
        defaults.auto_create_subject_id = True
    else:
        print "*** NORMAL MODE ***"
        if defaults._mode_settings is not None:
            defaults.initialize_delay = defaults._mode_settings[0]
            defaults.window_mode = defaults._mode_settings[1]
            defaults.fast_quit = defaults._mode_settings[2]
            expyriment.io.defaults.outputfile_time_stamp = \
                    defaults._mode_settings[3]
            defaults.auto_create_subject_id = defaults._mode_settings[4]
            defaults._mode_settings = None

        else:
            pass # Nothing to do

    if intensive_logging:
        expyriment.control.defaults.event_logging = 2

def _get_module_values(goal_dict, module):
    value = None
    for var in dir(module):
        if not var.startswith("_"):
            exec("value = {0}.{1}".format(module.__name__, var))
            goal_dict["{0}.{1}".format(module.__name__, var)] = value
    return goal_dict

def get_defaults(search_str="", as_string=False):
    """Return a dictionary with all default values in the current Expyriment
    environment. The keys represent the variables names.

    Parameters
    ----------
    search_str : str, optional
        search for a specific expression
    as_string : bool, optional
        print as string instead of dict

    """

    defaults = {}
    defaults = _get_module_values(defaults, expyriment.design.defaults)
    defaults = _get_module_values(defaults, expyriment.control.defaults)
    defaults = _get_module_values(defaults, expyriment.stimuli.defaults)
    defaults = _get_module_values(defaults, expyriment.io.defaults)
    defaults = _get_module_values(defaults, expyriment.misc.defaults)
    defaults = _get_module_values(defaults, expyriment.design.extras.defaults)
    defaults = _get_module_values(defaults, expyriment.stimuli.extras.defaults)
    defaults = _get_module_values(defaults, expyriment.io.extras.defaults)
    defaults = _get_module_values(defaults, expyriment.misc.extras.defaults)
    if len(search_str) >= 0:
        tmp = {}
        for key in defaults.keys():
            if key.lower().find(search_str.lower()) >= 0:
                tmp[key] = defaults[key]
        defaults = tmp
    if as_string:
        sorted_keys = defaults.keys()
        sorted_keys.sort()
        rtn = ""
        for key in sorted_keys:
            tabs = "\t" * (4 - int((len(key) + 1) / 8))
            rtn += key + ":" + tabs + repr(defaults[key]) + "\n"
    else:
        rtn = defaults

    return rtn

def register_wait_callback_function(function, exp=None):
    """Register a wait callback function.

    The registered wait callback function will be repetitively executed in
    all Expyriment wait and event loops that wait for an external input.
    That is, they are executed by the following functions (at least once!):

        control.wait_end_audiosystem,
        misc.clock.wait,         misc.clock.wait_seconds,
        misc.clock.wait_minutes  io.keyboard.wait,
        io.keyboard.wait_char,   io.buttonbox.wait,
        io.gamepad.wait_press,   io.triggerinput.wait,
        io.mouse.wait_press,     io.serialport.read_line,
        io.textinput.get,        stimulus.video.wait_frame,
        stimulus.video.wait_end

    Parameters
    ----------
    function : function
        the wait function
    exp : design.Experiment, optional
        specific experiment for which to register wait function

    Notes
    -----
    CAUTION! If wait callback function takes longer than 1 ms to process,
    Expyriment timing will be affected!

    """

    if exp is not None:
        exp.register_wait_callback_function(function)
    else:
        expyriment._active_exp.register_wait_callback_function(function)

def unregister_wait_callback_function(exp=None):
    """Unregister wait function.

    Parameters
    ----------
    exp : design.Experiment, optional
        specific experiment for which to unregister wait function

    """

    if exp is not None:
        exp.unregister_wait_callback_function()
    else:
        expyriment._active_exp.unregister_wait_callback_function()

def is_ipython_running():
    """Return True if IPython is running."""

    try:
        __IPYTHON__
        return True
    except NameError:
        return False

def is_idle_running():
    """Return True if IDLE is running."""

    import sys
    return "idlelib.run" in sys.modules

def _set_stdout_logging(event_file):
    """Set logging of stdout and stderr to event file.

    Note that if the script is called via IPython or IDLE logging will not
    work.

    Parameters
    ----------
    event_file : io.EventFile
        the event file

    """

    class Logger(object):
        def __init__(self, event_file, log_tag):
            self.terminal = sys.stdout
            self.event_file = event_file
            self.tag = log_tag
            self._buffer = []

        def write(self, message):
            self.terminal.write(message)
            self._buffer.append(message)
            if message.endswith("\n"):
                tmp = "".join(self._buffer).strip("\n")
                self.event_file.log("{0},received,{1}".format(self.tag,
                                                              repr(tmp)))
                self._buffer = []


    if is_ipython_running():
        print "Standard output and error logging is switched off under IPython."
    elif is_idle_running():
        print "Standard output and error logging is switched off under IDLE."
    else:
        sys.stderr = Logger(event_file, "stderr")
        sys.stdout = Logger(event_file, "stdout")
