__author__ = 'Vlad'

from node import Node
from util.type import Type
from util.global_options import Kinetic, write_output

class Container(Node):
    def __init__(self, var_name=None, **kwargs):
        super(Container, self).__init__(**kwargs)

        self._parse_container_config(kwargs)
        self.name = var_name
        self.children = []

        if self.name:
            self._make_constructor()

    @write_output
    def add(self, child):
        """Add node to container"""
#        child = Node()
#        child._id = Kinetic.Global.id_counter
#        Kinetic.Global.id_counter += 1
        child.index = len(self.children)
        child.parent = self
        self.children.append(child)
        stage = child.get_stage()

        if not stage:
            Kinetic.Global._add_temp_node(child)
        else:
            stage._add_id(child)
            stage._add_name(child)

            go = Kinetic.Global
            go._pull_nodes(stage)

        if hasattr(self, '_add'):
            self._add(child)

        return '%s.add(%s);' %(self.name, child.name)

    def get(self, selector):
        """
        Return an array of nodes that match the selector.
        Use '#' for id selectionsand '.' for name selections ex:
            var node = stage.get('#foo'); // selects node with id foo
            var nodes = layer.get('.bar'); // selects nodes with name bar inside layer
        """
        stage = self.get_stage()
        arr = []
        key = selector[1:]
        if selector[0] == '#':
            arr = [stage.ids[key]] if stage.ids[key] else []
        elif selector[0] == '.':
            arr = [stage.name[key]] if stage.name[key] else []
        elif selector == 'Shape' or selector == 'Group' or selector == 'Layer':
            return self._get_nodes(selector)
        else:
            return []

        retr_arr = []
        for n in xrange(len(arr)):
            node = arr[n]
            if self.is_ancestor_of(node):
                retr_arr.append(node)

        return retr_arr

    def get_children(self):
        """Get children"""
        return self.children

    def get_intersections(self, x, y):
        """Get shapes that intersect a point"""
        arr = []
        shapes = self.get('Shapes')

        for n in xrange(len(shapes)):
            shape = shapes[n]
            if shape.is_visible() and shape.intersects(x, y):
                arr.append(shape)

        return arr

    def is_ancestor_of(self, node):
        """Determine if node is an ancestor of descendant"""
        if self.node_type == 'Stage':
            return True

        parent = node.get_parent()
        while parent:
            if id(parent) == id(self):
                return True
            parent = parent.get_parent()

        return False

    @write_output
    def remove(self, child):
        """Remove child from container"""
        if child and child.index is not None and id(self.children[child.index]) == id(child):
            stage = self.get_stage()
            if stage:
                stage._remove_id(child.get_id())
                stage._remove_name(child.get_name())

            Kinetic.Global._remove_temp_node(child)
            del self.children[child.index]
            self._set_children_indices()

            while child.children and len(child.children) > 0:
                child.remove(child.children)

            if hasattr(child, '_remove'):
                child._remove()
        return '%s.remove(%s);' %(self.name, child.name)

    @write_output
    def remove_children(self):
        """Remove all children"""
        while len(self.children) > 0:
            self.remove(self.children[0])

        return '%s.removeChildren();' %self.name

    def _parse_container_config(self, kwargs):
        if 'alpha' in kwargs:
            self.attrs.alpha = round(kwargs['alpha'], 2)

    def _get_nodes(self, selector):
        """Get all shapes inside container"""
        arr = []
        def traverse(cont):
            children = cont.get_children()
            for n in xrange(len(children)):
                child = children[n]
                if child.node_type == selector:
                    arr.append(child)
                elif child.node_type != 'Shape':
                    traverse(child)
        traverse(self)
        return arr

    def _set_children_indices(self):
        for n in xrange(len(self.children)):
            self.children[n].index = n


if __name__ == '__main__':
    c = Container('container',**{'alpha': 1})
    from util.global_options import write_to_file
    from node import Node
    n1 = Node('node1', x=10)
    n2 = Node('node2')
    c.add(n1)
    c.add(n2)
    n2.move_down()

    write_to_file('kin.js')
