__author__ = 'Vlad'

from util.global_options import write_output
from shape import Shape
from util.type import Type

class Circle(Shape):
    def __init__(self, name, **kwargs):
        super(Circle, self).__init__(**kwargs)

        self.name = name
        self.shape_type = 'Circle'

        self.default.radius = 0.0
        self.set_default_attrs(self.default)

        self._parse_circle_config(kwargs)

        self._make_constructor()

    def get_radius(self):
        """Get radius"""
        return self.attrs.radius

    @write_output
    def set_radius(self, radius):
        """Set radius"""
        self.attrs.radius = round(radius, 2)
        return '%s.setRadius(%s);' %(self.name, Type.format(self.attrs.radius))

    def _parse_circle_config(self, kwargs):
        if 'radius' in kwargs:
            self.attrs.radius = round(kwargs['radius'], 2)
        else:
            raise NameError('parameter "radius" is required')
