"""
Default settings for the design package.

This module contains default values for all optional arguments in the init
function of all classes in this package.

"""

__author__ = 'Florian Krause <florian@expyriment.org, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import os
import sys


# Experiment
experiment_name = None  # Set None if experiment default name should be the
#                        name of the python main file


experiment_background_colour = (0, 0, 0)
experiment_foreground_colour = (150, 150, 150)

# On some versions of Mac OS, looking up a font without a full path fails. This
# is a quick hack to overcome this issue, but the root cause should be figured
# out.
if sys.platform == 'darwin':
    experiment_text_font = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            "..", "_fonts", "FreeSans.ttf"
    ))
else:
    experiment_text_font = "FreeSans"
experiment_text_size = 20
experiment_filename_suffix = None

# Block
block_name = 'unnamed'
max_shuffle_time = 5000

# trial_list
trial_list_directory = 'trials'
