#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Word fragment completion task as used in the study of Weldon (1991).

Stimulus list: "word_fragment_completion_stimuluslist.csv"!

Weldon, M. S. (1991). Mechanisms underlying priming on
perceptual tests. Journal of Experimental Psychology: Learning, Memory, and
Cognition, 17, 526-541.

"""

import csv
from expyriment import design, control, stimuli, io, misc

control.set_develop_mode(True)

#### read in wordlist file and make design
exp = design.Experiment("word fragment completion test")
block = design.Block()
with open("word_fragment_completion_stimuluslist.csv", "rb") as f:
    reader = csv.reader(f)
    for row in reader:
        trial = design.Trial()
        trial.set_factor("word", row[0].strip())
        trial.set_factor("fragment", row[1].strip())
        block.add_trial(trial)
block.shuffle_trials()
exp.add_block(block)
exp.add_data_variable_names(["word", "fragment", "RT", "RT2", "answer"])

control.initialize(exp)

#prepare some stimuli
fixcross = stimuli.FixCross(line_width=1)
fixcross.preload()
blank = stimuli.BlankScreen()
blank.preload()
txt_input = io.TextInput("")
control.start(exp)

#run experiment
for trial in exp.blocks[0].trials:
    #present blank inter-trial-screen and prepare stimulus
    blank.present()
    fragment = ""
    for c in trial.get_factor("fragment").upper():
        fragment += c + " "
    target = stimuli.TextLine(fragment.strip())
    target.preload()
    exp.clock.wait(1000)
    #present fixcross
    fixcross.present()
    exp.clock.wait(500)
    #present target
    target.present()
    key, rt = exp.keyboard.wait(misc.constants.K_SPACE)
    #ask response
    exp.clock.reset_stopwatch()
    answer = txt_input.get()
    rt2 = exp.clock.stopwatch_time
    #process answer and save data
    blank.present()
    answer = answer.strip()
    exp.data.add([trial.get_factor("word"), trial.get_factor("fragment"),
                  rt, rt2, answer])
    target.unload()

control.end()
