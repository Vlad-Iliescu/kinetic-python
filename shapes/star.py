__author__ = 'Vlad'

from util.global_options import write_output
from shape import Shape
from util.type import Type

class Star(Shape):
    def __init__(self, name, **kwargs):
        super(Star, self).__init__(**kwargs)

        self.default.num_points = 0
        self.default.inner_radius = 0.0
        self.default.outer_radius = 0.0
        self.set_default_attrs(self.default)

        self.name = name
        self.shape_type = 'Star'

        self._parse_star_config(kwargs)
        self._make_constructor()

    def get_inner_radius(self):
        """Ret inner radius"""
        return self.attrs.inner_radius

    def get_num_points(self):
        """Get number of points"""
        return self.attrs.num_points

    def get_outer_radius(self):
        """Get outer radius"""
        return self.attrs.outer_radius

    @write_output
    def set_inner_radius(self, radius):
        """Set inner radius"""
        self.attrs.inner_radius = round(radius, 2)
        return '%s.setInnerRadius(%s);' %(self.name, Type.format(self.attrs.inner_radius))

    @write_output
    def set_num_points(self, points):
        """Set number of points"""
        self.attrs.num_points = points
        return '%s.setNumPoints(%d);' %(self.name, points)

    @write_output
    def set_outer_radius(self, radius):
        """Set outer radius"""
        self.attrs.outer_radius = round(radius, 2)
        return '%s.setOuterRadius(%s);' %(self.name, Type.format(self.attrs.outer_radius))

    def _parse_star_config(self, kwargs):
        """
        :type kwargs: dict
        """
        if 'num_points' in kwargs:
            self.attrs.num_points = kwargs['num_points']
        else:
            raise NameError('parameter "num_points" is required')
        if 'outer_radius' in kwargs:
            self.attrs.outer_radius = round(kwargs['outer_radius'], 2)
        else:
            raise NameError('parameter "outer_radius" is required')
        if 'inner_radius' in kwargs:
            self.attrs.inner_radius = round(kwargs['inner_radius'], 2)
        else:
            raise NameError('parameter "inner_radius" is required')

