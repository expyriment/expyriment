#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example: moving stimulus in Expyriment using none OpenGL mode"""
from __future__ import division

from expyriment import control, stimuli, misc

control.defaults.open_gl = False # switch off opengl to avoid screen refesh sync

exp = control.initialize()
control.start()

radius = 20
movement = [4, 8]
arena = (exp.screen.size[0] // 2 - radius, exp.screen.size[1] // 2 - radius)
dot = stimuli.Circle(radius=radius, colour=misc.constants.C_YELLOW)

stimuli.BlankScreen().present()

exp.clock.reset_stopwatch()
while exp.clock.stopwatch_time < 10000:
    erase = stimuli.Rectangle(size=dot.surface_size, position=dot.position,
                        colour = exp.background_colour)
    dot.move(movement)
    if dot.position[0] > arena[0] or dot.position[0] < -1*arena[0]:
        movement[0] = -1 * movement[0]
    if dot.position[1] > arena[1] or dot.position[1] < -1*arena[1]:
        movement[1] = -1 * movement[1]

    erase.present(clear=False, update=False) # present but do not refesh screen
    dot.present(clear=False, update=True)    # present but do not refesh screen
    exp.screen.update_stimuli([dot, erase])  # refesh screen
    exp.keyboard.check()    # ensure that keyboard input is proccesed
                            # to quit experiment with ESC
    exp.clock.wait(1)

control.end()
