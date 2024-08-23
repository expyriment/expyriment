import os

import expyriment as xpy


#xpy.control.defaults.opengl = False
#xpy.control.defaults.window_mode = True
#xpy.control.defaults.window_size = (1600, 1200)
#xpy.io.defaults.textmenu_text_size=40
exp = xpy.design.Experiment(text_font="Impact", text_size=40)
xpy.control.initialize(exp)
xpy.control.run_test_suite()
#xpy.stimuli.BlankScreen(colour=(255,0,0)).present()
#exp.clock.wait(2000)
