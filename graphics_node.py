from PySide2.QtWidgets import QGraphicsItem, QGraphicsTextItem
from PySide2.QtCore import *
from PySide2.QtGui import *


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, title="Node Graphics Item", parent=None):
        super(QDMGraphicsNode, self).__init__(parent)
        self.title = title
        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)

        self.init_title()

        self.init_ui()

    def init_ui(self):
        pass

    def init_title(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPlainText(self.title)
