__author__ = 'Vlad'

from util.global_options import Kinetic, write_to_file, begin_block, end_block
from shapes.rect import Rect
from shapes.circle import Circle
from shapes.ellipse import Ellipse
from shapes.image import Image as _Image
from shapes.sprite import Sprite
from stage import Stage
from layer import Layer

Kinetic.Stage = Stage
Kinetic.Layer = Layer
Kinetic.Rect = Rect
Kinetic.Circle = Circle
Kinetic.Ellipse = Ellipse
Kinetic.Image = _Image
Kinetic.Sprite = Sprite

if __name__ == '__main__':
    stage = Kinetic.Stage('stage', container='container', width=578, height=200)
    layer = Kinetic.Layer('layer')
#    rect = Kinetic.Rect('rect', x=239, y=75, width=100, height=50, fill='#00D2FF', stroke='black', stroke_width=4)
#    layer.add(rect)
#    circle = Kinetic.Circle('circle', x=stage.get_width()/2, y=stage.get_height()/2, radius=70, fill='red',
#                            stroke='black', stroke_width=4)
#    layer.add(circle)
#    ellipse = Kinetic.Ellipse('ellipse', x=stage.get_width()/2, y=stage.get_height()/2, radius={'x':100, 'y':50},
#                              fill='yellow', stroke='black', stroke_width=4)
#    layer.add(ellipse)
    from util.image import Image
    animations = {'idle': [{'x': 2, 'y': 2, 'width': 70, 'height': 119}, {'x': 71, 'y': 2, 'width': 74, 'height': 119},
            {'x': 146, 'y': 2, 'width': 81, 'height': 119}, {'x': 226, 'y': 2, 'width': 76, 'height': 119}],
                  'punch': [{ 'x': 2, 'y': 138, 'width': 74, 'height': 122}, {'x': 76, 'y': 138, 'width': 84, 'height': 122},
                          {'x': 346, 'y': 138, 'width': 120, 'height': 122}] }
#    img = Image('img')
#    img.onload()

    #    yoda = Kinetic.Image('yoda', x=140, y=stage.get_height()/2 - 59, image=img, width=106, height=118)
    #    layer.add(yoda)

#    sprite = Kinetic.Sprite('sprite', x=250, y=40, image=img, animations=animations, frame_rate=7, animation='idle')
#    layer.add(sprite)
#    stage.add(layer)
#    sprite.start()
#    begin_block('document.getElementById("punch").addEventListener("click", function() {')
#    sprite.set_animation('punch')
#    sprite.after_frame(2)
#    sprite.set_animation('idle')
#    sprite.end_after_frame()
#    end_block('}, false);')
#
#    img.end_onload()
#    img.src('http://www.html5canvastutorials.com/demos/assets/blob-sprite.png')

    write_to_file('kin.js')

