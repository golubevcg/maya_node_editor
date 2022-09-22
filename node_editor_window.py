from PySide2.QtWidgets import *
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from node_graphics_scene import QDMGraphicsScene


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

        self.gr_scene = QDMGraphicsScene()

        self.view = QGraphicsView(self)
        self.view.setScene(self.gr_scene)
        self.layout.addWidget(self.view)

        # create graphic view

        self.show()


'''
#to work in maya launch this
import sys
sys.path.insert(0, "C:/Users/golub/Documents/maya_node_editor")

import node_editor_window
import imp
imp.reload(node_editor_window)

wnd = node_editor_window.NodeEditorWindow()
wnd.init_ui()
'''