#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A parity judgment task to assess the SNARC effect.

See e.g.:
Gevers, W., Reynvoet, B., & Fias, W. (2003). The mental representation of
ordinal sequences is spatially organized. Cognition, 87(3), B87-95.

"""

from expyriment import design, control, stimuli
from expyriment.misc import constants


control.set_develop_mode(False)

########### DESIGN ####################
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

#set further variables
t_fixcross = 500
min_max_ISI = [200, 750] # [min, max] inter_stimulus interval
ITI = 1000
t_error_screen = 2000
no_training_trials = 10

######### INITIALIZE ##############
control.initialize(exp)

# Prepare and preload some stimuli
blankscreen = stimuli.BlankScreen()
blankscreen.preload()
fixcross = stimuli.FixCross()
fixcross.preload()
error_beep = stimuli.Tone(duration=200, frequency=2000)
error_beep.preload()

#define a trial
def run_trial(cnt, trial):
    # present Fixation cross and prepare trial in the meantime
    fixcross.present()
    exp.clock.reset_stopwatch()
    ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
    digit = trial.get_factor("digit")
    target = stimuli.TextLine(text=str(digit), text_size=60)
    target.preload()
    exp.clock.wait(t_fixcross - exp.clock.stopwatch_time)
    #present blankscreen for a random interval
    blankscreen.present()
    exp.clock.wait(ISI)
    # Present target & record button response
    target.present()
    btn, rt = exp.keyboard.wait([constants.K_LEFT, constants.K_RIGHT])
    #Error feedback if required
    if block.get_factor("mapping") == "left_odd":
        error = (digit % 2 == 0 and btn == constants.K_LEFT) or \
                (digit % 2 == 1 and btn == constants.K_RIGHT)
    else:
        error = (digit % 2 == 1 and btn == constants.K_LEFT) or \
                (digit % 2 == 0 and btn == constants.K_RIGHT)

    #write data and clean up while inter-trial-interval
    blankscreen.present()
    if error:
        error_beep.present()
        exp.clock.wait(t_error_screen)

    exp.clock.reset_stopwatch()
    exp.data.add([block.id, block.get_factor("mapping"),
                  cnt, target.text, ISI,
                  btn, rt, int(error)])
    exp.data.save()
    target.unload()
    exp.clock.wait(ITI - exp.clock.stopwatch_time)


######### START ##############
control.start(exp)

# permute block order across subjects
if exp.get_permuted_bws_factor_condition('mapping_order') == "right_odd_first":
    exp.swap_blocks(0, 1)

# Run the actual experiment
for block in exp.blocks:
    # Show instruction screen
    if block.get_factor("mapping") == "left_odd":
        instruction = "Press LEFT arrow key for ODD\n" + \
                            "and RIGHT arrow key for EVEN numbers."
    else:
        instruction = "Press RIGHT arrow key for ODD\n" + \
                            "and LEFT arrow key for EVEN numbers."
    stimuli.TextScreen("Indicate the parity of the numbers", instruction +
                       "\n\nPress space bar to start training.").present()
    exp.keyboard.wait(constants.K_SPACE)
    #training trials
    for cnt in range(0, no_training_trials):
        trial = block.get_random_trial()
        run_trial(-1 * (1 + cnt), trial) #training trails has negative trial numbers
    # Show instruction screen
    stimuli.TextScreen("Attention!", instruction +
                       "\n\nThe experimental block starts now.").present()
    exp.keyboard.wait(constants.K_SPACE)
    # experimental trials
    for cnt, trial in enumerate(block.trials):
        run_trial(cnt, trial)


####### END EXPERIMENT ########
control.end(goodbye_text="Thank you very much for participating in our experiment",
             goodbye_delay=5000)
