from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, width, height, x=0, y=0, parent=None):
        super(QDMGraphicsSocket, self).__init__(parent)

        self.width = width
        self.height = height
        self._pen = QPen(Qt.black)
        self._brush = QBrush(Qt.transparent)
        self._x = x
        self._y = y

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        path_outline = QPainterPath()
        path_outline.setFillRule(Qt.WindingFill)
        path_outline.addRoundedRect(
            self._x,
            self._y,
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
            self._x,
            self._y,
            self.width + self._x,
            self.height + self._y
        )
