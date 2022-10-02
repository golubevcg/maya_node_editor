from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

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
        self.setLayout(self.layout)

        self.scene = Scene()

        node = Node(self.scene, "My Awesome Node")

        self.view = QDMGraphicsView(self.scene.gr_scene, self)
        self.layout.addWidget(self.view)

        # create graphic view

        self.show()

        # self.addDebugContent()

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

'''
#to work in maya launch this
import sys
import inspect

for module in list(sys.modules):
    module_path = None
    try:
        module_path = inspect.getfile(sys.modules[module])
        if "maya_node_editor" in module_path:
            sys.modules.pop(module_path)
    except:
        continue

import sys
sys.path.insert(0, "C:/Users/golub/Documents/maya_node_editor")
from editor_window import NodeEditorWindow

wnd = NodeEditorWindow()

wnd.init_ui()

'''