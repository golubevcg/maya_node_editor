import math

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super(QDMGraphicsScene, self).__init__(parent)

        self.scene = scene

        self.enable_grid = True
        self.additional_grid = True

        self.grid_size = 20
        self.grid_squares = 5

        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)

        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        self.setBackgroundBrush(self._color_background)

    def set_gr_scene(self, width, height):
        # scene center focus
        self.setSceneRect(
            -width//2,
            -height//2,
            width,
            height
        )

    def drawBackground(self, painter, rect):
        super(QDMGraphicsScene, self).drawBackground(painter, rect)

        if not self.enable_grid:
            return

        # here we create our grid
        left = int(math.floor(rect.left()))
        right = int(math.floor(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.floor(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        lines_light, lines_dark = [], []
        squares_step = self.grid_size * self.grid_squares
        for x in range(first_left, right, self.grid_size):
            if x % squares_step == 0 and self.additional_grid:
                lines_dark.append(QLine(x, top, x, bottom))
            else:
                lines_light.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % squares_step == 0 and self.additional_grid:
                lines_dark.append(QLine(left, y, right, y))
            else:
                lines_light.append(QLine(left, y, right, y))

        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)

        if lines_dark:
            painter.setPen(self._pen_dark)
            painter.drawLines(lines_dark)
