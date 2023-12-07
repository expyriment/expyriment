"""
Default settings for the stimuli package.

This module contains default values for all optional arguments in the init
function of all classes in this package.

"""

__author__ = 'Florian Krause <florian@expyriment.org, \
Oliver Lindemann <oliver@expyriment.org>'


from tempfile import mkdtemp as _mkdtemp
from shutil import rmtree as _rmtree
import atexit as _atexit

# Visual
visual_position = (0, 0)

# Canvas
canvas_colour = None  # 'None' is transparent
canvas_position = (0, 0)

# TextLine
textline_text_font = None  # 'None' is experiment_text_font
textline_text_size = None  # 'None' is experiment_text_size
textline_text_bold = False
textline_text_italic = False
textline_text_underline = False
textline_text_colour = None  # 'None' is experiment_text_colour
textline_background_colour = None  # 'None' is transparent
textline_position = (0, 0)

# TextBox
textbox_text_font = None  # 'None' is experiment_text_font
textbox_text_size = None  # 'None' is experiment_text_size
textbox_text_bold = False
textbox_text_italic = False
textbox_text_underline = False
textbox_text_justification = 1
textbox_text_colour = None  # 'None' is experiment_text_colour
textbox_background_colour = None  # 'None' is transparent
textbox_position = (0, 0)
textbox_do_not_trim_words = False

# TextScreen
textscreen_heading_font = None  # 'None' is experiment_heading_font
textscreen_heading_size = None  # 'None' is experiment_heading_size
textscreen_heading_bold = False
textscreen_heading_italic = False
textscreen_heading_underline = False
textscreen_heading_colour = None  # 'None' is experiment_heading_colour
textscreen_text_font = None  # 'None' is experiment_text_font
textscreen_text_size = None  # 'None' is experiment_text_size
textscreen_text_bold = False
textscreen_text_italic = False
textscreen_text_underline = False
textscreen_text_colour = None  # 'None' is experiment_text_colour
textscreen_text_justification = 1
textscreen_background_colour = None  # 'None' is transparent
textscreen_size = None  # 'None' is 4/5 of full screen
textscreen_position = (0, 0)

# Ellipse
ellipse_colour = None  # 'None' is experiment_text_colour
ellipse_line_width = 0
ellipse_position = (0, 0)
ellipse_anti_aliasing = 0

# FixCross
fixcross_colour = None  # 'None' is experiment_text_colour
fixcross_size = (20, 20)
fixcross_line_width = 2
fixcross_position = (0, 0)
fixcross_anti_aliasing = 0

# Circle
circle_colour = None  # 'None' is experiment_text_colour
circle_position = (0, 0)
circle_anti_aliasing = 0
circle_line_width = 0

# Shape
shape_colour = None  # 'None' is experiment_text_colour
shape_position = (0, 0)
shape_anti_aliasing = 0

# Line
line_colour = None  # 'None' is experiment_text_colour
line_anti_aliasing = 0

# Rectangle
rectangle_colour = None  # 'None' is experiment_text_colour
rectangle_position = (0, 0)
rectangle_line_width = 0
rectangle_corner_rounding = 0
rectangle_corner_anti_aliasing = 0

# Picture
picture_position = (0, 0)

# Video
video_position = [0, 0]
video_backend = "mediadecoder"  # 'mediadecoder' or 'pygame'

# Tone
tone_frequency = 440
tone_samplerate = 44100
tone_bitdepth = 16
tone_amplitude = 0.5

# Create tmp for compressed stimuli folder
try:
    tempdir = _mkdtemp(prefix="expyriment_")
except Exception:
    tempdir = None

def _remove_tempdir():
    global tempdir
    try:
        _rmtree(tempdir)
    except Exception:
        pass

_atexit.register(_remove_tempdir)
