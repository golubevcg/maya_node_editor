from PySide2.QtWidgets import QGraphicsView, QLineEdit
from PySide2.QtCore import *
from PySide2.QtGui import *

from node_editor.edge.edge_object import Edge
from node_editor.edge.graphics_edge import QDMGraphicsEdge
from node_editor.node.graphics_node import QDMGraphicsNode
from node_editor.socket.graphics_socket import QDMGraphicsSocket

import maya.cmds as cmds

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_THRESHOLD = 10

EDGE_TYPE_GLOBAL = 2


class QDMGraphicsView(QGraphicsView):
    def __init__(self, gr_scene, parent=None):
        super(QDMGraphicsView, self).__init__(parent)

        self.gr_scene = gr_scene

        self.init_ui()

        self.setScene(self.gr_scene)

        self.mode = MODE_NOOP

        self.zoom_in_factor = 1.1
        self.zoom_clamp = True
        self.zoom = 5
        self.zoom_step = 1
        self.zoom_range = [0, 100]

        self.current_root = None

    def init_ui(self):
        self.setRenderHints(
            QPainter.Antialiasing |
            QPainter.HighQualityAntialiasing |
            QPainter.TextAntialiasing |
            QPainter.SmoothPixmapTransform
        )

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middle_mouse_button_press(event)
        elif event.button() == Qt.LeftButton:
            self.left_mouse_button_press(event)
        elif event.button() == Qt.RightButton:
            self.right_mouse_button_press(event)
        else:
            super(QDMGraphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middle_mouse_button_release(event)
        elif event.button() == Qt.LeftButton:
            self.left_mouse_button_release(event)
        elif event.button() == Qt.RightButton:
            self.right_mouse_button_release(event)
        else:
            super(QDMGraphicsView, self).mouseReleaseEvent(event)

    def middle_mouse_button_press(self, event):
        release_event = QMouseEvent(
            QEvent.MouseButtonRelease,
            event.localPos(),
            event.screenPos(),
            Qt.LeftButton,
            Qt.NoButton,
            event.modifiers()
        )
        super(QDMGraphicsView, self).mouseReleaseEvent(release_event)

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fake_event = QMouseEvent(
            event.type(),
            event.localPos(),
            event.screenPos(),
            Qt.LeftButton,
            event.buttons() | Qt.LeftButton,
            event.modifiers()
        )
        super(QDMGraphicsView, self).mousePressEvent(fake_event)

    def middle_mouse_button_release(self, event):
        fake_event = QMouseEvent(
            event.type(),
            event.localPos(),
            event.screenPos(),
            Qt.LeftButton,
            event.buttons() & ~Qt.LeftButton,
            event.modifiers()
        )
        super(QDMGraphicsView, self).mouseReleaseEvent(fake_event)
        self.setDragMode(QGraphicsView.NoDrag)

    def left_mouse_button_press(self, event):
        # get item which we clicked on
        self.click_pressed_item = self.get_item_at_click(event)

        # store position of last LMB button click
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())
        if isinstance(self.click_pressed_item, QDMGraphicsSocket):
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edge_drag_start(self.click_pressed_item)
                return

        if hasattr(self.click_pressed_item, "node") or \
                isinstance(self.click_pressed_item, QDMGraphicsEdge) or \
                self.click_pressed_item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(
                    QEvent.MouseButtonPress,
                    event.localPos(),
                    event.screenPos(),
                    Qt.LeftButton,
                    event.buttons() | Qt.LeftButton,
                    event.modifiers() | Qt.ControlModifier
                )
                super(QDMGraphicsView, self).mousePressEvent(fakeEvent)
                return

        if self.mode == MODE_EDGE_DRAG:
            # IT IS WRONG THIS CHECK IS WRONG
            result = self.edge_drag_end(self.click_pressed_item)
            if result: return

        super(QDMGraphicsView, self).mousePressEvent(event)

    def left_mouse_button_release(self, event):
        # get item which we released
        click_released_item = self.get_item_at_click(event)
        if self.mode == MODE_EDGE_DRAG:

            # checking that we are not trying to connect same sockets together
            if self.click_pressed_item != click_released_item:
                result = self.edge_drag_end(click_released_item)
                if result: return

        if hasattr(self.click_pressed_item, "node") or \
                isinstance(click_released_item, QDMGraphicsEdge) or \
                click_released_item is None:
            if event.modifiers() & Qt.ShiftModifier:
                event.ignore()
                fakeEvent = QMouseEvent(
                    event.type(),
                    event.localPos(),
                    event.screenPos(),
                    Qt.LeftButton,
                    Qt.NoButton,
                    event.modifiers() | Qt.ControlModifier
                )
                super(QDMGraphicsView, self).mouseReleaseEvent(fakeEvent)
                return

        super(QDMGraphicsView, self).mouseReleaseEvent(event)

    def right_mouse_button_press(self, event):
        super(QDMGraphicsView, self).mousePressEvent(event)

    def right_mouse_button_release(self, event):
        super(QDMGraphicsView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        # calculate our zoom Factor
        zoom_out_factor = 1 / self.zoom_in_factor

        # store our scene position
        old_pos = self.mapToScene(event.pos())

        # calc zoom
        if event.angleDelta().y() > 0:
            zoom_factor = self.zoom_in_factor
            self.zoom += self.zoom_step
        else:
            zoom_factor = zoom_out_factor
            self.zoom -= self.zoom_step

        clamped = False
        # if self.zoom < self.zoom_range[0]:
        #     self.zoom, clamped = self.zoom_range[0], True
        if self.zoom > self.zoom_range[1]:
            self.zoom, clamped = self.zoom_range[1], True

        # set scene scale
        if not clamped or self.zoom_clamp is False:
            self.scale(zoom_factor, zoom_factor)

    def get_item_at_click(self, event):
        """returns item over which mouse was clicked"""
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def distance_between_click_and_release_is_off(self, event):
        """measures if we are too far from the las LMB click scene position"""
        new_lmb_pos_release_scene_pos = self.mapToScene(event.pos())
        dist_scene_pos = new_lmb_pos_release_scene_pos - self.last_lmb_click_scene_pos
        vector_length_without_sqrt = (dist_scene_pos.x() * dist_scene_pos.x() + dist_scene_pos.y()*dist_scene_pos.y())
        return vector_length_without_sqrt < EDGE_DRAG_START_THRESHOLD ** 2

    def edge_drag_start(self, item):
        print "Started dragging edges"
        print "    Assign start socket"

        self.drag_edge = Edge(
            self.gr_scene.scene,
            item.socket_obj.node,
            edge_type=EDGE_TYPE_GLOBAL
        )

    def edge_drag_end(self, item):
        """return True if skip the rest of the code"""
        self.mode = MODE_NOOP
        print("End dragging edge")

        # HERE YOU NEED TO DOUBLE CHECK THAT SOCKET TYPE
        # so always input socket will be to outsocket
        print(
            "isinstance(self.click_pressed_item, QDMGraphicsSocket):",
            isinstance(self.click_pressed_item, QDMGraphicsSocket)
        )
        if isinstance(self.click_pressed_item, QDMGraphicsSocket):
            print("item:", item)
            print('isinstance(item, QDMGraphicsSocket)', isinstance(item, QDMGraphicsSocket))

            # y need to replace this item self.click_pressed_item.socket_obj.position
            # w item at the beggining of drag edge

            if item and isinstance(item, QDMGraphicsSocket) \
                    and self.drag_edge.node_start.output_socket.position != item.socket_obj.position:
                print("    Assign end socket")
                self.drag_edge.node_destination = item.socket_obj.node
                self.drag_edge.node_destination.add_input_connection(self.drag_edge)
                self.drag_edge.node_start.add_output_connection(self.drag_edge)
                print("Assign start and end sockets to for edge")
                self.mode = MODE_NOOP
                return True

        print("end dragging edge")
        if self.drag_edge:
            self.drag_edge.remove()
            self.drag_edge = None

        print("self.drag_edge removed")
        return False

    def mouseMoveEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        if self.mode == MODE_EDGE_DRAG and self.drag_edge:
            self.drag_edge.gr_edge.set_destination(scene_pos.x()-1, scene_pos.y()-1)
            self.drag_edge.gr_edge.update()

        super(QDMGraphicsView, self).mouseMoveEvent(event)

    def keyPressEvent(self, event):
        selection = self.gr_scene.selectedItems()
        key = event.key()
        if key == Qt.Key_Tab:
            self.reveal_tab_search()
        elif key == Qt.Key_Delete:
            self.delete_items(selection)

        if key == Qt.Key_O and self.current_root:
            parent_list = cmds.listRelatives(self.current_root, parent=True, fullPath=True)
            if parent_list:
                parent = parent_list[0]
            else:
                parent = None
            self.updat_node_view_with_new_root(dag_node=parent)
            self.current_root = parent

        if len(selection) != 1:
            return

        selected_item = selection[0]
        if not isinstance(selection[0], QDMGraphicsNode):
            return

        node_full_name = selected_item.node.path
        if key == Qt.Key_I:
            self.updat_node_view_with_new_root(dag_node=node_full_name)

    def updat_node_view_with_new_root(self, dag_node=None):
        self.gr_scene.scene.main_window.draw_node_dependencies_for_current_root(dag_node)
        self.current_root = dag_node

    def delete_items(self, selection):
        if not selection:
            return

        for item in selection:
            if isinstance(item, QDMGraphicsEdge):
                item.edge.remove()
            elif isinstance(item, QDMGraphicsNode):
                item.node.remove()

    def reveal_tab_search(self):
        ql_edit = QLineEdit("tralala")
        self.addWidget(ql_edit)
