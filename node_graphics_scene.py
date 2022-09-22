import math

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self):
        super(QDMGraphicsScene, self).__init__()

        self.grid_size = 20

        self._color_background = QColor("#393939")

        self._color_light = QColor("#2f2f2f")
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)

        # scene size
        self.scene_width, self.scene_height = 64000, 64000

        # scene center focus
        self.setSceneRect(
            -self.scene_width//2,
            -self.scene_height//2,
            self.scene_width,
            self.scene_height
        )






        self.setBackgroundBrush(self._color_background)

    def drawBackground(self, painter, rect):
        super(QDMGraphicsScene, self).drawBackground(painter, rect)

        # here we create our grid
        left = int(
            math.floor(rect.left())
        )
        right = int(
            math.floor(rect.right())
        )
        top = int(
            math.floor(rect.top())
        )
        bottom = int(
            math.floor(rect.bottom())
        )

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        lines_light = []
        for x in range(first_left, right, self.grid_size):
            lines_light.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            lines_light.append(QLine(left, y, right, y))

        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)