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
        return self.attrs.font_size

    def get_font_style(self):
        """Get font style"""
        return self.attrs.font_style

    def get_height(self):
        """Get height of text box"""
        return self.attrs.height

    def get_line_height(self):
        """Get line height"""
        return self.attrs.line_height

    def get_padding(self):
        """Get padding"""
        return self.attrs.padding

    def get_shadow(self):
        """Get shadow of text or textbox"""
        return self.attrs.shadow

    def get_text(self):
        """Get text"""
        return self.attrs.text

    def get_text_fill(self):
        """Get text fill color"""
        return self.attrs.text_fill

    def get_text_height(self):
        """Get text height in pixels"""
        return '%s.getTextHeight()' %self.name

    def get_text_stroke(self):
        """Get text stroke color"""
        return self.attrs.text_stroke

    def get_text_stroke_width(self):
        """get text stroke width"""
        return self.attrs.text_stroke_width

    def get_text_width(self):
        """Get text width in pixels"""
        return '%s.getTextWidth()' %self.name

    def get_width(self):
        """get width of text box"""
        return self.attrs.width

    @write_output
    def set_align(self, align):
        """Set horizontal align of text"""
        self.attrs.align = align
        return '%s.setAlign(%s);' %(self.name, Type.format(align))

    @write_output
    def set_font_family(self, font_family):
        """Set font family"""
        self.attrs.font_family = font_family
        return '%s.setFontFamily(%s);' %(self.name, Type.format(font_family))

    @write_output
    def set_font_size(self, font_size):
        """Set font size"""
        self.attrs.font_size = font_size
        return '%s.setFontSize(%d)' %(self.name, font_size)

    @write_output
    def set_font_stroke(self, font_stroke):
        """Set text stroke color"""
        self.attrs.font_stroke = font_stroke
        return '%s.setFontStroke(%s);' %(self.name, Type.format(font_stroke))

    @write_output
    def set_font_style(self, font_style):
        """set font style. Can be "normal", "italic", or "bold". "normal" is the default."""
        self.attrs.font_style = font_style
        return '%s.setFontStyle(%s);' %(self.name, Type.format(font_style))

    @write_output
    def set_height(self, height):
        """set height of text box"""
        self.attrs.height = round(height, 2)
        return '%s.setHeight(%s);' %(self.name, Type.format(self.attrs.height))

    @write_output
    def set_line_height(self, line_height):
        """Set line height"""
        self.attrs.line_height = round(line_height, 2)
        return '%s.setLineHeight(%s);' %(self.name, self.attrs.line_height)

    @write_output
    def set_padding(self, padding):
        """Set padding"""
        self.attrs.padding = padding
        return '%s.setPadding(%d);' %(self.name, padding)

    @write_output
    def set_shadow(self, shadow):
        """Set shadow of text or textbox"""
        self.attrs.shadow = Storage(shadow)
        return '%s.setShadow(%s);' %(self.name, Type.format(self.attrs.shadow))

    @write_output
    def set_text(self, text):
        """Set text"""
        self.attrs.text = text
        return "%s.setText(%s);" %(self.name, Type.format(text))

    @write_output
    def set_text_fill(self, text_fill):
        """Set text fill color"""
        self.attrs.text_fill = text_fill
        return '%s.setTextFill(%s);' %(self.name, Type.format(text_fill))

    @write_output
    def set_text_stroke_width(self, text_stroke_width):
        """Set text stroke width"""
        self.attrs.text_stroke_width = text_stroke_width
        return '%s.setTextStrokeWidth(%d);' %(self.name, text_stroke_width)

    @write_output
    def set_width(self, width):
        """Set width of text box"""
        self.attrs.width = round(width, 2)
        return '%s.setWidth(%s)' %(self.name, Type.format(self.attrs.width))

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
