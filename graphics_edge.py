import math

from PySide2.QtCore import Qt, QPointF
from PySide2.QtWidgets import QGraphicsPathItem, QGraphicsItem
from PySide2.QtGui import *


class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super(QDMGraphicsEdge, self).__init__(parent)
        self._pen = None
        self.edge = edge

        self._color = QColor("#5f777f")
        self._color_selected = QColor("#FFFFA637")

        self._pen = QPen(self._color)
        self._pen.setWidth(2)

        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidth(2.0)

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.pos_source = [0, 0]
        self.pos_destination = [200, 100]

        self._arrow_height = 5
        self._arrow_width = 4

    def set_source(self, x, y):
        self.pos_source = [x, y]

    def set_destination(self, x, y):
        self.pos_destination = [x, y]

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.update_path()

        painter.setRenderHint(painter.Antialiasing)

        painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)

        path = painter.drawPath(self.path())


        arrow_position = self.path().pointAtPercent(1)
        arrow_position = [arrow_position.x(), arrow_position.y()]

        # change path.PointAtPercent() value to move arrow on the line
        triangle_source = self.arrowCalc(
            self.pos_source,
            arrow_position,
            self.path()
        )

        if triangle_source is not None:
            painter.setPen(self._pen)
            painter.setBrush(self._color)

            painter.drawPolygon(triangle_source)

    def update_path(self):
        # will handle drawing qpainter path from point a to point b
        raise NotImplemented("This method has to be overriden in a child class")

    def set_source(self, x, y):
        self.pos_source = [x, y]

    def set_destination(self, x, y):
        self.pos_destination = [x, y]

    def arrowCalc(self, end_point=None, start_point=None, line=None):
        # calculates the point where the arrow should be drawn
        arrow_size = 12

        p1 = line.elementAt(0)
        p2 = line.elementAt(1)

        dx, dy = end_point[0] - start_point[0], end_point[1] - start_point[1]

        angle = math.atan2(-dy, dx)

        PI_CONSTANT = math.pi

        qpointf_start_point = QPointF(*start_point)

        arrowP1 = QPointF(
            qpointf_start_point + QPointF(math.sin(angle + PI_CONSTANT / 3) * arrow_size,
            math.cos(angle + PI_CONSTANT / 3) * arrow_size)
        )

        arrowP2 = QPointF(
            qpointf_start_point + QPointF(
                math.sin(angle + PI_CONSTANT - PI_CONSTANT / 3) * arrow_size,
                math.cos(angle + PI_CONSTANT - PI_CONSTANT / 3) * arrow_size)
        )

        # arrow_head = QPolygonF(line.p1() << arrowP1 << arrowP2)
        return QPolygonF([qpointf_start_point, arrowP1, arrowP2])


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
