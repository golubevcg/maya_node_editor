import math

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

        painter.drawPath(self.path())

        # change path.PointAtPercent() value to move arrow on the line
        triangle_source = self.arrowCalc(
            self.pos_source,
            self.path().pointAtPercent(0.5)
        )

        if triangle_source is not None:
            painter.drawPolyline(triangle_source)

    def update_path(self):
        # will handle drawing qpainter path from point a to point b
        raise NotImplemented("This method has to be overriden in a child class")

    def set_source(self, x, y):
        self.pos_source = [x, y]

    def set_destination(self, x, y):
        self.pos_destination = [x, y]

    def arrowCalc(self, start_point=None, end_point=None):  # calculates the point where the arrow should be drawn

        # TODO: REWORK THIS FUNC
        try:
            if start_point is None:
                start_point = self.pos_source

            if end_point is None:
                end_point = self.pos_destination

            if isinstance(start_point, list):
                start_point = QPointF(start_point[0], start_point[1])

            if isinstance(end_point, list):
                end_point = QPointF(end_point[0], end_point[1])

            dx, dy = start_point.x() - end_point.x(), start_point.y() - end_point.y()

            leng = math.sqrt(dx ** 2 + dy ** 2)
            normX, normY = dx / leng, dy / leng  # normalize

            # perpendicular vector
            perpX = -normY
            perpY = normX

            leftX = end_point.x() + self._arrow_height * normX + self._arrow_width * perpX
            leftY = end_point.y() + self._arrow_height * normY + self._arrow_width * perpY

            rightX = end_point.x() + self._arrow_height * normX - self._arrow_width * perpX
            rightY = end_point.y() + self._arrow_height * normY - self._arrow_width * perpY

            point2 = QPointF(leftX, leftY)
            point3 = QPointF(rightX, rightY)

            return QPolygonF([point2, end_point, point3])
        except (ZeroDivisionError, Exception) as e:
            return None


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
