#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: <2016-04-23 10:47:53 chrplr>

''' Display two white squares in alternance and play sounds simultanously, 
to check timing with external equipment (oscilloscope, BlackBox ToolKit, ...) '''

import expyriment

exp = expyriment.design.Experiment(name="Cross-modal-timing-test")
expyriment.control.initialize(exp)

## setup
square_top = expyriment.stimuli.Rectangle((100, 100), position=(0, 200))
square_bottom = expyriment.stimuli.Rectangle((100, 100), position=(0, -200))
tone1 = expyriment.stimuli.Tone(100, 440)
tone2 = expyriment.stimuli.Tone(100, 880)

square_top.preload()
square_bottom.preload()
tone1.preload()
tone2.preload()

SOA = 20 * (1000 * 1/60.) - 5 # a bit less than 10 frames at 1/60Hz
NCYCLES = 10 

frame = expyriment.stimuli.Canvas((600, 600))
msg = expyriment.stimuli.TextScreen("",
                "Display two white squares for in alternance \n" +
                " and play sounds simultanously, \n"+
                " to check timing with external equipment \n" +
                " (oscilloscope, Blackbox toolkit, etc.)",
                position=(0,-100))
msg.plot(frame)
square_top.plot(frame)
square_bottom.plot(frame)


## run
expyriment.control.start(skip_ready_screen=True)

exp.screen.clear()
frame.present()
exp.keyboard.wait()


clock = expyriment.misc.Clock()

for i in range(NCYCLES * 3):

    while (clock.time < (SOA * i)):
        pass

    if (i % 3) == 0:
       exp.screen.clear()
       t = 0 # ?
    elif (i % 3) == 1: 
        tone1.play()
        t = square_top.present()
    else:
        tone2.play()
        t = square_bottom.present()
 
    clock.wait(SOA - t)

    exp.data.add([clock.time])
    exp.keyboard.process_control_keys()


## finish
expyriment.control.end()

