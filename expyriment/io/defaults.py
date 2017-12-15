"""
Default settings for the io package.

This module contains default values for all optional arguments in the init
function of all classes in this package.

"""

__author__ = 'Florian Krause <florian@expyriment.org, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

from ..misc import constants as _constants

# Keyboard
keyboard_default_keys = None

#Mouse
mouse_show_cursor = True
mouse_track_button_events = True
mouse_track_motion_events = False

# StreamingButtonBox
streamingbuttonbox_baseline = 0

# OutputFile
outputfile_comment_char = "#"
outputfile_time_stamp = True
outputfile_eol = "\n"

# EventFile
eventfile_directory = "events"
eventfile_delimiter = ","

# DataFile
datafile_directory = "data"
datafile_delimiter = ","

# SeriaPort
serialport_baudrate = 19200
serialport_bytesize = 8
serialport_parity = 'N'
serialport_stopbits = 1
serialport_timeout = 0
serialport_xonxoff = 0
serialport_rtscts = 0
serialport_dsrdtr = 0
serialport_input_history = None
serialport_input_timing = 1
serialport_os_buffer_size = 3000

# MarkerOutput
markeroutput_default_code = 1
markeroutput_default_duration = None

# TriggerInput
triggerinput_default_code = 1

# TextInput
textinput_position = (0, 0)
textinput_character_filter = None
textinput_length = 25
textinput_message_text_size = None  # 'None' is experiment_text_size
textinput_message_colour = None  # 'None is experiment_text_colour
textinput_message_font = None  # 'None' will use default system font
textinput_message_bold = False
textinput_message_italic = False
textinput_message_right_to_left = False
textinput_user_text_size = None  # 'None' is experiment_text_size
textinput_user_text_colour = None  # 'None' is experiment_text_colour
textinput_user_text_font = None  # 'None' will use default system font
textinput_user_text_bold = False
textinput_user_right_to_left = False
textinput_background_colour = None  # 'None' is experiment_background_colour
textinput_frame_colour = None  # 'None' is experiment_text_colour
textinput_gap = 6

# Menu
textmenu_text_size = 20
textmenu_gap = 2
textmenu_position = (0, 0)
textmenu_background_colour = _constants.C_BLACK
textmenu_heading_font = None
textmenu_text_font = None
textmenu_text_colour = _constants.C_GREY
textmenu_heading_text_colour = _constants.C_EXPYRIMENT_ORANGE
textmenu_select_background_colour = _constants.C_DARKGREY
textmenu_select_text_colour = [0, 0, 0]
textmenu_select_frame_colour = _constants.C_EXPYRIMENT_ORANGE
textmenu_select_frame_line_width = 0
textmenu_justification = 1
textmenu_scroll_menu = 0
