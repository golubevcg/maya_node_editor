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

        self.node_start.add_output_connection(self)
        self.node_destination.add_input_connection(self)

        self.update_positions()

    def update_positions(self):

        if self.node_start and self.node_start.output_connections:
            source_pos = self.node_start.output_socket.get_socket_position()
            source_pos[0] += self.node_start.gr_node.pos().x() + self.node_start.gr_node.width / (len(self.node_start.output_connections)+1)
            source_pos[1] += self.node_start.gr_node.pos().y()

            self.gr_edge.set_source(*source_pos)

        if self.node_destination and self.node_destination.input_connections:
            end_pos = self.node_destination.input_socket.get_socket_position()

            end_pos[0] += self.node_destination.gr_node.pos().x() + self.node_destination.gr_node.width / (len(self.node_destination.input_connections)+1)
            end_pos[1] += self.node_destination.gr_node.pos().y()

            self.gr_edge.set_destination(*end_pos)

        self.gr_edge.update()

    def remove_from_sockets(self):
        if self.node_start:
            self.node_start.output_socket.remove_connected_edge(self)

        if self.node_destination:
            self.node_destination.input_socket.remove_connected_edge(self)

        self.node_start = None
        self.node_destination = None

    def remove(self):
        self.remove_from_sockets()
        self.scene.gr_scene.removeItem(self.gr_edge)
        self.gr_edge = None
        self.scene.remove_edge(self)