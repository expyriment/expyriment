"""The io package.

This package contains several classes and functions that implement
input and output interfaces.

See also expyriment.io.extras for more io.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from . import defaults
from ._eventbuttonbox import EventButtonBox
from ._files import DataFile, EventFile, InputFile, OutputFile
from ._gamepad import GamePad
from ._keyboard import Keyboard
from ._markeroutput import MarkerOutput
from ._mouse import Mouse
from ._parallelport import ParallelPort
from ._screen import Screen
from ._serialport import SerialPort
from ._streamingbuttonbox import StreamingButtonBox
from ._textinput import TextInput
from ._textmenu import TextMenu
from ._touchscreenbuttonbox import TouchScreenButtonBox
from ._triggerinput import TriggerInput
