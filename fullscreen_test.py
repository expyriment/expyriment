import expyriment as xpy
import pygame


xpy.control.defaults.display = 0
xpy.control.defaults.open_gl = 0
xpy.control.defaults.window_mode = True
#xpy.control.defaults.window_size = [800, 600] #[640, 480]
#xpy.control.defaults.window_scaling = 125
xpy.control.defaults.display_resolution = (1920, 1080)

exp = xpy.control.initialize()

print("Surface size", exp.screen.surface.get_size())
print("Window size", exp.screen.window_size)
print("Display resolution", exp.screen.display_resolution)
print("Num displays", pygame.display.get_num_displays())
print("Desktop sizes", pygame.display.get_desktop_sizes())
print("List modes", pygame.display.list_modes())
print("---")
#exp.screen.save("s.png")
exp.keyboard.wait(xpy.misc.constants.K_SPACE)
size = exp.screen.window_size  #(1920, 1080) 
size = (100, 100)
line_width = 1
rect = xpy.stimuli.Rectangle(size, line_width=line_width, colour=[255,0,0])
rect.present()
print(rect.surface_size)
rect.save("r.png")
exp.keyboard.wait(xpy.misc.constants.K_SPACE)
c = xpy.stimuli.Circle(100, line_width=line_width, colour=[255,0,0])
c.present()
print(c.surface_size)
c.save("c.png")
exp.keyboard.wait(xpy.misc.constants.K_SPACE)
#xpy.control.run_test_suite()
