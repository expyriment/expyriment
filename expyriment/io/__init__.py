"""The io package.

This package contains several classes and functions that implement
input and output interfaces.

See also expyriment.io.extras for more io.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from . import defaults
from ._input_output import set_skip_wait_functions
from ._screen import Screen
from ._keyboard import Keyboard
from ._mouse import Mouse
from ._files import InputFile, OutputFile, DataFile, EventFile
from ._parallelport import ParallelPort
from ._serialport import SerialPort
from ._gamepad import GamePad
from ._eventbuttonbox import EventButtonBox
from ._streamingbuttonbox import StreamingButtonBox
from ._triggerinput import TriggerInput
from ._markeroutput import MarkerOutput
from ._textinput import TextInput
from ._textmenu import TextMenu
from ._touchscreenbuttonbox import TouchScreenButtonBox