__author__ = 'Vlad'

from math import radians, degrees
from util.transform import Transform
from util.storage import Storage
from util.type import Type
from util.global_options import write_output


class Node(object):
    def __init__(self, var_name=None,  **kwargs):
        """ Node constructor.  Nodes are entities that can be transformed,
        layered,and have events bound to them.
        They are the building blocks of a KineticJSapplication

        Keyword arguments:
        x               -- {Number} x coord (default 0)
        y               -- {Number} y coord (default 0)
        visible         -- {Boolean} (default True)
        listening       -- {Boolean} whether or not the node is listening for events (default True)
        id              -- {String} unique id (default None)
        name            -- {String} non-unique name (default None)
        opacity         -- {Number} determines node opacity. Can be any number between 0 and 1 (default 1)
        scale           -- {Dict} (default {'x': 1, 'y': 1})
            scale.x             -- {Number}(default 1)
            scale.y             -- {Number}(default 1)
        rotation        -- {Number} rotation in radians (default 0)
        rotation_deg    -- {Number} rotation in degrees (default 0)
        offset          -- {Dict} offsets default position point and rotation point (default {'x': 0, 'y': 0})
            offset.x            -- {Number} (default 0)
            offset.y            -- {Number} (default 0)
        draggable       -- {Boolean} (default False)
        drag_constraint -- {String} can be vertical, horizontal, or none (default "none")
        drag_bounds     -- {Dict} (default {})
             drag_bounds.top    -- {Number} (Optional)
             drag_bounds.right  -- {Number} (Optional)
             drag_bounds.bottom -- {Number} (Optional)
             drag_bounds.left   -- {Number} (Optional)
        """
        self.attrs = None
        self.default = Storage({
            'visible': True,
            'listening': True,
            'name': None,
            'opacity': 1.0,
            'x': 1.0,
            'y': 1.0,
            'scale': Storage({
                'x': 1.0,
                'y': 1.0
            }),
            'rotation': 0.0,
            'offset': Storage({
                'x': 0.0,
                'y': 0.0
            }),
            'drag_constraint': 'none',
            'drag_bounds': Storage(),
            'draggable': False
        })
        self.set_default_attrs(self.default)

        self.event_listeners = Storage()
        self._js = ''

        self.name = var_name
        self.class_name = 'Node'

        self.parent = None
        self.node_type = None
        self.index = None

        self._parse_node_config(kwargs)
        if self.name:
            self._make_constructor()

    def __str__(self):
        return self._js

    def set_default_attrs(self, config):
        """Set default attrs. This method should only be used if you're creating a custom node"""
        if not self.attrs:
            self.attrs = Storage()
        if config:
            for key in config:
                if not self.attrs[key]:
                    if isinstance(config[key], (dict, Storage)):
                        self.attrs[key] = Storage(config[key])
                        continue
                    self.attrs[key] = config[key]

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        """Get parent container"""
        return self.parent

    def clone(self, name, attrs):
        """Clone node"""
        c_attrs = self.attrs.copy()
        c_attrs.update(attrs)
        return Node(name, **c_attrs)

    def get_absolute_opacity(self):
        """Get absolute opacity"""
        abs_opacity = 1
        node = self
        while node.node_type != 'Stage':
            abs_opacity *= node.attrs.opacity
            node = node.parent
        return abs_opacity

    def get_absolute_position(self):
        """Get absolute position"""
        trans = self.get_absolute_transform()
        o = self.get_offset()
        trans.translate(o.x, o.y)
        return trans.get_translation()

    def get_absolute_transform(self):
        """Get absolute transform of the node which takes into account its parent transforms"""
        am = Transform()
        family = []
        parent = self.parent
        family.insert(0, self)
        while parent:
            family.insert(0, parent)
            parent = parent.parent

        for n in xrange(len(family)):
            node = family[n]
            m = node.get_transform()
            am.multiply(m)

