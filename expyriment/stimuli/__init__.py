"""The stimuli package.

This Package contains a variety of classes implementing experimental stimuli.
See also expyriment.stimuli.extras for more stimuli.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

from . import defaults
from ._audio import Audio
from ._blankscreen import BlankScreen
from ._canvas import Canvas
from ._circle import Circle
from ._ellipse import Ellipse
from ._fixcross import FixCross
from ._line import Line
from ._picture import Picture
from ._rectangle import Rectangle
from ._shape import Shape
from ._textbox import TextBox
from ._textline import TextLine
from ._textscreen import TextScreen
from ._tone import Tone
from ._video import Video
