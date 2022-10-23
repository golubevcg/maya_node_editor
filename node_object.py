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
        self.init_input_sockets()
        self.init_output_sockets()

        #rework with property bin and autosort by alphabet
        self.input_connections = []
        self.output_connections = []

    def init_input_sockets(self):
        self.input_socket = Socket(self, self.socket_height, position="TOP", parent=self)

    def init_output_sockets(self):
        self.output_socket = Socket(self, self.socket_height, position="BOTTOM", parent=self)

    def set_position(self, x, y):
        self.gr_node.setPos(x, y)

    def add_input_connection(self, connection_name):
        self.input_connections.append(connection_name)

    def add_output_connection(self, connection_name):
        self.output_connections.append(connection_name)

    def get_socket_position(self, position):
        if position not in POSSIBLE_POSITIONS:
            raise ValueError("Position must be on of the Possible Position constant values")

        if position == "TOP":
            return 0, -self.socket_height
        else:
            return 0, self.gr_node.height
