__author__ = 'Vlad'

from storage import Storage
from global_options import write_output, Kinetic
from type import Type

class Image(object):
    def __init__(self, name, **kwargs):
        self._js = ''
        self.name = name
        self._const = Storage()
        self.attrs = Storage()

        self.anonymus_onload = False

        self._parse_image_args(kwargs)
        self._make_constructor()

    def __str__(self):
        return self.name

    @write_output
    def src(self, src):
        self.attrs.src = src
        return '%s.src = %s;' %(self.name, Type.format(src))

    @write_output
    def onload(self, anonymous=True, function_name=''):
        if anonymous:
            self.anonymus_onload = True
            Kinetic.Global.tab += 1
            return '%s.onload = function() {' %self.name
        elif function_name:
            self.anonymus_onload = False
            return '%s.onload = %s' %(self.name, function_name)
        return ''

    @write_output
    def end_onload(self):
        if self.anonymus_onload:
            Kinetic.Global.tab -= 1
            return '};'
        return ''

    def _parse_image_args(self, kwargs):
        if 'src' in kwargs:
            self.attrs.src = self._const.src =  kwargs['src']

    @write_output
    def _make_constructor(self):
        self._js = 'var %s = new %s(%s);' %(self.name, self.__class__.__name__, Type.format(self._const))
        return self._js
