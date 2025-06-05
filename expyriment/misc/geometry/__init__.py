"""
The geometry module.

This module contains miscellaneous geometry functions for expyriment.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from ._geometry import coordinates2position, position2coordinates, position2coordinate
from ._geometry import position2visual_angle, visual_angle2position
from ._geometry import cartesian2polar, polar2cartesian, tuples2points
from ._geometry import points_to_vertices, points2vertices, lines_intersect, XYPoint
from ._geometry import lines_intersection_point
from ._basic_shapes import vertices_triangle, vertices_rectangle, vertices_regular_polygon
from ._basic_shapes import vertices_frame, vertices_trapezoid, vertices_parallelogram, vertices_cross
