__author__ = 'Vlad'

from util.global_options import write_output
from shape import Shape
from util.type import Type
from util.storage import Storage

class Image(Shape):
    def __init__(self, name, **kwargs):
        super(Image, self).__init__(**kwargs)

        self.name = name
        self.shape_type = 'Image'
        self.filter = None

        self.default.radius = 0.0
        self.set_default_attrs(self.default)

        self._parse_image_config(kwargs)

        self._make_constructor()

    def _parse_image_config(self, kwargs):
        if 'image' in kwargs:
            self.attrs.image = kwargs['image']
        if 'width' in kwargs:
            self.attrs.width = kwargs['width']
        if 'height' in kwargs:
            self.attrs.height = kwargs['height']
        if 'crop' in kwargs:
            self.attrs.crop = Storage()
            if 'x' in kwargs['crop']:
                self.attrs.crop.x = round(kwargs['crop']['x'], 2)
            if 'y' in kwargs['crop']:
                self.attrs.crop.y = round(kwargs['crop']['y'], 2)
            if 'width' in kwargs['crop']:
                self.attrs.crop.width = round(kwargs['crop']['width'], 2)
            if 'height' in kwargs['crop']:
                self.attrs.crop.height = round(kwargs['crop']['height'], 2)

    @write_output
    def apply_filter(self, config):
        """Apply filter"""
        self.filter = Storage(config)
        return '%s.applyFilter(%s)' %(self.name, Type.format(config))

    @write_output
    def clear_image_buffer(self, callback):
        """
        Create image buffer which enables more accurate hit detection mapping of the image
        by avoiding event detections for transparent pixels
        """
        return '%s.createImageBuffer(%s)' %(self.name, callback)

    def get_croop(self):
        """Get crop"""
        return self.attrs.crop

    def get_filter(self):
        """Get filter"""
        return self.filter

    def get_height(self):
        """Get height"""
        return self.attrs.height

    def get_image(self):
        """Get image"""
        return self.attrs.image

    def get_size(self):
        """return image size"""
        return Storage({
            'width': self.attrs.width,
            'height': self.attrs.height,
        })

    def get_width(self):
        """Get width"""
        return self.attrs.width

    @write_output
    def set_crop(self, crop):
        """Set crop"""
        if not self.attrs.crop:
            self.attrs.crop = Storage
        if 'x' in crop:
            self.attrs.crop.x = round(crop['x'], 2)
        if 'y' in crop:
            self.attrs.crop.y = round(crop['y'], 2)
        if 'width' in crop:
            self.attrs.crop.width = round(crop['width'], 2)
        if 'height' in crop:
            self.attrs.crop.height = round(crop['height'], 2)
        return '%s.setCrop(%s)' %(self.name, Type.format(self.attrs.crop))

    @write_output
    def set_filter(self, config):
        """Set filter"""
        self.filter = Storage(config)
        return '%s.setFilter(%s)' %(self.name, Type.format(config))

    @write_output
    def set_height(self, height):
        """Set height"""
        self.attrs.height = round(height, 2)
        return '%s.setHeight(%s)' %(self.name, Type.format(self.attrs.height))

    @write_output
    def set_image(self, image):
        """Set image"""
        self.attrs.image = image
        return '%s.setImage(%s)' %(self.name, image)

    @write_output
    def set_size(self, width, height):
        """Set width and height"""
        self.attrs.width = round(width, 2)
        self.attrs.height = round(height, 2)
        return '%s.setSize(%s, %s)' %(self.name, Type.format(self.attrs.width), Type.format(self.attrs.height))

    @write_output
    def set_width(self, width):
        """Set width"""
        self.attrs.width = round(width, 2)
        return '%s.setWidth(%s)' %(self.name, Type.format(self.attrs.width))
