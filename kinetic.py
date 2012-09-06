__author__ = 'Vlad'

from util.global_options import Kinetic, write_to_file, begin_block, end_block
from shapes.rect import Rect
from shapes.circle import Circle
from shapes.ellipse import Ellipse
from shapes.image import Image as _Image
from shapes.sprite import Sprite
from shapes.text import Text
from stage import Stage
from layer import Layer

Kinetic.Stage = Stage
Kinetic.Layer = Layer
Kinetic.Rect = Rect
Kinetic.Circle = Circle
Kinetic.Ellipse = Ellipse
Kinetic.Image = _Image
Kinetic.Sprite = Sprite
Kinetic.Text = Text

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
#    animations = {'idle': [{'x': 2, 'y': 2, 'width': 70, 'height': 119}, {'x': 71, 'y': 2, 'width': 74, 'height': 119},
#            {'x': 146, 'y': 2, 'width': 81, 'height': 119}, {'x': 226, 'y': 2, 'width': 76, 'height': 119}],
#                  'punch': [{ 'x': 2, 'y': 138, 'width': 74, 'height': 122}, {'x': 76, 'y': 138, 'width': 84, 'height': 122},
#                          {'x': 346, 'y': 138, 'width': 120, 'height': 122}] }
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

    t = """COMPLEX TEXT\\n\\n All the world\'s a stage, and all the men and women merely players. They have their exits and their entrances."""
    text = Kinetic.Text('text', x=190, y=15, text="Simple Text", font_size=30, font_family="Calibri", text_fill='green')
    text2 = Kinetic.Text('t2', x=100, y=60, stroke='#555', text=t, font_size=14, font_family='Calibri', text_fill='#555',
                        width=380, padding=20, align='center', font_style='italic',
                        shadow={'color': 'black', 'blur': 1, 'offset': {'x': 10, 'y': 10}, 'opacity': 0.2},
                        corner_radius=10, fill='#DDD')
    layer.add(text)
    layer.add(text2)
    stage.add(layer)


    write_to_file('kin.js')

