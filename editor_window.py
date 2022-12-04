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

        self.root_node = None
        self.navigation_buttons = []
        self.navigation_bar = QHBoxLayout()
        self.navigation_bar.setContentsMargins(0, 0, 0, 0)

        self.draw_node_dependencies_for_current_root()

        self.layout.addLayout(self.navigation_bar)
        self.layout.addWidget(self.view)

        # create graphic view
        self.setWindowTitle("Node Editor")
        self.show()

    def draw_node_dependencies_for_current_root(self, root_node=None):
        print()
        print("draw_node_dependencies_for_current_root")
        print("root_node:", root_node)
        if root_node:
            top_nodes = cmds.listRelatives(root_node, children=True, fullPath=True)
            self.root_node = root_node
        else:
            top_nodes = cmds.ls(assemblies=True, long=True)

        if top_nodes:
            top_nodes = [node for node in top_nodes if node not in default_nodes]

        if not top_nodes:
            return

        self.scene.clear_scene()

        init_x = -350
        init_y = -100
        x_offset = 0
        max_x = 0

        for index, node in enumerate(top_nodes):
            index += 1
            x_pos = (init_x + index * 300) + x_offset
            y_pos = init_y + index * 100

            node_type = cmds.nodeType(node)
            node_name = node.rsplit("|", 1)[1]

            node_obj = Node(self.scene, node_name, node_type)
            node_obj.path = node

            output_connections = cmds.listConnections(node, source=True, destination=False)
            input_connections = cmds.listConnections(node, source=False, destination=True)

            all_connections = []
            if output_connections:
                all_connections.extend(output_connections)
            if input_connections:
                all_connections.extend(input_connections)

            self.connection_x_step = 180
            node_obj.set_position(
                x_pos + (self.connection_x_step * len(all_connections))/2,
                y_pos
            )

            created_nodes = []

            if output_connections:
                output_nodes = self.add_connected_nodes(output_connections, node_obj)
                created_nodes.extend(output_nodes)

            if input_connections:
                input_nodes = self.add_connected_nodes(input_connections, node_obj, output=True)
                created_nodes.extend(input_nodes)

            nodes_x_pos = [node.gr_node.pos().x() for node in created_nodes]

            if nodes_x_pos:
                max_x = max(nodes_x_pos)

            x_offset += max_x

        self.update_navigation_bar()

        self.scene.gr_scene.update()
        self.view.update()

    def add_connected_nodes(self, nodes_list, node_obj, output=False):
        pos = node_obj.gr_node.pos()

        x_pos = pos.x()
        y_pos = pos.y() + 100

        x_offset = 0

        if len(nodes_list) > 1:
            x_offset = len(nodes_list)/2 * self.connection_x_step

        created_nodes = []

        for index, node_name in enumerate(nodes_list):
            if node_name in default_nodes:
                continue

            node_type = cmds.nodeType(node_name)

            upd_y_pos = y_pos + (index+1) * 130
            if not output:
                upd_y_pos *= -1

            upd_x_pos = x_pos + index * self.connection_x_step - x_offset

            created_node_obj = Node(self.scene, node_name, node_type)
            created_node_obj.path = node_name
            created_node_obj.set_position(upd_x_pos, upd_y_pos)
            created_nodes.append(created_node_obj)

            if output:
                Edge(
                    self.scene,
                    node_obj,
                    "input_1",
                    created_node_obj,
                    "output_1"
                )
            else:
                Edge(
                    self.scene,
                    created_node_obj,
                    "input_1",
                    node_obj,
                    "output_1"
                )

        return created_nodes

    def update_navigation_bar(self):
        if self.navigation_buttons:
            for button in self.navigation_buttons:
                self.navigation_bar.removeWidget(button)
                del button

        self.navigation_buttons = []
        parents = []
        if self.root_node:
            if self.root_node.count("|") > 1:
                parents = self.root_node.split("|")
                parents = [node for node in parents if node]
            elif "|" in self.root_node:
                parents = [self.root_node]

        parents = ["root"] + list(parents)
        for node in parents:
            full_node_path = None
            if self.root_node and node != "root":
                full_node_path = self.root_node.split(node)[0]
                full_node_path = full_node_path + node
            print("full_node_path", full_node_path)
            button1 = QPushButton(node)
            button1.clicked.connect(
                lambda: self.draw_node_dependencies_for_current_root(root_node=full_node_path)
            )
            self.navigation_buttons.append(button1)
            self.navigation_bar.addWidget(button1)

