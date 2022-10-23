from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsPathItem


class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super(QDMGraphicsEdge, self).__init__(parent)
        self._pen = None
        self.edge = edge

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.update_path()

        painter.setPen(self._pen)
        painter.setBrush(Qt.NoBrush)

        painter.drawPath(self.path())

    def update_path(self):
        # will handle drawing qpainter path from point a to point b
        pass