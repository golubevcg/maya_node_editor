from PySide2.QtCore import Qt, QPointF
from PySide2.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PySide2.QtGui import *


class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super(QDMGraphicsEdge, self).__init__(parent)
        self._pen = None
        self.edge = edge

        self._color = QColor("#000000")
        self._color_selected = QColor("#FFFFA637")

        self._pen = QPen(self._color)
        self._pen.setWidth(2.0)

        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidth(2.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.pos_source = [0, 0]
        self.pos_destination = [200, 100]

    def set_source(self, x, y):
        self.pos_source = [x, y]

    def set_destination(self, x, y):
        self.pos_destination = [x, y]

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.update_path()

        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)

        painter.drawPath(self.path())

    def update_path(self):
        # will handle drawing qpainter path from point a to point b
        raise NotImplemented("This method has to be overriden in a child class")

    def set_source(self, x, y):
        self.pos_source = [x, y]

    def set_destination(self, x, y):
        self.pos_destination = [x, y]


class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def update_path(self):
        path = QPainterPath(QPointF(self.pos_source[0], self.pos_source[1]))
        path.lineTo(self.pos_destination[0], self.pos_destination[1])
        self.setPath(path)


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def update_path(self):
        s = self.pos_source
        d = self.pos_destination

        dist = (d[0] - s[0]) * 0.5
        if s[0] > d[0]: dist *= -1

        path = QPainterPath(QPointF(self.pos_source[0], self.pos_source[1]))
        path.cubicTo(
            s[0] + dist,
            s[1],
            d[0] - dist,
            d[1],
            self.pos_destination[0],
            self.pos_destination[1]
        )
        self.setPath(path)
