from PySide2.QtWidgets import QGraphicsView
from PySide2.QtCore import *
from PySide2.QtGui import *

from edge_object import Edge
from graphics_socket import QDMGraphicsSocket

MODE_NOOP = 1
MODE_EDGE_DRAG = 2

EDGE_DRAG_START_THRESHOLD = 10


class QDMGraphicsView(QGraphicsView):
    def __init__(self, gr_scene, parent=None):
        super(QDMGraphicsView, self).__init__(parent)

        self.gr_scene = gr_scene

        self.init_ui()

        self.setScene(self.gr_scene)

        self.mode = MODE_NOOP

        self.zoom_in_factor = 1.25
        self.zoom_clamp = True
        self.zoom = 10
        self.zoom_step = 1
        self.zoom_range = [0, 10]

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

        super(QDMGraphicsView, self).mouseReleaseEvent(event)

    def edge_drag_end(self, item):
        """return True if skip the rest of the code"""
        self.mode = MODE_NOOP
        print("End dragging edge")

        # HERE YOU NEED TO DOUBLE CHECK THAT SOCKET TYPE
        # so always input socket will be to outsocket
        print("self.click_pressed_item.socket_obj.position:", self.click_pressed_item.socket_obj.position)
        # print("item.socket_obj.position:", item.socket_obj.position)
        check_sockets_not_same = self.click_pressed_item.socket_obj.position != item.socket_obj.position
        if isinstance(self.click_pressed_item, QDMGraphicsSocket) and check_sockets_not_same:
            print("    Assign end socket")
            return True

        return False

    def right_mouse_button_press(self, event):
        super(QDMGraphicsView, self).mousePressEvent(event)

        item = self.get_item_at_click(event)

        print("RMB: DEBUG", item)

    def right_mouse_button_release(self, event):
        super(QDMGraphicsView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        # calculate our zoom Factor
        zoom_out_factor = 1 / self.zoom_in_factor

        # store our scene position
        old_pos = self.mapToScene(event.pos())

        # calc zoom
        if event.angleDelta().y()>0:
            zoom_factor = self.zoom_in_factor
            self.zoom += self.zoom_step
        else:
            zoom_factor = zoom_out_factor
            self.zoom -= self.zoom_step

        clamped = False
        if self.zoom < self.zoom_range[0]:
            self.zoom, clamped = self.zoom_range[0], True
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
            edge_type=1
        )

    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.drag_edge.gr_edge.set_destination(pos.x(), pos.y())
            self.drag_edge.gr_edge.update()

        super(QDMGraphicsView, self).mouseMoveEvent(event)
