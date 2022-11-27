from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from edge_object import Edge
from node_object import Node
from scene_object import Scene
from graphics_view import QDMGraphicsView


class NodeEditorWindow(QWidget, MayaQWidgetDockableMixin):
    def __init__(self, *args, **kwargs):
        super(NodeEditorWindow, self).__init__(*args, **kwargs)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Scene node editor")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.scene = Scene()

        self.add_nodes()

        self.navigation_bar = QHBoxLayout()
        self.init_navigation_bar()
        self.layout.addLayout(self.navigation_bar)

        self.view = QDMGraphicsView(self.scene.gr_scene, self)
        self.layout.addWidget(self.view)

        # create graphic view
        self.setWindowTitle("Node Editor")
        self.show()

        # self.addDebugContent()

    def add_nodes(self):
        node = Node(self.scene, "my_super_node", "node type")
        node.set_position(-75, -250)

        node1 = Node(self.scene, "boxShape1", "mesh")
        node1.set_position(-250, -30)

        node2 = Node(self.scene, "joint1", "joint")
        node2.set_position(-75, 175)

        edge1 = Edge(self.scene, node, "input_1", node1, "output_1")

    def init_navigation_bar(self):
        self.navigation_bar.setContentsMargins(0, 0, 0, 0)
        button1 = QPushButton("test_button1")
        button2 = QPushButton("test_button2")
        self.navigation_bar.addWidget(button1)
        self.navigation_bar.addWidget(button2)

    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)

        rect = self.gr_scene.addRect(-100,-100,80,100,outlinePen,greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.gr_scene.addText("Ttrelelelelel", QFont("TimesNewRoman"))
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        widget1 = QPushButton("Hello World")
        proxy1 = self.gr_scene.addWidget(widget1)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setPos(0,30)

        widget2 = QTextEdit()
        proxy2 = self.gr_scene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos(0, 60)

        line = self.gr_scene.addLine(-200, -200, 400, -100, outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)
