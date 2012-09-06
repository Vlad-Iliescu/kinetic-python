__author__ = 'Vlad'

from util.global_options import write_output
from shape import Shape
from util.type import Type

class RegularPolygon(Shape):
    def __init__(self, name, **kwargs):
        super(RegularPolygon, self).__init__(**kwargs)

        self.default.radius = 0
        self.default.sides = 0
        self.set_default_attrs(self.default)

        self.name = name
        self.shape_type = 'RegularPolygon'
        self._parse_polygon_config(kwargs)
        self._make_constructor()

    def get_radius(self):
        """Get radius"""
        return self.attrs.radius

    def get_sides(self):
        """Get number of sides"""
        return self.attrs.sides

    @write_output
    def set_radius(self, radius):
        """Set points array"""
        self.attrs.radius = round(radius, 2)
        return '%s.setRadius(%s);' %(self.name, Type.format(self.attrs.radius))

    @write_output
    def set_sides(self, sides):
        """Set number of sides"""
        self.attrs.sides = sides
        return '%s.setSides(%s);' %(self.name, Type.format(self.attrs.sides))

    def _parse_polygon_config(self, kwargs):
        if 'sides' in kwargs:
            self.attrs.sides = kwargs['sides']
        else:
            raise NameError('parameter "sides" is required')
        if 'radius' in kwargs:
            self.attrs.radius = round(kwargs['radius'], 2)
        else:
            raise NameError('parameter "radius" is required')

