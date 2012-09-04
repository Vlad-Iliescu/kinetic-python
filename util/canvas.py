__author__ = 'Vlad'

from storage import Storage
from type import Type

class Canvas():
    def __init__(self, name, width=0, height=0):
        self.element = Storage()
        self.element.width = round(width, 2)
        self.element.height = round(height, 2)
        self.element.style = Storage()

        self.context = Storage()

        self.name = name
#        self.parent_name = parent.name

    def clear(self):
        """Clear canvas"""
        return '%s.clear();' %self.name

    def get_element(self):
        return self.element

    def get_context(self):
        """Get context"""
        return self.context

    def set_width(self, width):
        """Set width"""
        self.element.width = round(width, 2)
        return '%s.setWidth(%s)' %(self.name, Type.format(self.element.width))

    def set_height(self, height):
        """Set height"""
        self.element.height = round(height, 2)
        return '%s.setHeight(%s)' %(self.name, Type.format(self.element.height))

    def get_width(self):
        """Get width"""
        return self.element.width

    def get_height(self):
        """Get height"""
        return self.element.height

    def set_size(self, width, height):
        """Set size"""
        self.set_width(width)
        self.set_height(height)
        return '%s.setSize(%s, %s)' %(self.name, Type.format(self.element.width),
                                                  Type.format(self.element.height))