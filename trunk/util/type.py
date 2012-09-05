__author__ = 'Vlad'

from storage import Storage
from random import randint
#from util.image import Image

class Type():

    @classmethod
    def is_number(cls, number):
        return isinstance(number, (int, float, long))

    @classmethod
    def pep_to_js(cls, col):
        cols = {
            'rotation_deg': 'rotationDeg',
            'drag_constraint': 'dragConstraint',
            'drag_bounds': 'dragBounds',
            'stroke_width': 'strokeWidth',
            'line_join': 'lineJoin',
            'draw_func': 'drawFunc',
            'clear_before_draw': 'clearBeforeDraw',
            'corner_radius': 'cornerRadius',
            'frame_rate': 'frameRate'
        }
        if col in cols:
            return cols[col]
        return col

    @classmethod
    def format(cls, val):
        if isinstance(val, basestring):
            return '"%s"' %val
        elif isinstance(val, bool):
            return '%s' %('true' if val else 'false')
        elif isinstance(val, (dict, Storage)):
            _s = []
            for i in val:
                _s.append('%s: %s' %(Type.pep_to_js(i), Type.format(val[i])))
            return '{%s}' %', '.join(_s)
        elif Type.is_number(val):
            return  '%r' %val
        elif isinstance(val, (list, tuple)):
            _s = []
            for i in val:
                _s.append('%s' %Type.format(i))
            return '[%s]' % ', '.join(_s)
        elif val is None:
            return 'undefined'
        else:
            return '%s' %val


    @classmethod
    def rgb_to_hex(cls, r, g, b):
        return hex((1 << 24) + (r << 16) + (g << 8) + b)[3:]

    @classmethod
    def get_random_color_key(cls):
        r = randint(1, 255)
        g = randint(1, 255)
        b = randint(1, 255)
        return cls.rgb_to_hex(r, g, b)

