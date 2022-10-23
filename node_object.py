from content_widget import QDMNodeContentWidget
from graphics_node import QDMGraphicsNode


class Node:
    def __init__(self, scene, title, type):
        self.scene = scene
        self.title = title
        self.type = type

        self.content = QDMNodeContentWidget()
        self.gr_node = QDMGraphicsNode(self)

        self.scene.add_node(self)
        self.scene.gr_scene.addItem(self.gr_node)

        self.inputs = []
        self.outputs = []

    def set_position(self, x, y):
        self.gr_node.setPos(x,y)
