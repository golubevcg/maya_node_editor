from graphics_edge import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2


class Edge:
    def __init__(self,
                 scene,
                 node_start,
                 source_connection_name,
                 node_destination,
                 destination_connection_name,
                 type=1):
        self.scene = scene

        self.node_start = node_start
        self.source_connection_name = source_connection_name

        self.node_destination = node_destination
        self.destination_connection_name = destination_connection_name

        self.gr_edge = QDMGraphicsEdgeDirect(self) if type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)
        self.scene.gr_scene.addItem(self.gr_edge)


    def remove_from_sockets(self):
        pass