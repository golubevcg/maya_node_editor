import time

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import cmds

from node_editor.edge.edge_object import Edge
from node_editor.node.node_object import Node
from node_editor.scene.scene_object import Scene
from node_editor.view.graphics_view import QDMGraphicsView


default_nodes = [
    u'|persp', u'|top', u'|front', u'|side', u'|left', u'time1', u'sequenceManager1',
    u'hardwareRenderingGlobals', u'renderPartition', u'renderGlobalsList1', u'defaultLightList1',
    u'defaultShaderList1', u'postProcessList1', u'defaultRenderUtilityList1', u'defaultRenderingList1',
    u'lightList1', u'defaultTextureList1', u'lambert1', u'standardSurface1', u'particleCloud1',
    u'initialShadingGroup', u'initialParticleSE', u'initialMaterialInfo', u'shaderGlow1', u'dof1',
    u'defaultRenderGlobals', u'defaultRenderQuality', u'defaultResolution', u'defaultLightSet',
    u'defaultObjectSet', u'defaultViewColorManager', u'defaultColorMgtGlobals', u'hardwareRenderGlobals',
    u'characterPartition', u'defaultHardwareRenderGlobals', u'ikSystem', u'hyperGraphInfo', u'hyperGraphLayout',
    u'globalCacheControl', u'strokeGlobals', u'dynController1', u'lightLinker1', u'persp', u'perspShape',
    u'top', u'topShape', u'front', u'frontShape', u'side', u'sideShape', u'shapeEditorManager',
    u'poseInterpolatorManager', u'layerManager', u'defaultLayer', u'renderLayerManager', u'defaultRenderLayer'
]


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

        self.scene = Scene(self)
        self.view = QDMGraphicsView(self.scene.gr_scene, self)

        self.draw_node_dependencies_for_current_root()

        self.navigation_bar = QHBoxLayout()
        self.init_navigation_bar()
        self.layout.addLayout(self.navigation_bar)

        self.layout.addWidget(self.view)

        # create graphic view
        self.setWindowTitle("Node Editor")
        self.show()

    def draw_node_dependencies_for_current_root(self, root_node=None):

        print("root_node:", root_node)
        print("self.scene:", self.scene)
        print("self.scene.nodes():", self.scene.nodes)
        self.scene.clear_scene()
        print("self.scene.nodes():", self.scene.nodes)

        if root_node:
            top_nodes = cmds.listRelatives(root_node, children=True, fullPath=True)
        else:
            top_nodes = cmds.ls(assemblies=True, long=True)

        print("top_nodes:", top_nodes)
        top_nodes = [node for node in top_nodes if node not in default_nodes]
        if not top_nodes:
            raise RuntimeError("No top nodes has been found")

        init_x = -150
        init_y = -100

        for index, node in enumerate(top_nodes):
            y_pos = init_y + index * 100

            node_type = cmds.nodeType(node)
            node_name = node.split("|", 1)[1]
            print("-----node_name", node_name)

            node_obj = Node(self.scene, node_name, node_type)
            node_obj.path = node
            node_obj.set_position(init_x, y_pos)

        print("self.scene.nodes():", self.scene.nodes)
        print("self.scene.gr_scene.items():", self.scene.gr_scene.items())
        self.scene.gr_scene.update()
        self.view.update()

    def init_navigation_bar(self):
        self.navigation_bar.setContentsMargins(0, 0, 0, 0)
        button1 = QPushButton("test_button1")
        button2 = QPushButton("test_button2")
        self.navigation_bar.addWidget(button1)
        self.navigation_bar.addWidget(button2)

