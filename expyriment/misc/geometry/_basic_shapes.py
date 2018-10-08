"""
This file is part of the geometry module.

This module contains functions to create vertex lists of basic
geometrical shapes.

"""

from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import math as _math
from ._geometry import XYPoint, points2vertices

def _angular_vertex(angle, length):
    """Helper function

    calculates the vertex coordinates of a line with a particular
    length and angle (relative to the horizontal)

    """

    angle = _math.radians(angle)
    return -1*_math.cos(angle)*float(length), -1*_math.sin(angle)*float(length)


def vertices_rectangle(size):
    """Returns a list of vertices describing a rectangle

    Notes
    -----
    The resulting vertices can be plotted with the class
    stimuli.Shape(vertex_list=...).

    Parameters
    ----------
    size : (int, int)
        size (width, height) of the rectangle

    Returns
    -------
    vtx : list of vertices

    """

    return  [ (size[0]-1, 0),
              (0, -size[1]+1),
              (-size[0]+1, 0),
              (0, size[1]-1)]



def vertices_cross(size, line_width):
    """Returns a list of vertices describing a cross

    Notes
    -----
    The resulting vertices can be plotted with the class
    stimuli.Shape(vertex_list=...).

    Parameters
    ----------
    size : (int, int)
        xy, length of the horizontal (x) and vertical (y) line
    line_width : int
        width of the lines

    Returns
    -------
    vtx : list of vertices

    See also
    --------
    stimuli.FixCross()

    """

    x_a = (size[0] - line_width) // 2
    x_b = x_a
    y_a = (size[1] - line_width) // 2
    y_b = y_a

    if (size[0] - line_width) % 2:  # both have the different parities
        x_b = x_a + 1
        # to ensure that Shape behaves like two crossed surfaces plotted on each other
        if line_width % 2:  # odd line width swap x_a - x_b
            x_b, x_a = x_a, x_b

    if (size[1] - line_width) % 2:  # both have the different parities
        y_b = y_a + 1
        if line_width % 2 == 0:  # even line width swap x_a - x_b
            y_b, y_a = y_a, y_b

    return [(line_width - 1, 0),
            (0, -y_a),
            (x_a, 0),
            (0, -line_width + 1),
            (-x_a, 0),
            (0, -y_b),
            (-line_width + 1, 0),
            (0, y_b),
            (-x_b, 0),
            (0, line_width - 1),
            (x_b, 0)]


def vertices_trapezoid(width_top, width_bottom, height):
    """Returns a list of vertices describing a trapezoid

    Notes
    -----
    The resulting vertices can be plotted with the class
    stimuli.Shape(vertex_list=...).

    Parameters
    ----------
    width_top: int
        width of the top edge
    width_bottom: int
        width of the bottom edge
    height : int
        height of the trapezoid

    Returns
    -------
    vtx : list of vertices

    """

    left_bottom =XYPoint(x = 0, y = 0)
    right_bottom = XYPoint(x = width_bottom, y = 0)
    left_top = XYPoint(x = 0 + (width_bottom-width_top)/2.0, y = height)
    right_top = XYPoint(x = width_bottom - (width_bottom-width_top)/2.0, y = height)
    return list(map(lambda xy: (int(xy[0]), int(xy[1])),
                    points2vertices((left_top, right_top, right_bottom, left_bottom))))


def vertices_triangle(angle, length1, length2):
    """Returns a list of vertices describing a triangle
    A, B, C
    ```
            A --- B
                 .
                .
               C
    ```

    Notes
    -----
    The resulting vertices can be plotted with the class
    stimuli.Shape(vertex_list=...).

    Parameters
    ----------
    angle : float
        the angle between the lines AB and BC in degrees
    length1 : float
        the length between AB
    length2 : float
        the length between BC

    Returns
    -------
    vtx : list of vertices

    """

    xy = _angular_vertex(angle, length2)
    return [(length1-1, 0), (int(xy[0]), int(xy[1]))]


def vertices_parallelogram(angle, length1, length2):
    """Returns a list of vertices describing a parallelogram
    A, B, C, D
    ```
            A --- B
           .     .
          .     .
         D --- C
    ```

    Notes
    -----
    The resulting vertices can be plotted with the class
    stimuli.Shape(vertex_list=...).

    Parameters
    ----------
    angle : float
        the angle between the lines AB and BC in degrees
    length1 : float
        the length between AB
    length2 : float
        the length between BC

    Returns
    -------
    vtx : list of vertices

    """

    vtx = vertices_triangle(angle=angle, length1=length1, length2=length2)
    vtx.append((-length1+1, 0))
    return vtx


def vertices_regular_polygon(n_edges, length):
    """Returns a list of vertices describing a regular
    polygon

    Notes
    -----
    The resulting vertices can be plotted with the class
    stimuli.Shape(vertex_list=...).

    Parameters
    ----------
    n_edges : int
        the number of edges
    length : float
        the length of one side of the polygon

    Returns
    -------
    vtx : list of vertices

    """

    sum_of_angle = (n_edges - 2) * 180.0
    angle = 180 - (sum_of_angle / n_edges)
    x = 180
    vtx = []
    for _ in range(n_edges - 1):
        v = _angular_vertex(x, length=length)
        vtx.append((int(v[0]), int(v[1])))
        x += angle
    return vtx


def vertices_frame(size, frame_thickness):
    """Returns a list of vertices describing a frame

    Notes
    -----
    The resulting vertices can be plotted with the class
    stimuli.Shape(vertex_list=...).

    Parameters
    ----------
    size : (int, int)
        size (width, height) of the rectangle
    frame_thickness : int
        the thickness of the frame

    Returns
    -------
    vtx : list of vertices

    """

    return  [(size[0] - frame_thickness - 1, 0),
             (0, -size[1]+1),
             (-size[0]+1, 0),
             (0, size[1]-1),
             (frame_thickness - 1, 0),
             (0, -(size[1] - frame_thickness - 1)),
             (size[0] - 2 * frame_thickness - 1, 0),
             (0, size[1] - 2 * frame_thickness - 1),
             (-(size[0] - 2 * frame_thickness - 2), 0)]
