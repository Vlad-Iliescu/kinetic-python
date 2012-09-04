__author__ = 'Vlad'

from shape import Shape
from util.type import Type
from util.global_options import write_output

class Rect(Shape):
    def __init__(self, name, **kwargs):
        super(Rect, self).__init__(**kwargs)

        self.default.width = 0.0
        self.default.height = 0.0
        self.default.corner_radius = 0.0

        self.set_default_attrs(self.default)

        self.shape_type = "Rect"
        self.name = name
#        self.attrs.draw_funct = self.draw_funct
        self._parse_rect_config(kwargs)
        self._make_constructor()

    def draw_funct(self):
        pass

    def get_corner_radius(self):
        """Get corner radius"""
        return self.attrs.corner_radius

    def get_height(self):
        """Get height"""
        return self.attrs.height

    def get_width(self):
        """Get width"""
        return self.attrs.width

    @write_output
    def set_corner_radius(self, radius):
        """Set corner radius"""
        self.attrs.corner_radius = round(radius, 2)
        return '%s.setCornerRadius(%s)' %(self.name, Type.format(self.attrs.corner_radius))

    @write_output
    def set_width(self, width):
        """Set width"""
        self.attrs.width = round(width, 2)
        return '%s.setWidth(%s)' %(self.name, Type.format(self.attrs.width))

    @write_output
    def set_height(self, height):
        """Set height"""
        self.attrs.height = round(height, 2)
        return '%s.setHeight(%s)' %(self.name, Type.format(self.attrs.height))

    @write_output
    def set_size(self, width, height):
        """Set height"""
        self.set_width(width)
        self.set_height(height)
        return '%s.setSize(%s, %s)' %(self.name, Type.format(self.attrs.width), Type.format(self.attrs.height))

    def _parse_rect_config(self, kwargs):
        if 'width' in kwargs:
            self.attrs.width = round(kwargs['width'], 2)
        if 'height' in kwargs:
            self.attrs.height = round(kwargs['height'], 2)
        if 'corner_radius' in kwargs:
            self.attrs.corner_radius = kwargs['corner_radius']

if __name__ == '__main__':
    rect = Rect('rect', width = 10, height= 15)
    from util.global_options import write_to_file
    write_to_file('../kin.js')
