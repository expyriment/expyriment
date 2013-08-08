#!/usr/bin/env python

"""
A simple behavioural task to asses a Simon effect.

See also:
http://en.wikipedia.org/wiki/Simon_effect

"""

from expyriment import design, control, stimuli, io, misc


# Create and initialize an Experiment
exp = design.Experiment("Simon Task")
control.initialize(exp)

# Define and preload standard stimuli
fixcross = stimuli.FixCross()
fixcross.preload()

# Create IO
#response_device = io.EventButtonBox(io.SerialPort("/dev/ttyS1"))
response_device = exp.keyboard

# Create design
for task in ["left key for green", "left key for red"]:
    b = design.Block()
    b.set_factor("Response", task)
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
exp.add_bws_factor("ResponseMapping", [1, 2])
exp.data_variable_names = ["Position", "Button", "RT"]

# Start Experiment
control.start()
exp.permute_blocks(misc.constants.P_BALANCED_LATIN_SQUARE)
for block in exp.blocks:
    stimuli.TextScreen("Instructions", block.get_factor("Response")).present()
    response_device.wait()
    for trial in block.trials:
        fixcross.present()
        exp.clock.wait(1000 - trial.stimuli[0].preload())
        trial.stimuli[0].present()
        button, rt = response_device.wait()
        exp.data.add([trial.get_factor("Position"), button, rt])

# End Experiment
control.end()
