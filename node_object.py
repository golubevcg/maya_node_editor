from content_widget import QDMNodeContentWidget
from graphics_node import QDMGraphicsNode
from socket_object import POSSIBLE_POSITIONS, Socket


class Node:
    def __init__(self, scene, title, type):
        self.scene = scene
        self.title = title
        self.type = type

        self.content = QDMNodeContentWidget()
        self.gr_node = QDMGraphicsNode(self)

        self.scene.add_node(self)
        self.scene.gr_scene.addItem(self.gr_node)

        # init sockets
        self.socket_height = 20

        self.init_input_socket()
        self.init_output_socket()

        # rework with property bin and autosort by alphabet
        # each connection update (doesn't matter if it input or output)
        # we need to recalculate position of the sockets
        self.input_connections = []
        self.output_connections = []

    def init_input_socket(self):
        self.input_socket = Socket(self, self.socket_height, position="TOP", parent=self)

    def init_output_socket(self):
        self.output_socket = Socket(self, self.socket_height, position="BOTTOM", parent=self)

    def set_position(self, x, y):
        self.gr_node.setPos(x, y)

    def add_input_connection(self, edge_object):
        if edge_object not in self.input_connections:
            self.input_connections.append(edge_object)
            self.gr_node.update_node_width()
            self.update_edge_positions()

    def add_output_connection(self, edge_object):
        if edge_object not in self.output_connections:
            self.output_connections.append(edge_object)
            self.gr_node.update_node_width()
            self.update_edge_positions()

    def update_edge_indexes(self):
        if self.input_connections:
            for index, edge_obj in enumerate(self.input_connections):
                index += 2
                edge_obj.input_connection_index = index

        if self.output_connections:
            for index, edge_obj in enumerate(self.output_connections):
                index += 2
                edge_obj.output_connection_index = index

    # TODO: WRITE REMOVE CONNECTION
    def remove_connection(self, edge_object):
        if edge_object in self.input_connections:
            self.input_connections.remove(edge_object)
        elif edge_object in self.output_connections:
            self.output_connections.remove(edge_object)

        self.gr_node.update_node_width()
        self.update_edge_positions()

    def get_socket_position(self, position):
        if position not in POSSIBLE_POSITIONS:
            raise ValueError("Position must be on of the Possible Position constant values")

        if position == "TOP":
            return [0, -self.socket_height-1]
        else:
            return [0, self.gr_node.height+1]

    def update_edge_positions(self):
        self.update_edge_indexes()
        all_connections = self.get_all_connections()

        if all_connections:
            for edge in all_connections:
                edge.update_positions()

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def get_all_connections(self):
        all_connections = self.input_connections[:]
        if self.output_connections:
            all_connections.extend(self.output_connections)

        return all_connections
