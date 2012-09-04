__author__ = 'Vlad'

from container import Container
from util.canvas import Canvas
from util.type import Type
from util.global_options import write_output

class Layer(Container):
    def __init__(self, var_name, **kwargs):
        super(Layer, self).__init__(**kwargs)

        self.default.clear_before_draw = True
        self.set_default_attrs(self.default)

        self.name = var_name
        self.node_type = "Layer"
        self.before_draw_func = None
        self.after_draw_func = None

        self.canvas = Canvas(None)
        self.canvas.get_element().style.position = 'absolute'
        self.buffer_canvas = Canvas(None)
        self.buffer_canvas.name = 'buffer'

        self._parse_layer_config(kwargs)
        self._make_constructor()

    def after_draw(self, handler):
        """Set after draw handler"""
        pass

    def before_draw(self, handler):
        """Set before draw handler"""
        pass

    @write_output
    def clear(self):
        """Clear canvas tied to the layer"""
        return '%s.getCanvas().clear();' %self.name

    @write_output
    def draw(self, canvas=None):
        """Draw children nodes. this includes any groups or shapes"""
        if self.before_draw_func is not None:
            self.before_draw_func(self)

        if canvas:
            self._draw(canvas)
        else:
            self._draw(self.get_canvas())
            self._draw(self.buffer_canvas)

        if self.after_draw_func is not None:
            self.after_draw_func(self)

        return '%s.draw()' % self.name

    @write_output
    def draw_buffer(self):
        """Draw children nodes on buffer. this includes any groups or shapes"""
        self.draw(self.buffer_canvas)
        return '%s.drawBuffer()' %self.name

    @write_output
    def draw_scene(self):
        """Draw children nodes on scene. this includes any groups or shapes"""
        self.draw(self.get_canvas())
        return '%s.drawScene()' %self.name

    def get_canvas(self):
        """Get layer canvas"""
        return self.canvas

    def get_clear_before_draw(self):
        """Get flag which determines if the layer is cleared or not before drawing"""
        return self.attrs.clear_before_draw

    def get_context(self):
        """Get layer canvas context"""
        return self.canvas.context

    @write_output
    def set_clear_before_draw(self, clear_before_draw):
        """Set flag which determines if the layer is cleared or not before drawing"""
        self.attrs.clear_before_draw = bool(clear_before_draw)
        return '%s.setClearBeforeDraw(%s)' %(self.name, Type.format(self.attrs.clear_before_draw))

    def _parse_layer_config(self, kwargs):
        if 'clear_before_draw' in kwargs:
            self.attrs.clear_before_draw = bool(kwargs['clear_before_draw'])

    def _remove(self):
        """Remove layer from stage"""
        try:
            self.get_stage().content.remove_child(self.canvas.element)
        except Exception as e:
            pass

    def __draw(self, canvas):
        if self.attrs.clear_before_draw:
            canvas.clear()



if __name__ == '__main__':
    l = Layer('layer')
    from util.global_options import write_to_file
    write_to_file('kin.js')