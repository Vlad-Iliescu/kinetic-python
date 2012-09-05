__author__ = 'Vlad'

from util.global_options import write_output, Kinetic
from shape import Shape
from util.type import Type
from util.storage import Storage

class Sprite(Shape):
    def __init__(self, name, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.default.index = 0
        self.default.frame_rate = 17
        self.set_default_attrs(self.default)

        self.name = name
        self.shape_type = 'Sprite'
        self.after_frame_index = None
        self.after_frame_func = None
        self.anonymus = False

        self._parse_sprite_config(kwargs)
        self._make_constructor()

    @write_output
    def after_frame(self, index, func='', anonymus_func=True):
        """Set after frame event handler"""
        self.after_frame_index = index
        self.after_frame_func = func
        if anonymus_func:
            self.anonymus = True
            Kinetic.Global.tab += 1
            return '%s.afterFrame(%d, function() {' %(self.name, index)
        return '%s.afterFrame(%d, %s);' %(self.name, index, func)

    @write_output
    def end_after_frame(self):
        if self.anonymus:
            Kinetic.Global.tab -= 1
            return '});'
        return ''

    def get_animation(self):
        """Get animation key"""
        return self.attrs.animation

    def get_animations(self):
        """Get animations object"""
        return self.attrs.animations

    def get_index(self):
        """Get animation frame index"""
        return self.attrs.index

    @write_output
    def set_animation(self, anim):
        """Set animation key"""
        self.attrs.animation = anim
        return '%s.setAnimation(%s);' %(self.name, Type.format(anim))

    @write_output
    def set_animations(self, animations):
        """Set animations obect"""
        self.attrs.animations = Storage(animations)
        return '%s.setAnimations(%s);' %(self.name, Type.format(self.attrs.animations))

    @write_output
    def set_index(self, index):
        """Set animation frame index"""
        self.attrs.index = index
        return '%s.setIndex(%d);' %(self.name, index)

    @write_output
    def start(self):
        """Start sprite animation"""
        return '%s.start();' %self.name

    @write_output
    def stop(self):
        """Stop sprite animation"""
        return '%s.stop();' %self.name

    def _parse_sprite_config(self, kwargs):
        if 'image' in kwargs:
            self.attrs.image = kwargs['image']
        else:
            raise NameError('parameter "image" is required')
        if 'animations' in kwargs:
            self.attrs.animations = Storage(kwargs['animations'])
        else:
            raise NameError('parameter "animations" is required')
        if 'animation' in kwargs:
            self.attrs.animation = kwargs['animation']
        else:
            raise NameError('parameter "animation" is required')
        if 'frame_rate' in kwargs:
            self.attrs.frame_rate = kwargs['frame_rate']