from PySide2.QtWidgets import QGraphicsView
from PySide2.QtCore import *
from PySide2.QtGui import *


class QDMGraphicsView(QGraphicsView):
    def __init__(self, gr_scene, parent=None):
        super(QDMGraphicsView, self).__init__(parent)

        self.gr_scene = gr_scene

        self.init_ui()

        self.setScene(self.gr_scene)

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
        return super(QDMGraphicsView, self).mousePressEvent(event)

    def left_mouse_button_release(self, event):
        return super(QDMGraphicsView, self).mouseReleaseEvent(event)

    def right_mouse_button_press(self, event):
        return super(QDMGraphicsView, self).mousePressEvent(event)

    def right_mouse_button_release(self, event):
        return super(QDMGraphicsView, self).mouseReleaseEvent(event)

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
        if not clamped or self.zoom_clap is False:
            self.scale(zoom_factor, zoom_factor)
