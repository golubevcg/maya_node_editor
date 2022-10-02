from graphics_node import QDMGraphicsNode


class Node:
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene
        self.title = title

        self.gr_node = QDMGraphicsNode(self, self.title)

        self.scene.add_node(self)
        self.scene.gr_scene.addItem(self.gr_node)

        self.inputs = []
        self.outputs = []
