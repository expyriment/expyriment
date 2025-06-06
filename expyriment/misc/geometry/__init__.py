"""
The geometry module.

This module contains miscellaneous geometry functions for expyriment.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from ._basic_shapes import (
    vertices_cross,
    vertices_frame,
    vertices_parallelogram,
    vertices_rectangle,
    vertices_regular_polygon,
    vertices_trapezoid,
    vertices_triangle,
)
from ._geometry import (
    XYPoint,
    cartesian2polar,
    coordinates2position,
    lines_intersect,
    lines_intersection_point,
    points2vertices,
    points_to_vertices,
    polar2cartesian,
    position2coordinate,
    position2coordinates,
    position2visual_angle,
    tuples2points,
    visual_angle2position,
)
