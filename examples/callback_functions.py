#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example of the usage of callback_functions in Expyriment
"""
from __future__ import absolute_import, print_function, division
from builtins import *

from expyriment import control, stimuli
from expyriment.control import CallbackQuitEvent

control.set_develop_mode(True)

def my_callback():
    """Quit all event loop with mouse press"""
    global exp
    if exp.mouse.check_button_pressed(0):
        return CallbackQuitEvent(data="'Mouse Button'")

## initialize ##
exp = control.initialize()

# The registered callback function will be continuously called by all wait or event
# loops such as wait.keyboard
control.register_wait_callback_function(my_callback)

## start ##
control.start(exp, skip_ready_screen=True)

stimuli.TextLine(text="waiting keypress....").present()

key, rtn = exp.keyboard.wait()
if isinstance(key, CallbackQuitEvent):
    stimuli.TextLine(text= "Wait keyboard has been quited by " + \
                     "{0} after {1} ms".format(key, rtn), text_size=12).present()
    # my_callback should not be called for the next clock wait
    control.unregister_wait_callback_function()
    exp.clock.wait(4000)

## end ##
control.end()
