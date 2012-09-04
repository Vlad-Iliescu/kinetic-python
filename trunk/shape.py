__author__ = 'Vlad'

from node import Node
from util.storage import Storage
from util.type import Type
from util.global_options import Kinetic, write_output

class Shape(Node):
    def __init__(self, var_name=None, **kwargs):
        """ Shape constructor. Shapes are primitive objects such as rectangles, circles, text, lines, etc.

        Keyword arguments:
        fill -- can be a string color, a linear gradient object, a radial gradient object, or a pattern object.
            fill.image -- image object if filling the shape with a pattern
            fill.offset -- pattern offset if filling the shape with a pattern (x,y)
            fill.start -- start point if using a linear gradient or radial gradient fill (x, y, radius)
            fill.end -- end point if using a linear gradient or radial gradient fill (x, y, radius)
        stroke -- stroke color
        stroke_width -- stroke width
        line_join -- line join can be miter, round, or bevel. The default is miter
        shadow -- shadow object (color, blur, (offset.x , offset.y), opacity)
        x -- x coord
        y -- y coord
        visible -- visible true or false
        listening -- whether or not the node is listening for events
        id -- unique id
        name -- non-unique name
        opacity -- determines node opacity. Can be any number between 0 and 1
        scale -- (scale.x, scale.y)
        rotation -- rotation in radians
        rotation_deg -- rotation in degrees
        offset -- offsets default position point and rotation point (offset.x, offset.y)
        draggable -- draggable true of false
        drag_constraint -- can be vertical, horizontal, or none. The default is none
        drag_bounds -- (dragBounds.top, dragBounds.right, dragBounds.bottom, dragBounds.right)
        """
        super(Shape, self).__init__(**kwargs)

        self.default.line_join = 'mitter'
        self.set_default_attrs(self.default)

        self.name = var_name
        self.node_type = "Shape"
        self.applied_shadow = False
        self.shape_type = ''

        shapes = Kinetic.Global.Shapes
        key = ''
        while True:
            key = Type.get_random_color_key()
            if key and not (key in shapes):
                break
        self.color_key = key
        shapes[key] = self

