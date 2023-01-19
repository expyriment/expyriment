import expyriment as xpy
import pygame


xpy.control.defaults.display = 0
#xpy.control.defaults.opengl = 0

exp = xpy.control.initialize()

print(exp.screen.surface.get_size())
print(exp.screen.window_size)
print(exp.screen.display_resolution)
print(pygame.display.get_num_displays())
print(pygame.display.get_desktop_sizes())
size = exp.screen.window_size  #(1920, 1080) 
#size = (1920, 1080) 
rect = xpy.stimuli.Rectangle(size, line_width=1, colour=[255,0,0])
rect.present()
exp.keyboard.wait()
