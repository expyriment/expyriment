"""
The geometry module.

This module contains miscellaneous geometry functions for expyriment.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import math as _math
from ... import _internals


def coordinates2position(coordinate, surface_size=None):
    """"OBSOLETE FUNCTION: Please use 'coordinate2position'."""

    raise DeprecationWarning("coordinates2position is an obsolete function. Please use coordinate2position.")
    
    coordinate2position(coordinate, surface_size=None)

def coordinate2position(coordinate, surface_size=None):
    """Convert a coordinate on the screen or surface to an
    Expyriment position.

    Parameters
    ----------
    coordinate : (int, int)
        coordinate (x,y) to convert
    surface_size: (int, int), optional
        size of the surface one which position is defined
        if None (default), the position will be calculated relative
        to the screen

    Returns
    -------
    coordinate : [int, int]

    """

    if surface_size is None:
        surface_size = _internals.active_exp.screen.surface.get_size()

    rtn = [coordinate[0] - surface_size[0] // 2,
            - coordinate[1] + surface_size[1] // 2]
    if (surface_size[0] % 2) == 0: #even
        rtn[0] += 1
    if (surface_size[1] % 2) == 0:
        rtn[1] -= 1
    return rtn

def position2coordinate(position, surface_size=None):
    """Convert an Expyriment position to a coordinate on the
    screen or surface.

    Parameters
    ----------
    coordinate : (int, int)
        coordinate (x,y) to convert
    surface_size: (int, int), optional
        size of the surface one which position should be calculated
        if None (default), the position will be calculated relative
        to the screen

    Returns
    -------
    coordinate : [int, int]

    """

    if surface_size is None:
        surface_size = _internals.active_exp.screen.surface.get_size()

    rtn = [position[0] + surface_size[0] // 2,
            - position[1] + surface_size[1] // 2]
    if (surface_size[0] % 2) == 0: #even
        rtn[0] -= 1
    if (surface_size[1] % 2) == 0:
        rtn[1] -= 1
    return rtn

def position2visual_angle(position, viewing_distance, monitor_size):
    """Convert an expyriment position (pixel) to a visual angle from center.

    Parameters
    ----------
    position : (int, int)
        position (x,y) to convert
    viewing_distance : numeric
        viewing distance in cm
    monitior_size : numeric
        physical size of the monitor in cm (x, y)

    Returns
    -------
    angle : (float, float)
        visual angle for x & y dimension

    """

    screen_size = _internals.active_exp.screen.surface.get_size()
    cm = (position[0] * monitor_size[0] / float(screen_size[0]),
          position[1] * monitor_size[1] / float(screen_size[1]))

    angle = (2.0 * _math.atan((cm[0] / 2) / viewing_distance),
             2.0 * _math.atan((cm[1] / 2) / viewing_distance))
    return (angle[0] * 180 / _math.pi, angle[1] * 180 / _math.pi)

def visual_angle2position(visual_angle, viewing_distance, monitor_size):
    """Convert an position defined as visual angle from center to expyriment
    position (pixel).

    Parameters
    ----------
    visual_angle : (numeric, numeric)
        position in visual angle (x,y) to convert
    viewing_distance : numeric
        viewing distance in cm
    monitior_size : (numeric, numeric)
        physical size of the monitor in cm (x, y)

    Returns
    -------
    position : (float, float)
        position (x,y)

    """

    screen_size = _internals.active_exp.screen.surface.get_size()
    angle = (visual_angle[0] * _math.pi / 360,
             visual_angle[1] * _math.pi / 360) # angle / 180 / 2
    cm = (_math.tan(angle[0]) * viewing_distance * 2,
          _math.tan(angle[1]) * viewing_distance * 2)
    return (cm[0] * screen_size[0] / monitor_size[0],
            cm[1] * screen_size[1] / monitor_size[1])

def points_to_vertices(points):
    """OBSOLETE FUNCTION! Please use `points2vertices`!"""
    
    raise DeprecationWarning("points_to_vertices is an obsolete function. Please use point2vertices.")

    point2vertices(points)
    
def points2vertices(points):
    """Returns vertex representation of the points (int, int) in xy-coordinates

    Parameters
    ----------
    points : (int, int)
        list of points

    Returns
    -------
    vtx : list
        list of vertices

    """

    vtx = []
    for i in range(1, len(points)):
        vtx.append((points[i][0] - points[i - 1][0], points[i][1] - points[i - 1][1]))
    return vtx

def lines_intersect(pa, pb, pc, pd):
    """Return true if two line segments are intersecting

    Parameters
    ----------
    pa : misc.XYPoint
        point 1 of line 1
    pb : misc.XYPoint
        point 2 of line 1
    pc : misc.XYPoint
        point 1 of line 2
    pb : misc.XYPoint
        point 2 of line 2

    Returns
    -------
    check : bool
        True if lines intersect

    """

    def ccw(pa, pb, pc):
        return (pc._y - pa._y) * (pb._x - pa._x) > (pb._y - pa._y) * (pc._x - pa._x)

    return ccw(pa, pc, pd) != ccw(pb, pc, pd) and ccw(pa, pb, pc) != ccw(pa, pb, pd)

def cartesian2polar(xy, radians=False):
    """Convert a cartesian coordinate (x,y) to a polar coordinate
    (radial, angle[degrees]).

    Parameters
    ----------
    xy : (float, float)
        cartesian coordinate (x,y)
    radians : boolean
        use radians instead of degrees for the angle

    Returns
    ----------
    polar : (float, float)
        polar coordinate (radial, angle[degrees])

    """

    ang = _math.atan2(xy[1], xy[0])
    radial =_math.hypot(xy[0], xy[1])
    if radians:
        return (radial, ang)
    else:
        return (radial, _math.degrees(ang))

def polar2cartesian(polar, radians=False):
    """Convert a polar coordinate (radial, angle[degrees])
     to a polar coordinate (x, y)


    Parameters
    ----------
    polar : (float, float)
        polar coordinate (radial, angle[degrees])
    radians : boolean
        use radians instead of degrees for the angle

    Returns
    ----------
    xy : (float, float)
        cartesian coordinate (x,y)

    """

    if radians:
        a = polar[1]
    else:
        a = _math.radians(polar[1])
    return (polar[0]*_math.cos(a), polar[0]*_math.sin(a))


class XYPoint(object):
    """ The Expyriment point class """
    def __init__(self, x=None, y=None, xy=None):
        """Initialize a XYPoint.

        Parameters
        ----------
        x : numeric
        y : numeric
        xy : (numeric, numeric)
            xy = (x,y)

        Notes
        -----
        use `x`, `y` values (two numberic) or the tuple xy=(x,y)

        """

        if x is None:
            if xy is None:
                self._x = 0
                self._y = 0
            else:
                self._x = xy[0]
                self._y = xy[1]
        elif y is None:
            #if only a tuple is specified: e-g. Point((23,23))
            self._x = x[0]
            self._y = x[1]
        else:
            self._x = x
            self._y = y

    def __repr__(self):
        return  "(x={0}, y={1})".format(self._x, self._y)

    @property
    def x(self):
        """Getter for x"""
        return self._x

    @x.setter
    def x(self, value):
        """Getter for x"""
        self._x = value

    @property
    def y(self):
        """Getter for y"""
        return self._y

    @y.setter
    def y(self, value):
        """Getter for y"""
        self._y = value

    @property
    def tuple(self):
        return (self._x, self._y)

    @tuple.setter
    def tuple(self, xy_tuple):
        self._x = xy_tuple[0]
        self._y = xy_tuple[1]


    @property
    def polar(self):
        return cartesian2polar((self._x, self._y))

    def move(self, v):
        """Move the point along the coodinates specified by the vector v.

        Parameters
        ----------
        v : misc.XYPoint
            movement vector

        """

        self._x = self._x + v._x
        self._y = self._y + v._y
        return self

    def distance(self, p):
        """Return euclidian distance to the points (p).

        Parameters
        ----------
        p : misc.XYPoint
            movement vector

        Returns
        -------
        dist : float
            distance to other point p

        """

        dx = self._x - p._x
        dy = self._y - p._y
        return _math.hypot(dx, dy)

    def rotate(self, degree, rotation_centre=(0, 0)):
        """Rotate the point counterclockwise in degree around rotation_centre.

        Parameters
        ----------
        degree : int
            degree of rotation (default=(0, 0) )
        rotation_center : (numeric, numeric)
            rotation center (x, y)

        """

        #cart -> polar
        r, ang = cartesian2polar(xy = (self._x - rotation_centre[0],
                                       self._y - rotation_centre[1]),
                                 radians=True)
        ang -= _math.radians(degree)
        #polar -> cart
        self._x = r * _math.sin(ang) + rotation_centre[0]
        self._y = r * _math.cos(ang) + rotation_centre[1]


    def is_inside_polygon(self, point_list):
        """Return true if point is inside a given polygon.

        Parameters
        ----------
        point_list : list
            point list defining the polygon

        Returns
        -------
        check : bool

"""

        n = len(point_list)
        inside = False

        p1 = point_list[0]
        for i in range(n + 1):
            p2 = point_list[i % n]
            if self._y > min(p1._y, p2._y):
                if self._y <= max(p1._y, p2._y):
                    if self._x <= max(p1._x, p2._x):
                        if p1._y != p2._y:
                            xinters = (self._y - p1._y) * (p2._x - p1._x) // (p2._y - p1._y) + p1._x
                        if p1._x == p2._x or self._x <= xinters:
                            inside = not inside
            p1 = p2

        return inside
