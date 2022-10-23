from PySide2.QtCore import Qt
from PySide2.QtGui import QPen, QBrush

from graphics_socket import QDMGraphicsSocket

POSSIBLE_POSITIONS = {
    "TOP",
    "BOTTOM"
}


class Socket:
    def __init__(self, node, height, parent=None, position="TOP"):

        self.node = node
        if position not in POSSIBLE_POSITIONS:
            raise ValueError("Position must be on of the Possible Position constant values")

        self.position = position

        self.width = self.node.gr_node.width
        self.height = height

        self.gr_socket = QDMGraphicsSocket(self.node.gr_node, self.height)
        self.gr_socket.setPos(*self.node.get_socket_position(self.position))

        self.edge = None