#        self._parse_shape_kwargs(kwargs)
        self._parse_shape_config(kwargs)
        if self.name:
            self._make_constructor()

    @write_output
    def apply_line_join(self, context):
        """Helper method to set the line join of a shapebased on the lineJoin property"""
        if self.attrs.line_join:
            context['line_join'] = self.attrs.line_join
        return '%s.applyLineJoin()' %self.name

    @write_output
    def draw_image(self, *args):
        """Helper method to draw an image and apply a shadow if needed"""
        applied_shadow = False
        context = args[0]
        context.save()
        a = args
        if len(a) == 6 or len(a) == 10:
            if self.attrs.shadow and not self.applied_shadow:
                applied_shadow = self._applyShadow(context)
            if len(a) == 6:
                context.draw_image(a[1], a[2], a[3], a[4], a[5])
            else:
                context.draw_image(a[1], a[2], a[3], a[4], a[5], a[6], a[7], a[8], a[9])
        context.restore()
        if applied_shadow:
            self.draw_image(self, *a)
        return '%s.drawImage()' %self.name

    @write_output
    def fill(self, context):
        """
        Helper method to fill the shape with a color, linear gradient,radial gradient,
        or pattern, and also apply shadows if needed
        """
        applied_shadow = False
        fill = self.attrs.fill
        if fill:
            context.save()
            if self.attrs.shadow and not self.applied_shadow:
                applied_shadow = self._applyShadow(context)
            s = fill.start
            e = fill.end
            f = None

            if isinstance(fill, basestring):
                context.fill_style = fill
                context.fill(context)
            elif fill.image:
                repeat = 'repeat' if not fill.repeat else fill.repeat
                if fill.scale:
                    context.scale(fill.scale.x, fill.scale.y)
                if fill.offset:
                    context.translate(fill.scale.x, fill.scale.y)
                context.fill_style = context.create_pattern(fill.image, repeat)
                context.fill(context)
            elif not(s.radius or e.radius):
                grd = context.create_linear_gradient(s.x, s.y, e.x, e.y)
                color_stops = fill.color_stops or []
                for n in xrange(0, len(color_stops),2):
                    grd.add_color_stop(color_stops[n], color_stops[n + 1])
                context.fill_style = grd
                context.fill(context)
            elif (s.radius or s.radius == 0) and (e.radius or e.radius == 0):
                grd = context.create_radial_gradient(s.x, s.y, s.radius, e.x, e.y, e.radius)
                color_stops = fill.color_stops

                for n in xrange(0, len(color_stops),2):
                    grd.add_color_stop(color_stops[n], color_stops[n + 1])
                context.fill_style = grd
                context.fill(context)
            else:
                context.fill_style = 'black'
                context.fill(context)
        context.restore()
        if applied_shadow:
            self.fill(context)
        return '%s.fill(%s)' %(self.name, Type.format(context))

    @write_output
    def fill_text(self, context, text):
        """Helper method to fill text and appy shadows if needed"""
        applied_shadow = False
        if self.attrs.text_fill:
            context.save()
            if self.attrs.shadow and not self.applied_shadow:
                applied_shadow = self._applyShadow(context)
            context.fill_style = self.attrs.text_fill
            context.fill_text(text, 0, 0)
            context.restore()
        if applied_shadow:
            self.fill_text(context, text, 0, 0)
        return '%s.fillText(%s, %s, 0, 0)' %(self.name, Type.format(context), Type.format(text))

    def get_canvas(self):
        """Get canvas tied to the layer"""
        return self.get_layer().get_canvas()

    def get_context(self):
        """Get canvas context tied to the layer"""
        return self.get_layer().get_context()

    def get_draw_func(self):
        """Get draw function"""
        return self.attrs.draw_func

    def get_fill(self):
        """Get fill"""
        return self.attrs.fill

    def get_line_join(self):
        """Get line join"""
        return self.attrs.line_join

    def get_shadow(self):
        """Get shadow object"""
        return self.attrs.shadow

    def get_stroke(self):
        """Get stroke color"""
        return self.attrs.stroke

    def get_stroke_width(self):
        """Get stroke width"""
        return self.attrs.stroke_width

    def intersects(self, x, y):
        """Determines if point is in the shape"""
        stage = self.get_stage()
        buffer_canvas = stage.buffer_canvas
        buffer_canvas.clean()
        self.__draw(buffer_canvas)
        p = buffer_canvas.context.get_image_data(round(x), round(y), 1, 1).data
        return p[3] > 0

    def set_draw_func(self, draw_func):
        """set draw function"""
        self.attrs.draw_func = draw_func

    @write_output
    def set_fill(self, fill):
        """Set fill which can be a color, linear gradient object, radial gradient object, or pattern object"""
        self.attrs.fill = fill
        return '%s.setFill(%s)' %(self.name, Type.format(fill))

    @write_output
    def set_line_join(self, line_join='miter'):
        """Set line join"""
        self.attrs.line_join = line_join
        return '%s.setLineJoin(%s)' %(self.name, Type.format(line_join))

    @write_output
    def set_stroke(self, stroke):
        """Set stroke color"""
        self.attrs.stroke = stroke
        return '%s.setStroke(%s)' %(self.name, Type.format(stroke))

    @write_output
    def set_stroke_width(self, stroke_width):
        """Set stroke width"""
        self.attrs.stroke_width = stroke_width
        return '%s.setStrokeWidth(%s)' %(self.name, Type.format(stroke_width))

    @write_output
    def stroke(self, context):
        """Helper method to stroke the shape and apply shadows if needed"""
        stroke_width = self.get_stroke_width()
        stroke = self.get_stroke()
        if stroke or stroke_width:
            applied_shadow = False

            context.save()
            if self.attrs.shadow and not self.applied_shadow:
                applied_shadow = self._applyShadow(context)
            context.line_width = stroke_width or 2
            context.stroke_style = stroke or 'black'
            context.stroke(context)
            context.restore()

            if applied_shadow:
                self.stroke(context)
        return '%s.stroke()' %self.name

    @write_output
    def stroke_text(self, context,  text, *args):
        """Helper method to stroke text and apply shadowsif needed"""
        applied_shadow = False

        if self.attrs.text_stroke or self.attrs.text_stroke_width:
            context.save()
            if self.attrs.shadow and not self.applied_shadow:
                applied_shadow = self._applyShadow(context)
            text_stroke = self.attrs.text_stroke or 'black'
            text_strike_width = self.attrs.text_stroke_width or 2
            context.line_width = text_strike_width
            context.stroke_style = text_stroke
            context.stroke_text(text, 0, 0)
            context.restore()

        if applied_shadow:
            self.stroke_text(context, text, 0, 0)

        return '%s.strokeText(%s)' %(self.name, Type.format(text))

    def __draw(self, canvas):
        if self.attrs.draw_func:
            stage = self.get_stage()
            context = canvas.get_context()
            family = []
            parent = self.parent

            family.insert(0, self)
            while parent:
                family.insert(0, parent)
                parent = parent.parent

            context.save()
            for n in xrange(len(family)):
                node = family[n]
                t = node.get_transform()
                m = t.get_matrix()
                context.transform(m[0], m[1], m[2], m[3], m[4], m[5])

            abs_opacity = self.get_absolute_opacity()
            if abs_opacity != 1:
                context.global_alpha = abs_opacity
            self.apply_line_join(context)

            self.applied_shadow = False

            wl = Kinetic.Global.BUFFER_WHITELIST
            bl = Kinetic.Global.BUFFER_BLACKLIST
            attrs = Storage()
            if canvas.name == 'buffer':
                for n in xrange(len(wl)):
                    key = wl[n]
                    attrs['key'] = self.attrs[key]
                    if (self.attrs[key]) or (key == 'fill' and not self.attrs.stroke and not('image' in self.attrs)):
                        self.attrs[key] = '#' + self.color_key

                for n in xrange(len(bl)):
                    key = bl[n]
                    attrs[key] = self.attrs[key]
                    self.attrs[key] = ''

                if 'image' in self.attrs.image:
                    attrs.image = self.attrs.image
                    if self.image_buffer:
                        self.attrs.image = self.image_buffer
                    else:
                        self.attrs.image = None
                        self.attrs.fill = '#' + self.color_key
                context.global_alpha = 1

            self.attrs.draw_func(self, canvas.get_context())

            if canvas.name == 'buffer':
                both_list = wl.extend(bl)
                for n in xrange(len(both_list)):
                    key = both_list[n]
                    self.attrs[key] = attrs[key]
                self.attrs.image = attrs.image
            context.restore()

    def _parse_shape_config(self, kwargs):
        if 'fill' in kwargs:
            if isinstance(kwargs['fill'], basestring):
                self.attrs.fill = kwargs['fill']
            else:
                self.attrs.fill = Storage()
                fill = kwargs['fill']
                if 'image' in fill:
                    self.attrs.fill.image = fill['image']
                if 'offset' in fill:
                    self.attrs.fill.offset = Storage()
                    if 'x' in fill['offset']:
                        self.attrs.fill.offset.x = round(fill['offset']['x'], 2)
                    if 'y' in fill['offset']:
                        self.attrs.fill.offset.y = round(fill['offset']['y'], 2)
                if 'start' in fill:
                    self.attrs.fill.start = Storage()
                    if 'x' in fill['start']:
                        self.attrs.fill.start.x = round(fill['start']['x'], 2)
                    if 'y' in fill['start']:
                        self.attrs.fill.start.y = round(fill['start']['y'], 2)
                    if 'radius' in fill['start']:
                        self.attrs.fill.start.radius = fill['start']['radius']
                if 'end' in fill:
                    self.attrs.fill.end = Storage()
                    if 'x' in fill['end']:
                        self.attrs.fill.end.x = round(fill['end']['x'], 2)
                    if 'y' in fill['start']:
                        self.attrs.fill.end.y = round(fill['end']['y'], 2)
                    if 'radius' in fill['end']:
                        self.attrs.fill.end.radius = fill['end']['radius']
        if 'stroke' in kwargs:
            self.attrs.stroke = kwargs['stroke']
        if 'stroke_width' in kwargs:
            self.attrs.stroke_width = round(kwargs['stroke_width'], 2)
        if 'line_join' in kwargs and kwargs['line_join'] in ['miter', 'round', 'bevel']:
            self.attrs.line_join = kwargs['line_join']
        else:
            self.attrs.line_join = 'mitter'
        if 'shadow' in kwargs:
            self.attrs.shadow = Storage()
            shadow = kwargs['shadow']
            if 'color' in shadow:
                self.attrs.shadow.color = shadow['color']
            if 'blur' in shadow:
                if Type.is_number(shadow['blur']):
                    self.attrs.shadow.blur = round(shadow['blur'], 2)
                else:
                    if 'offset' in shadow['blur']:
                        self.attrs.shadow.blur = Storage({'offset': Storage()})
                        if 'x' in shadow['blur']['offset']:
                            self.attrs.shadow.blur.offset.x = round(shadow['blur']['offset']['x'], 2)
                        if 'y' in shadow['blur']['offset']:
                            self.attrs.shadow.blur.offset.y = round(shadow['blur']['offset']['y'], 2)

    def _applyShadow(self, context):
        """Apply shadow.  return true if shadow was applied and false if it was not"""
        s = self.attrs.shadow
        if s:
            aa = self.get_absolute_opacity()
            color = s.color if s.color else 'black'
            blur = s.blur if s.blur else 5
            offset = s.offset if s.offset else Storage({ 'x': 0, 'y': 0 })
            if s.opacity:
                context.global_alpha = s.opacity * aa
            context.shadow_color = color
            context.shadow_blur = blur
            context.shadow_offset_x = offset.x
            context.shadow_offset_y = offset.y
            self.applied_shadow = True

            return True
        return False

if __name__ == '__main__':
    shape = Shape('shape', x=10, y=11, fill='abc', shadow= {'color': '#ccc', 'blur': { 'offset': { 'x': 10}}})
    from util.global_options import write_to_file
    write_to_file('kin.js')

