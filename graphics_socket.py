from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket):
        super(QDMGraphicsSocket, self).__init__(socket.node.gr_node)

        self.socket_obj = socket
        self.gr_node = self.socket_obj.node.gr_node

        self.width = self.gr_node.width
        self.height = self.socket_obj.node.socket_height
        self._pen = QPen(Qt.transparent)
        self._pen.setWidth(2)

        # self._brush = QBrush(Qt.transparent)
        self._brush = QBrush("#404040")

        self.setAcceptHoverEvents(True)

        self._hover_pen = QPen(self.gr_node.border_color)
        self._hover_pen.setWidth(1)

        self.hover_mode = False
        self.width_padding = 20

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        path_outline = QPainterPath()
        path_outline.setFillRule(Qt.WindingFill)

        path_outline.addRoundedRect(
            10,
            0,
            self.width - self.width_padding,
            self.height,
            self.gr_node.edge_size,
            self.gr_node.edge_size
        )

        painter.setBrush(self._brush)

        if self.hover_mode:
            painter.setPen(self._hover_pen)
        else:
            painter.setPen(self._pen)

        painter.drawPath(path_outline.simplified())

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        )

    def hoverEnterEvent(self, event):
        self.hover_mode = True
        self.update()
        super(QDMGraphicsSocket, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.hover_mode = False
        self.update()
        super(QDMGraphicsSocket, self).hoverLeaveEvent(event)
