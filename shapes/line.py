__author__ = 'Vlad'

from util.global_options import write_output
from shape import Shape
from util.type import Type

class Line(Shape):
    def __init__(self, name, **kwargs):
        super(Line, self).__init__(**kwargs)

        self.default.points = []
        self.default.line_cap = 'butt'
        self.default.dash_array = []
        self.default.detection_type = 'pixel'
        self.set_default_attrs(self.default)

        self.name = name
        self.shape_type = 'Line'

        self._parse_line_config(kwargs)
        self._make_constructor()

    def get_dash_array(self):
        """Get dash array"""
        return self.attrs.dash_array

    def get_line_cap(self):
        """Get line cap"""
        return self.attrs.line_cap

    def get_points(self):
        """Get points array"""
        return self.attrs.points

    @write_output
    def set_dash_array(self, dash_array):
        """Set dash array"""
        self.attrs.dash_array = dash_array[:]
        return '%s.setDashArray(%s);' %(self.attrs, Type.format(self.attrs.dash_array))

    @write_output
    def set_line_cap(self, line_cap):
        """Set line cap. Can be butt, round, or square"""
        self.attrs.line_cap = line_cap
        return '%s.setLineCap(%s);' %(self.name, Type.format(line_cap))

    @write_output
    def set_points(self, points):
        """Set points array"""
        self.attrs.points = points[:]
        return '%s.setPoints(%s)' %(self.name, Type.format(self.attrs.points))


    def _parse_line_config(self, kwargs):
        if 'points' in kwargs:
            self.attrs.points = kwargs['points'][:]
        else:
            raise NameError('parameter "points" is required')
        if 'line_cap' in kwargs:
            self.attrs.line_cap = kwargs['line_cap']
        if 'dash_array' in kwargs:
            self.attrs.dash_array = kwargs['dash_array'][:]


