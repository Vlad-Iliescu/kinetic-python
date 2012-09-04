__author__ = 'Vlad'

from container import Container
from util.storage import Storage
from util.type import Type
from util.global_options import Kinetic, write_output

class Stage(Container):
    def __init__(self, stage_name, **kwargs):
        """ Creates a new Stage()

        Keyword arguments:
        x -- the x coord (default 0)
        y -- the y coord (default 0)
        visible -- is the stage visible or not (default True)
        listening -- whether or not the node is listening for events (default True)
        id -- unique id
        name -- non-unique name
        opacity  -- determines node opacity. Can be any number between 0 and 1 (default 1)
        scale -- the scale to resize (default (1,1))
        rotation -- rotation in radians
        rotation_deg -- rotation in degrees
        offset -- offsets default position point and rotation point (default (0,0))
        draggable -- is dragable or not (default False)
        drag_constraint -- can be vertical, horizontal, or none (default 'none')
        drag_bounds -- drag bounds (top, right, bottom, left)
        """
        super(Stage, self).__init__(**kwargs)

        self.default['width'] = 400.0
        self.default['height'] = 200.0
        self.set_default_attrs(self.default)

        self._set_stage_default_proprieties()
        self.content = []
        self.name = stage_name

        self.ids = Storage()
        self.names = Storage()

        self._parse_stage_config(kwargs)
        self._make_constructor()

    @write_output
    def clear(self):
        """Clear all layers"""
        layers = self.children
        for n in xrange(len(layers)):
            layers[n].clear()
        return '%s.clear();' %self.name

    @write_output
    def draw(self):
        """Draw children"""
        self._draw()
        return '%s.draw();' %self.name

    def get_container(self):
        """Get container DOM element"""
        return self.attrs.container

    def get_dom(self):
        """Get stage DOM node, which is a div element with the class name "kineticjs-content" """
        return '%s.getDOM();' %self.name

    def get_intersection(self, x, y):
        """Get intersection object that contains shape and pixel data"""
        layers = self.get_children()
        for i in xrange(len(layers)-1, -1, -1):
            layer = layers[n]
            p = layer.buffer_canvas.context.get_image_data(round(x), round(y), 1, 1).data
            if p[3] == 255:
                color_key = Type.rgb_to_hex(p[0], p[1], p[2])
                shape = Kinetic.Global.shapes[color_key]
                return Storage({
                    'shape': shape,
                    'pixel': p
                })
            elif p[0] > 0 or p[1] > 0 or p[2] > 0 or p[3] > 0:
                return Storage({
                    'pixel': p
                })
        return None

    def get_mouse_position(self, evt):
        """Get mouse position for desktop apps"""
        return '%s.getMousePosition(%s);' %(self.name, evt)

    def get_size(self):
        """Get stage size"""
        return Storage({
            'width': self.attrs.width,
            'height': self.attrs.height
        })

    def get_stage(self):
        """Get stage"""
        return self

    def get_touch_position(self, evt):
        """Get touch position for mobile apps"""
        return '%s.getTouchPosition(%s);' %(self.name, evt)

    def get_user_position(self, evt):
        """Get user position (mouse position or touch position)"""
        return '%s.getUserPosition(%s);' %(self.name, evt)

    def get_width(self):
        """Get height"""
        return self.attrs.width

    @write_output
    def reset(self):
        """Reset stage to default state"""
        self.remove_children()
        self._set_stage_default_proprieties()
        self.set_default_attrs(self.default)
        return '%s.reset();' %self.name

    @write_output
    def set_height(self, height):
        """Set height"""
        self.attrs.height = round(height, 2)
        return '%s.setHeight(%s);' %(self.name, Type.format(self.attrs.height))

    def get_height(self):
        """Get height"""
        return self.attrs.height

    @write_output
    def set_size(self, width,  height):
        """Set stage size"""
        self.set_width(width)
        self.set_height(height)
        return '%s.setSize(%s, %s);' %(self.name, Type.format(self.attrs.width), Type.format(self.attrs.height))

    @write_output
    def set_width(self, width):
        """Set width"""
        self.attrs.width = round(width, 2)
        return '%s.setHeight(%s);' %(self.name, Type.format(self.attrs.width))

    def _parse_stage_config(self, kwargs):
        if 'width' in kwargs:
            self.attrs.width = round(kwargs['width'], 2)
        if 'height' in kwargs:
            self.attrs.height = round(kwargs['height'], 2)
        if 'container' in kwargs:
            self.attrs.container = kwargs['container']

    def _set_stage_default_proprieties(self):
        self.node_type = 'Stage'
        self.dbl_click_window = 400.0
        self.target_shape = None
        self.mouse_pos = None
        self.click_start = None
        self.touch_pos = None
        self.tap_start = False

    def _add(self, layer):
        """Add layer to stage"""
        layer.canvas.set_size(self.attrs.width, self.attrs.height)
        layer.buffer_canvas.set_size(self.attrs.width, self.attrs.height)

#        layer.draw()
        self.content.append(layer.canvas.element)

    def _add_id(self, node):
        if node.attrs.id is not None:
            self.ids[node.attrs.id] = node

    def _remove_id(self, id):
        if id is not None:
            if id in self.ids:
                del self.ids[id]

    def _add_name(self, node):
        name = node.attrs.name
        if name is not None:
            if self.name[name]:
                self.names[name] = []
            self.names[name].append(node)

    def _remove_name(self, name, _id=None):
        if name is not None:
            nodes = self.names[name]
            if nodes:
                while n < len(nodes):
                    no = nodes[n]
                    if id(no) == _id:
                        del nodes[n]
                    else:
                        n += 1
                if len(nodes):
                    del self.names[name]

if __name__ == '__main__':
    stage = Stage('stage', container='container', width = 578, height=200)
    stage.clear()
    from util.global_options import write_to_file
    write_to_file('kin.js')
