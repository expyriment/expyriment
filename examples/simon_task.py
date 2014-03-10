#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A simple experiment to assess a Simon effect.

See also: http://en.wikipedia.org/wiki/Simon_effect

"""

from expyriment import design, control, stimuli, io, misc

# Create and initialize an Experiment
exp = design.Experiment("Simon Task")
control.initialize(exp)

# Define and preload standard stimuli
fixcross = stimuli.FixCross()
fixcross.preload()
# left and right arrow keys for responses
response_keys = [misc.constants.K_LEFT, misc.constants.K_RIGHT]

# Create design
for mapping in ["left4green", "left4red"]:
    b = design.Block()
    b.set_factor("Mapping", mapping)
    for where in [["left", -300], ["right", 300]]:
        for what in [["red", misc.constants.C_RED],
                     ["green", misc.constants.C_GREEN]]:
            t = design.Trial()
            t.set_factor("Position", where[0])
            t.set_factor("Colour", what[0])
            s = stimuli.Rectangle([50, 50], position=[where[1], 0],
                                  colour=what[1])
            t.add_stimulus(s)
            b.add_trial(t, copies=20)
    b.shuffle_trials()
    exp.add_block(b)
exp.add_bws_factor("OrderOfMapping", [1, 2])

exp.data_variable_names = ["Mapping", "Colour", "Position", "Button", "RT"]

# Start Experiment
control.start()
if exp.get_permuted_bws_factor_condition("OrderOfMapping") == 2:
    exp.swap_blocks(0,1)
for block in exp.blocks:
    stimuli.TextScreen("Instructions", block.get_factor("Mapping")).present()
    exp.keyboard.wait()
    for trial in block.trials:
        fixcross.present()
        exp.clock.wait(1000 - trial.stimuli[0].preload())
        trial.stimuli[0].present()
        button, rt = exp.keyboard.wait(keys=response_keys)
        exp.data.add([block.get_factor("Mapping"), trial.get_factor("Colour"),
                        trial.get_factor("Position"), button, rt])

# End Experiment
control.end()
