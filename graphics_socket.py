from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, parent_gr_node, height, socket):
        super(QDMGraphicsSocket, self).__init__(parent_gr_node)

        self.socket_obj = socket
        self.gr_node = parent_gr_node

        self.width = self.gr_node.width
        self.height = height
        self._pen = QPen(Qt.black)
        self._brush = QBrush(Qt.transparent)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        path_outline = QPainterPath()
        path_outline.setFillRule(Qt.WindingFill)
        path_outline.addRoundedRect(
            0,
            0,
            self.width,
            self.height,
            0,
            0
        )

        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawPath(path_outline.simplified())

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        )
