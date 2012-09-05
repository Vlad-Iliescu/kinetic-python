__author__ = 'Vlad'

from storage import Storage
from functools import wraps
from cStringIO import StringIO

def _pull_nodes(stage):
    temp_nodes = Kinetic.Global.temp_nodes
    for key in temp_nodes:
        node = temp_nodes[key]
        if node.get_stage() is not None and id(node.get_stage()) == id(stage):
            stage._add_id(node)
            stage._add_name(node)
            Kinetic.Global._remove_temp_node(node)

Kinetic = Storage()
Kinetic.Filters = Storage()
Kinetic.Plugins = Storage()
Kinetic.Global = Storage({
    'BUBBLE_WHITELIST': ['mousedown', 'mousemove', 'mouseup', 'mouseover', 'mouseout', 'click', 'dblclick',
                       'touchstart', 'touchmove', 'touchend', 'tap', 'dbltap', 'dragstart', 'dragmove', 'dragend'],
    'BUFFER_WHITELIST': ['fill', 'stroke', 'text_fill', 'text_stroke'],
    'BUFFER_BLACKLIST': ['shadow'],
    'id_counter': 0,
    'temp_nodes': Storage(),
    '_add_temp_node': lambda node : Kinetic.Global.temp_nodes.update({id(node): node}),
    '_remove_temp_node' : lambda node : Kinetic.Global.temp_nodes.update({id(node): None}),
    '_pull_nodes': _pull_nodes,
    'Shapes': Storage(),
    'filename': StringIO(),
    'tab': 1
})

def write_output(fn, file=Kinetic.Global.filename):
    @wraps(fn)
    def wrapper(*args, **kw):
        result = fn(*args, **kw)
        file.write('\t'*Kinetic.Global.tab+result+"\n")
        return result
    return wrapper

def begin_block(js='{', file=Kinetic.Global.filename):
    file.write('\t'*Kinetic.Global.tab+js+"\n")
    Kinetic.Global.tab += 1

def end_block(js='}', file=Kinetic.Global.filename):
    Kinetic.Global.tab -= 1
    file.write('\t'*Kinetic.Global.tab+js+"\n")


def write_to_file(file):
    file = open(file, 'wb')
    io = Kinetic.Global.filename
    io.seek(0)
    file.write('window.onload = function() {\n')
    file.write(io.read())
    file.write('};')
    file.close()

