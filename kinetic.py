__author__ = 'Vlad'

from util.global_options import Kinetic, write_to_file
from shapes.rect import Rect
from stage import Stage
from layer import Layer

Kinetic.Rect = Rect
Kinetic.Stage = Stage
Kinetic.Layer = Layer

if __name__ == '__main__':
    stage = Kinetic.Stage('stage', container='container', width=578, height=200)
    layer = Kinetic.Layer('layer')
    rect = Kinetic.Rect('rect', x=239, y=75, width=100, height=50, fill='#00D2FF', stroke='black', stroke_width=4)
    layer.add(rect)
    stage.add(layer)
    write_to_file('kin.js')

