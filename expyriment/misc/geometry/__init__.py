"""
The geometry module.

This module contains miscellaneous geometry functions for expyriment.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from ._geometry import coordinate2position, position2coordinate, coordinates2position
from ._geometry import position2visual_angle, visual_angle2position
from ._geometry import points_to_vertices, lines_intersect, XYPoint
