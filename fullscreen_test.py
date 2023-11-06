import expyriment as xpy
import pygame


xpy.control.defaults.display = 0
xpy.control.defaults.open_gl = 3
xpy.control.defaults.window_mode = True
xpy.control.defaults.window_size = [800, 600] #[640, 480]
xpy.control.defaults.window_scaling = 125
#xpy.control.defaults.display_resolution = (1536, 864) #(1920, 1080)

exp = xpy.control.initialize()

print("Surface size", exp.screen.surface.get_size())
print("Window size", exp.screen.window_size)
print("Display resolution", exp.screen.display_resolution)
print("Num displays", pygame.display.get_num_displays())
print("Desktop sizes", pygame.display.get_desktop_sizes())
size = exp.screen.window_size  #(1920, 1080) 
#size = (1920, 1080) 
rect = xpy.stimuli.Rectangle(size, line_width=1, colour=[255,0,0])
print(rect.present())
exp.keyboard.wait()
#xpy.control.run_test_suite()
