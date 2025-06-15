"""
The geometry module.

This module contains miscellaneous geometry functions for expyriment.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from ._basic_shapes import (vertices_cross, vertices_frame,
                            vertices_parallelogram, vertices_rectangle,
                            vertices_regular_polygon, vertices_trapezoid,
                            vertices_triangle)
from ._geometry import (XYPoint, cartesian_to_polar, coordinates_to_position,
                        lines_intersect, lines_intersection_point,
                        points_to_vertices, polar_to_cartesian,
                        position_to_coordinates, position_to_visual_angle,
                        tuples_to_points, visual_angle_to_position)
