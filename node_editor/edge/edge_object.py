from graphics_edge import *

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2


class Edge:
    def __init__(self,
                 scene,
                 node_start,
                 source_connection_name=None,
                 node_destination=None,
                 destination_connection_name=None,
                 edge_type=2):
        self.scene = scene

        self.node_start = node_start
        self.source_connection_name = source_connection_name

        self.input_connection_index = 1
        self.output_connection_index = 1

        self.node_destination = node_destination
        self.destination_connection_name = destination_connection_name

        self.gr_edge = QDMGraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)

        self.scene.gr_scene.addItem(self.gr_edge)
        self.scene.add_edge(self)

        self.node_start.add_output_connection(self)
        if self.node_destination:
            self.node_destination.add_input_connection(self)

        self.update_positions()

    def update_positions(self):
        if not self.gr_edge:
            return

        source_pos = None

        # this one used to have a little offset in front of node so edge will not intersect with node
        socket_padding = 3
        if self.node_start and self.node_start.output_connections:
            source_pos = self.node_start.output_socket.get_socket_position()
            amount_of_ouput_conns = len(self.node_start.output_connections)

            outputs_step = self.node_start.gr_node.width / (amount_of_ouput_conns+1)
            source_pos[0] += self.node_start.gr_node.pos().x() + outputs_step * self.output_connection_index - outputs_step
            source_pos[1] += self.node_start.gr_node.pos().y() + socket_padding
            self.gr_edge.set_source(*source_pos)

        if self.node_destination and self.node_destination.input_connections:
            end_pos = self.node_destination.input_socket.get_socket_position()

            amount_of_input_conns = len(self.node_destination.input_connections)
            # if amount_of_input_conns == 1:
            #     amount_of_input_conns += 1

            inp_step = self.node_destination.gr_node.width / (amount_of_input_conns+1)
            end_pos[0] += self.node_destination.gr_node.pos().x() + inp_step * self.input_connection_index - inp_step
            end_pos[1] += self.node_destination.gr_node.pos().y() + self.node_start.socket_height - socket_padding

            self.gr_edge.set_destination(*end_pos)
        else:
            if source_pos:
                self.gr_edge.set_destination(*source_pos)

        self.gr_edge.update()

    def remove_from_sockets(self):
        if self.node_start:
            self.node_start.output_socket.remove_connected_edge(self)
            # remove from node this connection
            # update edge positions for node

        if self.node_destination:
            self.node_destination.input_socket.remove_connected_edge(self)

        self.node_start = None
        self.node_destination = None

    def remove(self):
        self.remove_from_sockets()
        self.scene.gr_scene.removeItem(self.gr_edge)
        self.gr_edge = None
        self.scene.remove_edge(self)

    def __str__(self):
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
