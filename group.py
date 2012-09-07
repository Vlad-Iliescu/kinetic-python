__author__ = 'Vlad'

from container import Container

class Group(Container):
    def __init__(self, name, **kwargs):
        super(Group, self).__init__(**kwargs)
        self.name = name
        self.node_type = "Group"

        self._parse_container_config(kwargs)
        self._make_constructor()
