import math

from PySide2.QtCore import Qt, QPointF, QLineF
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

        self.y_padding = 4

        # add param to this attribute
        # if this attribute changed - recalculate node graph
        # on i/o hotkeys update this parent node and redraw node graph
        self.current_parent_dag_node = None

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

        socket_radius = 3
        painter.setPen(self._pen)
        painter.setBrush(self._color)

        painter.drawEllipse(QPointF(self.pos_source[0], self.pos_source[1]+(self.y_padding-2)), socket_radius, socket_radius)
        painter.drawEllipse(QPointF(self.pos_destination[0], self.pos_destination[1]-(self.y_padding-2)), socket_radius, socket_radius)

        triangle_source = self.arrowCalc(
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
        self.pos_source = [x, y + self.y_padding]

    def set_destination(self, x, y):
        self.pos_destination = [x, y - self.y_padding]

    def arrowCalc(self, line):
        # calculates the point where the arrow should be drawn
        arrow_size = 10
        arrow_padding = 0.45

        end_point = line.pointAtPercent(0.0 + arrow_padding)

        start_point = line.pointAtPercent(1.0 - arrow_padding)

        dx, dy = end_point.x() - start_point.x(), end_point.y() - start_point.y()

        angle = math.atan2(-dy, dx)

        PI_CONSTANT = math.pi

        arrowP1 = QPointF(
            start_point + QPointF(math.sin(angle + PI_CONSTANT / 3) * arrow_size,
            math.cos(angle + PI_CONSTANT / 3) * arrow_size)
        )

        arrowP2 = QPointF(
            start_point + QPointF(
                math.sin(angle + PI_CONSTANT - PI_CONSTANT / 3) * arrow_size,
                math.cos(angle + PI_CONSTANT - PI_CONSTANT / 3) * arrow_size)
        )

        return QPolygonF([start_point, arrowP1, arrowP2])


class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def update_path(self):
        path = QPainterPath(QPointF(self.pos_source[0], self.pos_source[1]))
        path.lineTo(self.pos_destination[0], self.pos_destination[1])
        self.setPath(path)


class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def update_path(self):

        p0 = QPointF(*self.pos_source)
        p1 = QPointF(*self.pos_destination)

        # bezier_padding = 80*1.5
        bezier_padding = 50

        path = QPainterPath()
        path.moveTo(p0)
        path.cubicTo(
            QPointF(p0.x(), p0.y() + bezier_padding),
            QPointF(p1.x(), p1.y() - bezier_padding),
            p1
        )

        self.setPath(path)
