__author__ = 'Vlad'

from math import cos, sin
from storage import Storage

class Transform(object):
    """Simple class for keeping track of the current transformation matrix"""

    def __init__(self, src=None):
        if isinstance(src, Transform):
            self.m = src.m[:]
        else:
            self.reset()

    def __str__(self):
        return str(self.m)

    def reset(self):
        """Reset the transform to identity"""
        self.m = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]

    def clone(self):
        """Clone transform"""
        return Transform(self)

    def multiply(self, matrix):
        """Transform multiplication"""
        m11 = self.m[0] * matrix.m[0] + self.m[2] * matrix.m[1]
        m12 = self.m[1] * matrix.m[0] + self.m[3] * matrix.m[1]

        m21 = self.m[0] * matrix.m[2] + self.m[2] * matrix.m[3]
        m22 = self.m[1] * matrix.m[2] + self.m[3] * matrix.m[3]

        dx = self.m[0] * matrix.m[4] + self.m[2] * matrix.m[5] + self.m[4]
        dy = self.m[1] * matrix.m[4] + self.m[3] * matrix.m[5] + self.m[5]

        self.m = [m11, m12, m21, m22, dx, dy]

        return self

    def invert(self):
        """Inverts the transform"""
        d = 1.0 / (self.m[0] * self.m[3] - self.m[1] * self.m[2])
        m0 = self.m[3] * d
        m1 = -self.m[1] * d
        m2 = -self.m[2] * d
        m3 = self.m[0] * d
        m4 = d * (self.m[2] * self.m[5] - self.m[3] * self.m[4])
        m5 = d * (self.m[1] * self.m[4] - self.m[0] * self.m[5])
        self.m = [m0, m1, m2, m3, m4, m5]

        return self

    def rotate(self, rad):
        """Apply rotation"""
        c = cos(rad)
        s = sin(rad)
        m11 = self.m[0] * c + self.m[2] * s
        m12 = self.m[1] * c + self.m[3] * s
        m21 = self.m[0] * -s + self.m[2] * c
        m22 = self.m[1] * -s + self.m[3] * c
        self.m[0] = m11
        self.m[1] = m12
        self.m[2] = m21
        self.m[3] = m22

        return self

    def translate(self, x, y):
        """Apply translation"""
        self.m[4] += self.m[0] * x + self.m[2] * y
        self.m[5] += self.m[1] * x + self.m[3] * y

        return self

    def scale(self, sx, sy):
        """Apply scale"""
        self.m[0] *= sx
        self.m[1] *= sx
        self.m[2] *= sy
        self.m[3] *= sy

        return self

    def transform_point(self, px, py):
        """Transform a point"""
        x = px
        y = py
        px = x * self.m[0] + y * self.m[2] + self.m[4]
        py = x * self.m[1] + y * self.m[3] + self.m[5]
        return Storage({ x: px, y: py })

    def get_translation(self):
        """Returns the translation"""
        return  Storage({ 'x': self.m[4], 'y': self.m[5] })

    def has_rotation(self):
        """Determines if the transform has rotation"""
        return  self.m[1] != 0
