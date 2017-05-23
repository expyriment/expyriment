"""
The control._miscellaneous module of expyriment.

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import sys
from types import FunctionType

import pygame

from . import defaults
from .. import _internals
from .._internals import CallbackQuitEvent
from ..misc import is_idle_running, is_ipython_running


def start_audiosystem():
    """Start the audio system.

    Notes
    ------
    The audiosystem is automatically started when initializing an
    Experiment!

    """

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


def wait_end_audiosystem(channel=None, callback_function=None,
                         process_control_events=True):
    """Wait until audiosystem has ended playing sounds.

    Blocks until the audiosystem is not busy anymore and only returns then.

    Parameters
    ----------
    channel : pygame.mixer.Channel, optional
        specific channel to wait for end of playing
    callback_function : function, optional
        function to repeatedly execute during waiting loop
    process_control_events : bool, optional
        process ``io.Keyboard.process_control_keys()`` and
        ``io.Mouse.process_quit_event()`` (default = True)

    Notes
    ------
    This will also by default process control events (quit and pause).
    Thus, keyboard events will be cleared from the cue and cannot be
    received by a Keyboard().check() anymore!

    """

    from .. import io
    while get_audiosystem_is_playing(channel):
        if _internals.skip_wait_methods:
            break
        if isinstance(callback_function, FunctionType):
            rtn_callback = callback_function()
            if isinstance(rtn_callback, CallbackQuitEvent):
                if channel is None:
                    pygame.mixer.stop()
                else:
                    channel.stop()
                return rtn_callback
        if _internals.active_exp is not None and \
           _internals.active_exp.is_initialized:
            rtn_callback = _internals.active_exp._execute_wait_callback()
            if isinstance(rtn_callback, CallbackQuitEvent):
                if channel is None:
                    pygame.mixer.stop()
                else:
                    channel.stop()
                return rtn_callback
            if process_control_events:
                if _internals.active_exp.mouse.process_quit_event() or \
                   _internals.active_exp.keyboard.process_control_keys():
                    if channel is None:
                        pygame.mixer.stop()
                    else:
                        channel.stop()
                    break
            else:
                pygame.event.pump()


def set_skip_wait_methods(on=True):
    """Skip all wait methods.

    Parameters
    ----------
    on : bool, optional
        If True, all wait methods in the experiment (i.e. all wait functions
        in ``expyriment.io`` and the clock) will be ommited (default = True)

    """

    if on:
        _internals.skip_wait_methods = True
    else:
        _internals.skip_wait_methods = False


def set_develop_mode(on=True, intensive_logging=False, skip_wait_methods=False):
    """Set defaults for a more convenient develop mode.

    Notes
    -----
    The function set the following global variables

    >>> expyriment.control.defaults.initialize_delay = 0
    >>> expyriment.control.defaults.window_mode = True
    >>> expyriment.control.defaults.no_frame_windows = False
    >>> expyriment.control.defaults.fast_quit = True
    >>> expyriment.control.defaults.auto_create_subject_id = True
    >>> expyriment.io.defaults.outputfile_time_stamp = False

    Parameters
    ----------
    on : bool, optional
        set develop_mode on (True) or off (False)
    intensive_logging : bool, optional
        True sets expyriment.io.defaults.event_logging=2
        (default = False)
    skip_wait_methods : bool, optional
        If True, all wait functions in the experiment (i.e. all wait functions
        in ``expyriment.io`` and the clock) will be ommited (default = False)

    """

    from .. import io
    if on:
        defaults._mode_settings = [defaults.initialize_delay,
                                   defaults.window_mode,
                                   defaults.fast_quit,
                                   io.defaults.outputfile_time_stamp,
                                   defaults.auto_create_subject_id]
        if intensive_logging:
                defaults._mode_settings.append(defaults.event_logging)
                defaults.event_logging = 2
        if skip_wait_methods:
            set_skip_wait_methods(True)
        print("*** DEVELOP MODE ***")
        defaults.initialize_delay = 0
        defaults.window_mode = True
        defaults.no_frame_windows = False
        defaults.fast_quit = True
        io.defaults.outputfile_time_stamp = False
        defaults.auto_create_subject_id = True
    else:
        print("*** NORMAL MODE ***")
        if defaults._mode_settings is not None:
            defaults.initialize_delay = defaults._mode_settings[0]
            defaults.window_mode = defaults._mode_settings[1]
            defaults.fast_quit = defaults._mode_settings[2]
            io.defaults.outputfile_time_stamp = \
                defaults._mode_settings[3]
            defaults.auto_create_subject_id = defaults._mode_settings[4]
            defaults._mode_settings = None
            try:
                defaults.event_logging = defaults._mode_settings[5]
            except:
                pass
            set_skip_wait_methods(False)
        else:
            pass  # Nothing to do


def _get_module_values(goal_dict, module):
    value = None
    namespace = locals()
    for var in dir(module):
        if not var.startswith("_"):
            exec("value = {0}.{1}".format(module.__name__, var), namespace)
            goal_dict["{0}.{1}".format(module.__name__, var)] = namespace['value']
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

    from .. import design,stimuli, io, control,misc
    from ..io import extras as ioextras
    from ..design import extras as designextras
    from ..stimuli import extras as stimuliextras
    from ..misc import extras as miscextras

    defaults = {}
    defaults = _get_module_values(defaults, design.defaults)
    defaults = _get_module_values(defaults, control.defaults)
    defaults = _get_module_values(defaults, stimuli.defaults)
    defaults = _get_module_values(defaults, io.defaults)
    defaults = _get_module_values(defaults, misc.defaults)
    defaults = _get_module_values(defaults, designextras.defaults)
    defaults = _get_module_values(defaults, stimuliextras.defaults)
    defaults = _get_module_values(defaults, ioextras.defaults)
    defaults = _get_module_values(defaults, miscextras.defaults)
    if len(search_str) >= 0:
        tmp = {}
        for key in list(defaults.keys()):
            if key.lower().find(search_str.lower()) >= 0:
                tmp[key] = defaults[key]
        defaults = tmp
    if as_string:
        sorted_keys = list(defaults.keys())
        sorted_keys.sort()
        rtn = ""
        for key in sorted_keys:
            tabs = "\t" * (4 - int((len(key) + 1) // 8))
            rtn += key + ":" + tabs + repr(defaults[key]) + "\n"
    else:
        rtn = defaults

    return rtn


def register_wait_callback_function(function, exp=None):
    """Register a wait callback function.

    The registered wait callback function will be repetitively executed in
    all Expyriment wait and event loops that wait for an external input.
    That is, they are executed by the following functions (at least once!):

        - control.wait_end_audiosystem
        - misc.Clock.wait
        - misc.Clock.wait_seconds
        - misc.Clock.wait_minutes
        - io.Keyboard.wait
        - io.Keyboard.wait_char
        - io.Mouse.wait_press
        - io.SerialPort.read_line
        - io.StreamingButtonBox.wait
        - io.EventButtonBox.wait
        - io.GamePad.wait_press
        - io.TriggerInput.wait
        - io.TextInput.get
        - io.TouchScreenButtonBox.wait
        - io.extras.CedrusResponseDevice.wait
        - stimuli.Video.wait_frame
        - stimuli.Video.wait_end

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

    See Also
    --------
    unregister_wait_callback_function

    """

    if exp is not None:
        exp.register_wait_callback_function(function)
    else:
        _internals.active_exp.register_wait_callback_function(function)


def unregister_wait_callback_function(exp=None):
    """Unregister all wait callback functions.

    Parameters
    ----------
    exp : design.Experiment, optional
        specific experiment for which to unregister the wait callback function


    See Also
    --------
    register_wait_callback_function

    """

    if exp is not None:
        exp.unregister_wait_callback_function()
    else:
        _internals.active_exp.unregister_wait_callback_function()

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

        def flush(self):  # required for some modules (e.g. multiprocessing)
            pass

    if is_ipython_running():
        print("Standard output and error logging is switched off under IPython.")
    elif is_idle_running():
        print("Standard output and error logging is switched off under IDLE.")
    else:
        sys.stderr = Logger(event_file, "stderr")
        sys.stdout = Logger(event_file, "stdout")