#        return '%s.getAbsoluteTransform()' %self.name
        return am

    def get_absolute_zindex(self):
        """Get absolute z-index which takes into account sibling and parent indices"""
        level = self.get_level()
        index = 0
        def add_children(children):
            nodes = []
            n = 0
            while n < len(children):
                child = children[n]
                index += 1

                if child.node_type != 'Shape':
                    nodes.extend(child.get_children())

                if id(child) == id(self):
                    n =  len(children)
                n += 1
            if len(nodes) > 0 and nodes[0].get_level() <= level:
                add_children(nodes)
        if self.node_type != 'Stage':
            add_children(self.get_stage().get_children())

        return index

    def get_attrs(self):
        """Get attrs"""
        return self.attrs

    def get_drag_bounds(self):
        """Get drag bounds"""
        return self.attrs['drag_bounds']

    def get_drag_constraint(self):
        """Get drag constraint"""
        return self.attrs['drag_constraint']

    def get_dragable(self):
        """Get draggable"""
        return self.attrs['draggable']

    def get_id(self):
        """Get ID"""
        return self.attrs['id']

    def get_layer(self):
        """Get layer that contains the node"""
        if self.node_type == 'Layer':
            return self
        else:
            return self.get_parent().get_layer()

    def get_level(self):
        """Get node level in node tree"""
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level

    def get_listening(self):
        """Determine if listening to events or not"""
        return self.attrs['listening']

    def get_name(self):
        """Get name"""
        return self.attrs['name']

    def get_offset(self):
        """Get offset"""
        return self.attrs.offset

    def get_opacity(self):
        """Get opacity"""
        return self.attrs['opacity']

    def get_position(self):
        """Get node position relative to container"""
        return Storage({'x': self.attrs['x'], 'y': self.attrs['y']})

    def get_rotation(self):
        """Get rotation in radians"""
        return self.attrs['rotation']

    def get_rotation_deg(self):
        """Get rotation in degrees"""
        return round(degrees(self.attrs['rotation']), 2)

    def get_scale(self):
        """Get scale"""
        return self.attrs['scale']

    def get_stage(self):
        """Get stage that contains the node"""
        if self.node_type != 'Stage' and self.get_parent():
            return self.get_parent().get_stage()
        elif self.node_type == 'Stage':
            return self
        else:
            return None

    def get_transform(self):
        """Get transform of the node"""
        transform = Transform()

        if self.attrs['x'] != 0 or self.attrs['y'] != 0:
            transform.translate(self.attrs['x'], self.attrs['y'])
        if self.attrs['rotation']:
            transform.rotate(self.attrs['rotation'])
        if self.attrs['scale']['x'] != 1 or self.attrs['scale']['y'] != 1:
            transform.scale(self.attrs['scale']['x'], self.attrs['scale']['y'])
        if self.attrs['offset'] and (self.attrs['offset']['x'] or self.attrs['offset']['y']):
            transform.translate(-1*self.attrs['offset']['x'], -1*self.attrs['offset']['y'])
        return transform

    def get_x(self):
        """Get node x position"""
        return self.attrs['x']

    def get_y(self):
        """Get node y position"""
        return self.attrs['y']

    def get_zindex(self):
        """Get zIndex"""
        return self.index

    @write_output
    def hide(self):
        """Hide node. Hidden nodes are no longer detectable"""
        self.attrs['visible'] = False
        return '%s.hide()' %self.name

    def is_dragging(self):
        """Determine if node is currently in drag and drop mode"""
        return "%s.isDragging()" %self.name

    def is_visible(self):
        """
        Determine if shape is visible or not. Shape is visible only if it's visible and all of its
        ancestors are visible. If an ancestor is invisible, this means that the shape is also invisible
        """
        if self.attrs['visible'] and self.get_parent() and not self.get_parent().is_visible():
            return False
        return self.attrs['visible']

    @write_output
    def move(self, x, y):
        """Move node by an amount"""
        self.attrs['x'] += x
        self.attrs['y'] += y
        return "%s.move( %.2f, %.2f )" %(self.name, x ,y)

    @write_output
    def move_down(self):
        """Move node down"""
        index = self.index
        if index > 0:
            self.parent.children.remove(self)
            self.parent.children.insert(index - 1, self)
            self.parent._set_children_indices()

            if self.node_type == 'Layer':
                stage = self.get_stage()
                if stage:
                    stage.content.remove_child(self.canvas.element)
                    stage.content.insert_before(self.canvas.element, stage.get_children()[self.index+1].canvas.element)

        return '%s.moveDown()' %self.name

    @write_output
    def move_to(self, new_container):
        """Move node to another container"""
        parent = self.parent
        del parent.children[self.index]
        parent.set_children_indices()

        new_container.children.append(self)
        self.index = len(new_container.children) + 1
        self.parent = new_container
        new_container.set_children_indices()

        return '%s.moveTo()' %self.name

    @write_output
    def move_to_bottom(self):
        """Move node to the bottom of its siblings"""
        index = self.index
        del self.parent.children[index]
        self.parent.insert(0, self)
        self.parent.set_children_indices()

        if self.node_type == 'Layer':
            if self.node_type == 'Layer':
                stage = self.get_stage()
                if stage:
                    stage.content.remove_child(self.canvas.element)
                    stage.content.insert_before(self.canvas.element, stage.get_children()[1].canvas.element)
        return '%s.moveToBottom()' %self.name

    @write_output
    def move_to_top(self):
        """Move node to the top of its siblings"""
        index = self.index
        del self.parent.children[index]
        self.parent.append(self)
        self.parent.set_children_indices()

        if self.node_type == 'Layer':
            if self.node_type == 'Layer':
                stage = self.get_stage()
                if stage:
                    stage.content.remove_child(self.canvas.element)
                    stage.content.append_child(self.canvas.element)
        return '%s.moveToTop()' %self.name

    @write_output
    def move_up(self):
        """Move node up"""
        index = self.index
        if index < len(self.parent.get_children()) + 1:
            self.parent.children.remove(self)
            self.parent.children.insert(index + 1, self)
            self.parent._set_children_indices()

            if self.node_type == 'Layer':
                stage = self.get_stage()
                if stage:
                    stage.content.remove_child(self.canvas.element)
                    if self.index < len(stage.get_children()) - 1:
                        stage.content.insert_before(self.canvas.element, stage.get_children()[self.index+1].canvas.element)
                    else:
                        stage.content.append_child(self.canvas.element)


        return '%s.moveUp()' %self.name

    @write_output
    def off(self, type_str):
        """
        Remove event bindings from the node. Pass in a string of event types delimmited by a space
        to remove multiple event bindings at once such as 'mousedown mouseup mousemove'. include a
        namespace to remove an event binding by name such as 'click.foobar'.
        """
        types = type_str.split(' ')
        for n in xrange(len(types)):
            type = types[n]
            event = type
            parts = event.split('.')
            base_event = parts[0]

            if self.event_listeners[base_event] and len(parts) > 1:
                name = parts[1]
                i = 0
                while i < len(self.event_listeners[base_event]):
                    if self.event_listeners[base_event][i]['name'] == name:
                        del self.event_listeners[base_event][i]
                        if not len(self.event_listeners[base_event]):
                            del self.event_listeners[base_event]
                            break
                        i -= 1
                    i += 1
            else:
                del self.event_listeners[base_event]
        return '%s.off(%s)' %(self.name, Type.format(type_str))

    @write_output
    def on(self, type_str, handler):
        """
        Bind events to the node. KineticJS supports mouseover, mousemove, mouseout, mousedown, mouseup,
        click, dblclick, touchstart, touchmove, touchend, tap, dbltap, dragstart, dragmove, and dragend.
        Pass in a string of event types delimmited by a space to bind multiple events at once such as
        'mousedown mouseup mousemove'. include a namespace to bind an event by name such as 'click.foobar'.
        """
        types = type_str.split(' ')
        for n in xrange(len(types)):
            type = types[n]
            event = type
            parts = event.split('.')
            base_event = parts[0]
            name = parts[1] if len(parts) > 1 else ''

            if not(self.event_listeners[base_event]):
                self.event_listeners[base_event] = []

            self.event_listeners[base_event].append(Storage({
                'name': name,
                'handler': handler
            }))
        return '%s.on( "%s", %s )' %(self.name, type_str, handler)

    @write_output
    def rotate(self, theta):
        """Rotate node by an amount in radians"""
        self.attrs.rotation = self.get_rotation() + theta
        return '%s.rotate(%s)' %(self.name, Type.format(theta))

    @write_output
    def rotate_deg(self, deg):
        """Rotate node by an amount in degrees"""
        self.attrs.rotation = self.get_rotation() + radians(deg)
        return '%s.rotate(%s)' %(self.name, Type.format(radians(deg)))

    @write_output
    def set_absolute_position(self, pos):
        """Set absolute position"""
        trans = self._clear_transform()
        self.attrs.x = trans.x
        self.attrs.y = trans.y
        del trans.x
        del trans.y

        it = self.get_absolute_transform()
        it.invert()
        it.translate(pos['x'], pos['y'])
        self._set_transform(trans)

        return '%s.setAbsolutePosition(%s)' %(self.name, Type.format(pos))

    @write_output
    def set_attrs(self, **config):
        """Set attrs"""
        _attrs = self.attrs.copy()
        _attrs.update(config)
        self._parse_node_config(_attrs)
        return '%s.setAttrs( %s )' %(self.name, Type.format(self._eliminate_defaults()))

    @write_output
    def set_drag_bounds(self, bounds):
        """Set drag bounds."""
        if 'top' in bounds:
            self.attrs['drag_bounds']['top'] = round(bounds['top'], 2)
        if 'right' in bounds:
            self.attrs['drag_bounds']['right'] = round(bounds['right'], 2)
        if 'bottom' in bounds:
            self.attrs['drag_bounds']['bottom'] = round(bounds['bottom'], 2)
        if 'left' in bounds:
            self.attrs['drag_bounds']['left'] = round(bounds['left'], 2)

        return '%s.setDragBounds( %s )' %(self.name, Type.format(bounds))

    @write_output
    def set_drag_constraint(self, constraint):
        """Set drag constraint."""
        if constraint not in ['vertical', 'horizontal', 'none']:
            return ''
        self.attrs.drag_constraint = constraint
        return '%s.setDragConstraint( %s )' %(self.name, Type.format(constraint))

    @write_output
    def set_draggable(self, draggable):
        """Set draggable"""
        self.attrs.draggable = bool(draggable)
        return '%s.setDraggable(%s)' %(self.name, Type.format(draggable))

    @write_output
    def set_listening(self, listening):
        """Listen or don't listen to events"""
        self.attrs.listening = bool(listening)
        return '%s.setListening(%s)' %(self.name, Type.format(listening))

    @write_output
    def set_offset(self, x, y):
        """Set offset. A node's offset defines the positition and rotation point"""
        self.attrs.offset.x = round(x, 2)
        self.attrs.offset.y = round(y, 2)
        return "%s.setOffset( %s )" %(self.name, Type.format(self.attrs.offset))

    @write_output
    def set_opacity(self, opacity):
        """
        Set opacity. Opacity values range from 0 to 1. A node with an opacity of 0 is fully transparent,
        and a node with an opacity of 1 is fully opaque
        """
        self.attrs.opacity = round(opacity, 2)
        return '%s.setOpacity( %s )' %(self.name, Type.format(self.attrs.opacity))

    @write_output
    def set_position(self, x , y):
        """Set node position"""
        self.attrs.x = round(x, 2)
        self.attrs.y = round(y, 2)
        return "%s.setPosition( %.2f, %.2f )" %(self.name, self.attrs.x, self.attrs.y)

    @write_output
    def set_rotation(self, theta):
        """Set node rotation in radians"""
        self.attrs.rotation = theta
        return '%s.setRotation(%s)' %(self.name, Type.format(theta))

    @write_output
    def set_rotation_deg(self, deg):
        """Set node rotation in degrees"""
        self.attrs.rotation = radians(deg)
        return '%s.setRotationDeg(%s)' %(self.name, Type.format(self.attrs.rotation))

    @write_output
    def set_scale(self, x, y):
        """Set node scale."""
        self.attrs.scale.x = round(x, 2)
        self.attrs.scale.y = round(y, 2)
        return "%s.setScale(%s)" %(self.name, Type.format(self.attrs.scale))

    @write_output
    def set_x(self, x):
        """Set node x position"""
        self.attrs.x = round(x, 2)
        return "%s.setX( %.2f )" %(self.name, self.attrs.x)

    @write_output
    def set_y(self, y):
        """Set node y position"""
        self.attrs.y = round(y, 2)
        return "%s.setY( %.2f )" %(self.name, self.attrs.y)

    @write_output
    def set_zindex(self, zindex):
        """Set zIndex"""
        self.attrs.zindex = zindex
        return "%s.setZIndex( %d )" %(self.name, self.attrs.zindex)

    @write_output
    def show(self):
        """Show node"""
        self.attrs.visible = True
        return '%s.show()' %self.name

    @write_output
    def simulate(self, event_type):
        """Simulate event"""
        return '%s.simulate( %s )' %(self.name, Type.format(event_type))

    @write_output
    def to_data_url(self, config):
        """
        Creates a composite data URL. If MIME type is notspecified, then "image/png" will result.
        For "image/jpeg", specify a qualitylevel as quality (range 0.0 - 1.0)
        """
        return '%s.toDataURL(%s)' %(self.name, Type.format(config))

    @write_output
    def transition_to(self, config):
        """
        transition node to another state. Any property that can accept a real number can be transitioned,
        including x, y, rotation, opacity, strokeWidth, radius, scale.x, scale.y, offset.x, offset.y, etc.
        """
        self.set_attrs(**config)
        return '%s.transitionTo(%s)' %(self.name, Type.format(config))

    #**********************************************************************
    #*                          Private Methods
    #**********************************************************************
    def _set_attr(self, obj, attr, val):
        if val is not None:
            if obj is None:
                obj = Storage()
            obj[attr] = val

    def _set_transform(self, trans):
        for key in trans:
            self.attrs[key] = trans[key]

    def _clear_transform(self):
        trans = Storage({
            'x': self.attrs.x,
            'y': self.attrs.y,
            'rotation': self.attrs.rotation,
            'scale': Storage({
                'x': self.attrs.scale.x,
                'y': self.attrs.scale.y,
            }),
            'offset': Storage({
                'x': self.attrs.offset.x,
                'y': self.attrs.offset.y,
            })
        })
        self.attrs.x = 0.0
        self.attrs.y = 0.0
        self.attrs.rotation = 0.0
        self.attrs.scale = Storage({'x': 1.0, 'y': 1.0})
        self.attrs.offset = Storage({'x': 0.0, 'y': 0.0})
        return trans

    def _parse_node_config(self, kwargs):
        if 'x' in kwargs:
            self.attrs.x = round(kwargs['x'], 2)
        if 'y' in kwargs:
            self.attrs.y = round(kwargs['y'], 2)
        if 'visible' in kwargs:
            self.attrs.visible = bool(kwargs['visible'])
        if 'listening' in kwargs:
            self.attrs.listening = bool(kwargs['listening'])
        if 'id' in kwargs:
            self.attrs.id = kwargs['id']
        if 'name' in kwargs:
            self.attrs.name = kwargs['name']
        if 'opacity' in kwargs:
            self.attrs.opacity = round(kwargs['opacity'], 2)
        if 'scale' in kwargs:
            if 'x' in kwargs['scale']:
                self.attrs.scale.x = round(kwargs['scale']['x'], 2)
            if 'y' in kwargs['scale']:
                self.attrs.scale.y = round(kwargs['scale']['y'], 2)
        if 'rotation' in kwargs:
            self.attrs.rotation = round(kwargs['rotation'])
        if 'rotation_deg' in kwargs:
            self.attrs.rotation = radians(kwargs['rotation_deg'])
        if 'offset' in kwargs:
            if 'x' in kwargs['offset']:
                self.attrs.scale.x = round(kwargs['offset']['x'], 2)
            if 'y' in kwargs['offset']:
                self.attrs.scale.y = round(kwargs['offset']['y'], 2)
        if 'draggable' in kwargs:
            self.attrs.draggable = bool(kwargs['draggable'])
        if 'drag_constraint' in kwargs and kwargs['drag_constraint'] in ['vertical', 'horizontal', 'none']:
            self.attrs.drag_constraint = kwargs['drag_constraint']
        if 'drag_bounds' in kwargs:
            if 'top' in kwargs['drag_bounds']:
                self.attrs.drag_bounds.top = round(kwargs['drag_bounds']['top'], 2)
            if 'right' in kwargs['drag_bounds']:
                self.attrs.drag_bounds.right = round(kwargs['drag_bounds']['right'], 2)
            if 'bottom' in kwargs['drag_bounds']:
                self.attrs.drag_bounds.bottom = round(kwargs['drag_bounds']['bottom'], 2)
            if 'left' in kwargs['drag_bounds']:
                self.attrs.drag_bounds.left = round(kwargs['drag_bounds']['left'], 2)

    @write_output
    def _make_constructor(self):
        _const = self._eliminate_defaults()
        self._js = 'var %s = new Kinetic.%s(%s);' %(self.name, self.__class__.__name__, Type.format(_const))
        return self._js

    def _eliminate_defaults(self):
        _const = {}
        for key in self.attrs:
            if key in self.default:
                if self.default[key] is None:
                    continue
                if self.default[key] != self.attrs[key]:
                    _const[key] = self.attrs[key]
            else:
                _const[key] = self.attrs[key]
        return _const

    def _draw(self, canvas=None):
        if self.is_visible() and (not canvas or canvas.name == 'buffer' or self.get_listening()):
            if hasattr(self, '__draw'):
                self.__draw(canvas)
            children = self.children
            if children:
                for n in xrange(len(children)):
                    child = children[n]
                    if hasattr(child, 'draw'):
                        child.draw(canvas)
                    else:
                        child._draw(canvas)


if __name__ == '__main__':
    node = Node('node', x=10, y=11, listening=True, drag_bounds={'top': 10}, rotation_deg = 10)
    print str(node)
    from util.global_options import write_to_file
    write_to_file('kin.js')


