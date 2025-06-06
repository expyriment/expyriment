"""
The geometry module.

This module contains miscellaneous geometry functions for expyriment.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import math as _math

from ... import _internals


def coordinates2position(coordinates, surface_size=None):
    """Convert coordinates on the screen or surface to an
    Expyriment position.

    Parameters
    ----------
    coordinates : (int, int)
        coordinates (x,y) to convert
    surface_size: (int, int), optional
        size of the surface one which position is defined
        if None (default), the position will be calculated relative
        to the screen

    Returns
    -------
    position : [int, int]

    """

    if surface_size is None:
        surface_size = _internals.active_exp.screen.surface.get_size()

    rtn = [coordinates[0] - surface_size[0] // 2,
            - coordinates[1] + surface_size[1] // 2]
    if (surface_size[0] % 2) == 0: #even
        rtn[0] += 1
    if (surface_size[1] % 2) == 0:
        rtn[1] -= 1
    return rtn

def position2coordinate(coordinate, surface_size=None):
    """"OBSOLETE FUNCTION: Please use 'position2coordinates'."""

    raise DeprecationWarning("position2coordinate is an obsolete function. Please use position2coordinates.")

    position2coordinates(coordinate, surface_size=None)

def position2coordinates(position, surface_size=None):
    """Convert an Expyriment position to coordinates on the
    screen or surface.

    Parameters
    ----------
    position : (int, int)
        position (x,y) to convert
    surface_size: (int, int), optional
        size of the surface one which coordinates should be calculated
        if None (default), the coordinates will be calculated relative
        to the screen

    Returns
    -------
    coordinates : [int, int]

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

def tuples2points(list_of_tuples):
    """Converts a list of tuples (x,y) to a list of misc.XYPoints"""
    return list(map(lambda v:XYPoint(x=v[0], y=v[1]), list_of_tuples))

def points_to_vertices(points):
    """OBSOLETE FUNCTION! Please use `points2vertices`!"""

    raise DeprecationWarning("points_to_vertices is an obsolete function. Please use points2vertices.")

def points2vertices(points):
    """Returns vertex representation of the points (list of misc.XYPoints)

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
        vtx.append((points[i].x - points[i - 1].x, points[i].y - points[i - 1].y))
    return vtx

def lines_intersect(pa, pb, pc, pd):
    """Returns true if two line segments are intersecting

    Parameters
    ----------
    pa : misc.geometry.XYPoint
        point 1 of line 1
    pb : misc.geometry.XYPoint
        point 2 of line 1
    pc : misc.geometry.XYPoint
        point 1 of line 2
    pb : misc.geometry.XYPoint
        point 2 of line 2

    Returns
    -------
    check : bool
        True if lines intersect

    """

    def ccw(pa, pb, pc):
        return (pc._y - pa._y) * (pb._x - pa._x) > (pb._y - pa._y) * (pc._x - pa._x)

    return ccw(pa, pc, pd) != ccw(pb, pc, pd) and ccw(pa, pb, pc) != ccw(pa, pb, pd)

def lines_intersection_point(pa, pb, pc, pd):
    """Returns the intersection point of two lines (a-b) and (c-d)

    Parameters
    ----------
    pa : misc.geometry.XYPoint
        point 1 of line 1
    pb : misc.geometry.XYPoint
        point 2 of line 1
    pc : misc.geometry.XYPoint
        point 1 of line 2
    pb : misc.geometry.XYPoint
        point 2 of line 2

    Returns
    -------
    intersec_point: misc.geometry.XYPoint
        intersection point

    """

    # slope: dy/dx (y2 - y1) / (x2 - x1)
    slope = ((pb.y - pa.y) / float(pb.x - pa.x), #line 1
             (pd.y - pc.y) / float(pd.x - pc.x)) #line 2
    if slope[0] == slope[1]:
        return None  # lines are parallel

    # intercept: y = slope*x + b,  b = y - slope*x
    intercept =(pa.y - slope[0]*pa.x,
                pc.y - slope[1]*pc.x)

    # Set both lines equal to find the intersection point in the x direction
    # m1 * x + b1 = m2 * x + b2 ==> x = (b2 - b1) / (m1 - m2)
    x = (intercept[1] - intercept[0]) / float(slope[0] - slope[1])
    # solve for y:  y = mx + b
    y = slope[0] * x + intercept[0]
    return XYPoint(x=x,y=y)


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
    """Convert a polar coordinate (radial, angle[degrees]) to a polar
    coordinate (x, y)


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
        use `x`, `y` values (two numbers) or the tuple xy=(x,y)

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
        """Getter for the tuple (x, y) """

        return (self._x, self._y)

    @tuple.setter
    def tuple(self, xy_tuple):
        self._x = xy_tuple[0]
        self._y = xy_tuple[1]


    @property
    def polar(self):
        """Getter for polar coordinate the point """

        return cartesian2polar((self._x, self._y))

    def move(self, v):
        """Move the point along the coordinates specified by the vector v.

        Parameters
        ----------
        v : misc.XYPoint
            movement vector

        """

        self._x = self._x + v._x
        self._y = self._y + v._y
        return self

    def distance(self, p):
        """Return euclidean distance to the points (p).

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
        self._x, self._y = polar2cartesian(polar=(r, ang), radians=True)
        self._x += rotation_centre[0]
        self._y += rotation_centre[1]


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
