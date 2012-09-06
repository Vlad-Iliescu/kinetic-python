__author__ = 'Vlad'

from util.global_options import write_output
from shape import Shape
from util.type import Type

class Polygon(Shape):
    def __init__(self, name, **kwargs):
        super(Polygon, self).__init__(**kwargs)

        self.default.points = []
        self.set_default_attrs(self.default)

        self.name = name
        self.shape_type = 'Polygon'

        self._parse_polygon_config(kwargs)
        self._make_constructor()

    def get_points(self):
        """Get points array"""
        return self.attrs.points

    @write_output
    def set_points(self, points):
        """Set points array"""
        self.attrs.points = points[:]
        return '%s.setPoints(%s);' %(self.name, Type.format(self.attrs.points))

    def _parse_polygon_config(self, kwargs):
        if 'points' in kwargs:
            self.attrs.points = kwargs['points'][:]
        else:
            raise NameError('parameter "points" is required')
