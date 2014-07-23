#!/usr/bin/env python

"""
A Shape stimulus.

This module contains a class implementing a shape stimulus.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import copy
from math import sqrt
import pygame

import defaults
from _visual import Visual
import expyriment
from expyriment.misc._timer import get_time

class Shape(Visual):
    """A class implementing a shape."""

    def __init__(self, position=None, colour=None, line_width=None,
                 anti_aliasing=None):
        """Create a shape.

        A shape comprises always (0,0) as origin vertex

        Parameters
        ----------
        position : (int, int), optional
            position of the stimulus
        colour : (int, int, int), optional
            colour of the shape
        line_width : int, optional
            line width in pixels; 0 will result in a filled shape,
            as does a value < 0 or >= min(size) (optional)
        anti_aliasing : int, optional
            anti aliasing parameter (good anti_aliasing with 10)

        """

        if position is None:
            position = defaults.shape_position
        Visual.__init__(self, position)
        if colour is None:
            colour = defaults.shape_colour
        if colour is not None:
            self._colour = colour
        else:
            self._colour = expyriment._active_exp.foreground_colour
        if line_width is not None:
            self._line_width = line_width
        else:
            self._line_width = defaults.shape_line_width
        if anti_aliasing is not None:
            self._anti_aliasing = anti_aliasing
        else:
            self._anti_aliasing = defaults.shape_anti_aliasing

        self._vertices = []
        self._xy_points = []
        self._rect = []
        self._native_rotation = 0
        self._native_scaling = [1, 1]
        self._native_rotation_centre = (0, 0)
        self._rotation_centre_display_colour = None
        self._update_points()

    _getter_exception_message = "Cannot perform {0} if surface exists!"

    def __repr__(self):
        return  "vertices: {0}; points: {1}".format(self.vertices,
                                                    self.points)

    @property
    def colour(self):
        """Getter for colour."""

        return self._colour

    @colour.setter
    def colour(self, colour):
        """Setter for colour."""

        if self.has_surface:
            raise AttributeError(Shape._getter_exception_message.format(
                "colour change"))
        self._colour = colour

    @property
    def anti_aliasing(self):
        """Getter for anti_aliasing."""

        return self._anti_aliasing

    @anti_aliasing.setter
    def anti_aliasing(self, value):
        """Setter for anti_aliasing."""

        if self.has_surface:
            raise AttributeError(Shape._getter_exception_message.format(
                "anti_aliasing"))
        self._anti_aliasing = value

    @property
    def rotation_centre(self):
        """Getter for rotation_centre."""
        return self._native_rotation_centre

    @rotation_centre.setter
    def rotation_centre(self, centre):
        """Setter for rotation_centre."""

        self._native_rotation_centre = centre
        self._update_points()


    @property
    def rotation_centre_display_colour(self):
        """Getter for rotation_centre_display_colour."""

        return self._rotation_centre_display_colour

    @rotation_centre_display_colour.setter
    def rotation_centre_display_colour(self, colour):
        """Setter for rotation_centre_display_colour.

        Set rotation_centre_display_colour to a colour (default=None) to
        display the centre of rotation.

        """

        self._rotation_centre_display_colour = colour
        self._update_points()

    @property
    def width(self):
        return self.rect[3] - self.rect[1]#r-l

    @property
    def height(self):
        return self.rect[0] - self.rect[2]#t-b

    @property
    def size(self):
        return (self.width, self.height)

    @property
    def line_width(self):
        return self._line_width

    @property
    def rect(self):
        """Getter for rect =(top, left, bottom, right)."""

        return self._rect

    @property
    def vertices(self):
        """Getter for the polygon verticies."""

        return self._vertices

    @property
    def points(self):
        """Return polygon as list of tuples (x,y) in Expyriment coordinates.

        In contrast to the vertex representation, the point representation
        takes into all the native transformations (rotation, scaling,
        flipping)

        Returns
        -------
        val: list of tuples
            polygon as list of tuples (x,y) in Expyriment coordinates

        """

        rtn = []
        for p in self.xy_points:
            rtn.append(p.tuple)
        return rtn

    @property
    def points_on_screen(self):
        """Return polygon as list of tuples in Expyriment coordinates.

        In contrast to the vertex representation, the point representation
        takes into all the native transformations (rotation, scaling,
        flipping)

        Returns
        -------
        val: list of tuples
            polygon as list of tuples (x,y) in Expyriment coordinates

        """

        rtn = []
        for p in self.xy_points_on_screen:
            rtn.append(p.tuple)
        return rtn

    @property
    def scaling(self):
        """"Getter for the total native scaling."""
        return self._native_scaling

    @property
    def rotation(self):
        """"Getter for the total native rotation."""
        return self._native_rotation

    @property
    def flipping(self):
        """"Getter for the total native flipping."""
        return ((self.scaling[0] < 0), (self.scaling[1] < 0))

    @property
    def xy_points(self):
        """Return polygon as list of XYPoints of the shape.

        The representation does not take into account the position. Use
        xy_points_on_screen for position-depended representation.

        In contrast to the vertex representation, the point representation
        takes into all the native transformations (rotation, scaling,
        flipping).

        Returns
        -------
        val: list of XYPoints
             polygon as list of XYPoints of the shape

        """

        return self._xy_points

    @property
    def xy_points_on_screen(self):
        """Return polygon as list of XYPoints in Expyriment coordinates.

        In contrast to the vertex representation, the point representation
        takes into all the native transformations (rotation, scaling,
        flipping).

        Returns
        -------
        val: list of XYPoints
             polygon as list of XYPoints of the shape

        """

        rtn = []
        pos = expyriment.misc.geometry.XYPoint(xy=self.position)
        for p in copy.deepcopy(self.xy_points):
            rtn.append(p.move(pos))
        return rtn

    def add_vertex(self, xy):
        """ Add a vertex to the shape.

        Parameters
        ----------
        xy : (int, int)
            vertex as tuple

        """

        self.add_vertices([xy])

    def add_vertices(self, vertex_list):
        """ Add a list of vertices to the shape.

        Parameters
        ----------
        vertex_list : (int, int)
            list of vertices (int, int)

        """
        type_error_message = "The method add_vertices requires a list of" + \
                            " tuples as argument."
        if self.has_surface:
            raise AttributeError(Shape._getter_exception_message.format(
                "add_vertices"))
        if type(vertex_list) is not list:
            raise TypeError(type_error_message)
        for xy in vertex_list:
            if type(xy) is not tuple and type(xy) is not list:
                raise TypeError(type_error_message)
            if len(xy) != 2:
                raise TypeError(type_error_message)
            self._vertices.append(list(xy))
        self._update_points()

    def remove_vertex(self, index):
        """Remove a vertex."""

        if self.has_surface:
            raise AttributeError(Shape._getter_exception_message.format(
                "remove_vertex"))
        if index > 0 and index < len(self._vertices):
            self._vertices.pop(index)
        self._update_points()

    def erase_vertices(self):
        """Removes all vertices."""

        if self.has_surface:
            raise AttributeError(Shape._getter_exception_message.format(
                "erase_vertices"))

        self._vertices = []
        self._xy_points = []
        self._rect = []
        self._native_rotation = 0
        self._native_scaling = [1, 1]
        self._native_rotation_centre = (0, 0)
        self._rotation_centre_display_colour = None
        self._update_points()

    def convert_expyriment_xy_to_surface_xy(self, point_xy):
        """Convert a point from shape coordinates to surface coordinates.

        Parameters
        ----------
        point_xy : (int, int)
            Expyriment screen coordinates (tuple)

        """

        jitter = self._line_width / 2
        return (int(point_xy[0] - self.rect[1] + jitter),
                - 1 * int(point_xy[1] - self.rect[0] - jitter))

    def native_overlapping_with_position(self, position):
        """Return True if the position is inside the shape.

        Parameters
        position -- Expyriment screen coordinates (tuple)

        Returns
        -------
        val : bool
            True if the position is inside the shape

        """

        pt = expyriment.misc.geometry.XYPoint(position)
        return pt.is_inside_polygon(self.xy_points_on_screen)

    def is_point_inside(self, point_xy):
        """DEPRECATED METHOD: Please use 'native_overlapping_with_position'."""

        return self.native_overlapping_with_position(point_xy)

    def overlapping_with_shape(self, other):
        """Return true if shape overlaps with other shape.

        Parameters
        ----------
        other : stimuli.Shape
            the other shape object

        Returns
        -------
        val : bool
            True if overlapping

        """

        # shape and other shape do not overlap if 
        # (a) no point of shape is inside other shape 
        # (b) AND no point of other shape is inside shape
        # (c) AND lines do not intersect

        s1 = self.xy_points_on_screen
        s2 = other.xy_points_on_screen
        #(a) & (b)
        for p in s1:
            if p.is_inside_polygon(s2):
                return True
        for p in s2:
            if p.is_inside_polygon(s1):
                return True
        #(c)
        for from1 in range(0, len(s1) - 1):
            for to1 in range(from1 + 1, len(s1)):
                for from2 in range(0, len(s2) - 1):
                    for to2 in range(0, len(s2)):
                        if expyriment.misc.geometry.lines_intersect(s1[from1],
                                                s1[to1], s2[from2], s2[to2]):
                            return True
        return False

    def is_shape_overlapping(self, shape2):
        """DEPRECATED METHOD: Please use 'overlapping_with_shape'."""

        return self.overlapping_with_shape(shape2)


    def native_rotate(self, degree):
        """Rotate the shape.

        Native rotation of shape is a native operation (not a surface
        operation) and does therefore not go along with a quality loss.
        No surface will be created.

        Parameters
        ----------
        degree : int
            degree to rotate counterclockwise (int)

        """

        if self.has_surface:
            raise AttributeError(Shape._getter_exception_message.format(
                "native_rotate"))
        self._native_rotation = self._native_rotation + degree
        self._update_points()

    def native_scale(self, factors, scale_line_width=False):
        """Scale the shape.

        Native scaling of shapes is a native operation (not a surface
        operation) and does therefore not go along with a quality loss.
        No surface will be created.

        Negative scaling values will native_flip the stimulus.

        Parameters
        ----------
        factors : int or (int, int)
            x and y factors to scale
        scale_line_width : bool, optional
            if True, line_width will be scaled proportionally to the change in
            surface size (default=False)

        """

        if (type(factors) is not list):
            factors = [factors, factors]
        if self.has_surface:
            raise AttributeError(Shape._getter_exception_message.format(
                "native_scale"))

        self._native_scaling[0] = self._native_scaling[0] * factors[0]
        self._native_scaling[1] = self._native_scaling[1] * factors[1]
        self._line_width = self._line_width * sqrt(factors[0] * factors[1])
        self._update_points()

    def native_flip(self, booleans):
        """Flip the shape.

        Native flipping of shapes is a native operation (not a surface
        operation) and does therefore not go along with a quality loss.
        No surface will be created.

        Parameters
        ----------
        booleans : (bool, bool)
            booleans to flip horizontally and vertically or not

        """

        if self.has_surface:
            raise AttributeError(Shape._getter_exception_message.format(
                "native_flip"))
        if booleans[0]:
            self._native_scaling[0] = self._native_scaling[0] * -1
        if booleans[1]:
            self._native_scaling[1] = self._native_scaling[1] * -1
        self._update_points()

    def blur(self, level):
        """Blur the shape.

        This blurs the stimulus, by scaling it down and up by the factor of
        'level'.
        Notes
        -----
        Depending on the blur level and the size of your stimulus, this method
        may take some time!

        Parameters
        ----------
        level : int
            level of bluring

        Returns
        -------
        time : int
            the time it took to execute this method

        """

        start = get_time()
        self.scale((1.0 / level, 1.0 / level))
        self.scale((level, level))
        return int((get_time() - start) * 1000)

    def _update_points(self):
        """Updates the points of the shape and the drawing rect.

        Converts vertex to points, centers points, rotates, calculates rect and
        clears surface and draw_rotation_point.

         """

        # Copying and scaling and flipping of verticies
        tmp_vtx = []
        for v in self._vertices:
            v = (v[0] * self._native_scaling[0],
                 v[1] * self._native_scaling[1])
            tmp_vtx.append(v)

        # Converts tmp_vtx to points in xy-coordinates
        xy_p = [expyriment.misc.geometry.XYPoint(0, 0)]
        for v in tmp_vtx:
            x = (v[0] + xy_p[-1].x)
            y = (v[1] + xy_p[-1].y)
            xy_p.append(expyriment.misc.geometry.XYPoint(x, y))

        xy_p = self._center_points(xy_p)
        if self._native_rotation != 0:
            for x in range(0, len(xy_p)):
                xy_p[x].rotate(self._native_rotation,
                               self._native_rotation_centre)

        self._xy_points = xy_p
        self._rect = self._make_shape_rect(self.xy_points)

    def _make_shape_rect(self, points):
        """Four points (geomerty.XYPoint) top, left, bottom, right."""

        t = 0
        l = 0
        r = 0
        b = 0
        for p in points:
            if p.x < l:
                l = p.x
            elif p.x > r:
                r = p.x
            if p.y > t:
                t = p.y
            elif p.y < b:
                b = p.y
        return (t, l, b, r)

    def _center_points(self, points):
        """Return centered points (list of geomerty.XYPoint)."""

        t, l, b, r = self._make_shape_rect(points)

        # Stimulus center
        c = expyriment.misc.geometry.XYPoint(((r - l) / 2.0) - r,
                                             ((t - b) / 2.0) - t)
        for x in range(0, len(points)): # Center points
            points[x].move(c)
        return points

    def _create_surface(self):
        """Create the surface of the stimulus."""

        # Trick: draw enlarged shape and reduce size
        if self._anti_aliasing > 0: # Draw enlarged shape
            aa_scaling = (self._anti_aliasing / 5.0) + 1
            old_scaling = copy.copy(self._native_scaling)
            old_line_width = self._line_width
            self.native_scale([aa_scaling, aa_scaling], scale_line_width=True)

        line_width = int(self._line_width)
        # Draw the rect
        s = (self.size[0] + line_width, self.size[1] + line_width)
        surface = pygame.surface.Surface(s,
                                        pygame.SRCALPHA).convert_alpha()
        #surface.fill((255, 0, 0)) # for debugging only
        poly = []
        for p in self.xy_points: # Convert points_in_pygame_coordinates
            poly.append(self.convert_expyriment_xy_to_surface_xy(p.tuple))
        rot_centre = self.convert_expyriment_xy_to_surface_xy(
            self._native_rotation_centre)
        pygame.draw.polygon(surface, self.colour, poly, line_width)
        if self._rotation_centre_display_colour is not None:
            pygame.draw.circle(surface, self._rotation_centre_display_colour,
                               rot_centre, 2)

        if self._anti_aliasing > 0: # Scale back
            size = surface.get_size()
            surface = pygame.transform.smoothscale(surface,
                                (int(size[0] / aa_scaling),
                                 int(size[1] / aa_scaling)))
            self._native_scaling = old_scaling
            self._line_width = old_line_width
            self._update_points()
        return surface


if __name__ == "__main__":
    from expyriment import control, design
    control.set_develop_mode(True)
    exp = design.Experiment(log_level=0)
    control.initialize(exp)
    sh = Shape(position=(20, 200), colour=(255, 0, 255))
    sh.add_vertex((0, 0))
    sh.add_vertex((50, 50))
    sh.add_vertex((0, 50))
    sh.present()
    exp.clock.wait(1000)
