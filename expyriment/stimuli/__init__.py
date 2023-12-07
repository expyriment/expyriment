"""The stimuli package.

This Package contains a variety of classes implementing experimental stimuli.
See also expyriment.stimuli.extras for more stimuli.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

from . import defaults
from ._audio import Audio
from ._video import Video
from ._canvas import Canvas
from ._circle import Circle
from ._rectangle import Rectangle
from ._line import Line
from ._ellipse import Ellipse
from ._shape import Shape
from ._blankscreen import BlankScreen
from ._textline import TextLine
from ._fixcross import FixCross
from ._textbox import TextBox
from ._textscreen import TextScreen
from ._picture import Picture
from ._tone import Tone

from ._obsolete import Dot, Frame
