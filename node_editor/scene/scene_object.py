from graphics_scene import QDMGraphicsScene
from PySide2.QtGui import *


class Scene:
    def __init__(self, main_window):
        print("------////SCENE_OBJ_INIT////-------")
        self.nodes = []
        self.edges = []

        self.main_window = main_window

        self.scene_width = 64000
        self.scene_height = 64000

        self.init_ui()

    def init_ui(self):
        self.gr_scene = QDMGraphicsScene(self)
        self.gr_scene.setBackgroundBrush(QColor("#303030"))
        self.gr_scene.set_gr_scene(self.scene_width, self.scene_height)

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def clear_scene(self):
        items = self.gr_scene.items()
        self.main_window.view.delete_items(items)
