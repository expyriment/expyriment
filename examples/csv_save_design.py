#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Save design to csv file
"""
from __future__ import print_function

from expyriment import design

exp = design.Experiment(name="SNARC")

# Design: 2 response mappings x 8 stimuli x 10 repetitions
for response_mapping in ["left_odd", "right_odd"]:
    block = design.Block()
    block.set_factor("mapping", response_mapping)
    #add trials to block
    for digit in [1, 2, 3, 4, 6, 7, 8, 9]:
        trial = design.Trial()
        trial.set_factor("digit", digit)
        block.add_trial(trial, copies=10)
    block.shuffle_trials()
    exp.add_block(block)

exp.add_experiment_info("This a just a SNARC experiment.")
#add between subject factors
exp.add_bws_factor('mapping_order', ['left_odd_first', 'right_odd_first'])
#prepare data output
exp.data_variable_names = ["block", "mapping", "trial", "digit", "ISI",
                           "btn", "RT", "error"]

exp.save_design("design.csv")

print(exp)
