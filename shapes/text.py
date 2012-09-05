__author__ = 'Vlad'

from util.global_options import write_output, Kinetic
from shape import Shape
from util.type import Type
from util.storage import Storage

class Text(Shape):
    def __init__(self, name, **kwargs):
        super(Text, self).__init__(**kwargs)

        self.default.font_size = 12
        self.default.font_family = 'Calibri'
        self.default.font_style = 'normal'
        self.default.text_stroke_width = 2
        self.default.align = 'left'
        self.default.padding = 0
        self.default.width = 'auto'
        self.default.height = 'auto'
        self.default.line_height = 1.2
        self.default.corner_radius = 0
        self.default.text = ''

        self.set_default_attrs(self.default)
        self.name = name
        self.shape_type = 'Text'

        self._parse_text_config(kwargs)
        self._make_constructor()

    def get_align(self):
        """Get horizontal align"""
        return self.attrs.align

    def get_box_height(self):
        """Get box height"""
        if self.attrs.height == 'auto':
            return '%s.getBoxHeight()' %self.name
        return self.attrs.height

    def get_box_width(self):
        """Get box width"""
        if self.attrs.width == 'auto':
            return '%s.getBoxWidth()' %self.name
        return self.attrs.width

    def get_font_family(self):
        """Get font family"""
        return self.attrs.font_family

    def get_font_size(self):
        """Get font size"""
        pass








    def _parse_text_config(self, kwargs):
        if 'text' in kwargs:
            self.attrs.text = kwargs['text']
        else:
            raise NameError('parameter "text" is required')
        if 'font_size' in kwargs:
            self.attrs.font_size = kwargs['font_size']
        if 'font_family' in kwargs:
            self.attrs.font_family = kwargs['font_family']
        if 'font_style' in kwargs:
            self.attrs.font_style = kwargs['font_style']
        if 'text_fill' in kwargs:
            self.attrs.text_fill = kwargs['text_fill']
        if 'text_stroke' in kwargs:
            self.attrs.text_stroke = kwargs['text_stroke']
        if 'text_stroke_width' in kwargs:
            self.attrs.text_stroke_width = kwargs['text_stroke_width']
        if 'align' in kwargs:
            self.attrs.align = kwargs['align']
        if 'padding' in kwargs:
            self.attrs.padding = kwargs['padding']
        if 'width' in kwargs:
            self.attrs.width = kwargs['width']
        if 'height' in kwargs:
            self.attrs.height = kwargs['height']
        if 'line_height' in kwargs:
            self.attrs.line_height = kwargs['line_height']
        if 'corner_radius' in kwargs:
            self.attrs.corner_radius = kwargs['corner_radius']







