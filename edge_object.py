from graphics_edge import QDMGraphicsEdge


class Edge:
    def __init__(self, scene, start_socket, end_socket):
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.gr_edge = QDMGraphicsEdge(self)