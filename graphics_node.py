from PySide2.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget
from PySide2.QtCore import *
from PySide2.QtGui import *

from socket_object import QDMGraphicsSocket


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super(QDMGraphicsNode, self).__init__(parent)
        self.node = node
        self.content = self.node.content

        self._node_inner_width_padding = 60
        self._node_inner_height_padding = 35

        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 14)
        qfont_metrics = QFontMetrics(self._title_font)
        self.title_width = qfont_metrics.horizontalAdvance(self.node.title)
        self.title_height = qfont_metrics.height()

        self._node_type_title_color = QColor("#656565")
        self._node_type_title_font = QFont("Ubuntu", 10)
        node_type_qfont_metrics = QFontMetrics(self._title_font)
        self._node_type_width = node_type_qfont_metrics.horizontalAdvance(self.node.type)
        self._node_type_height = node_type_qfont_metrics.height()

        self.biggest_font_width = self.title_width if self.title_width > self._node_type_width else self._node_type_width

        self.width = self.biggest_font_width + self._node_inner_width_padding
        self.height = self.title_height + self._node_type_height

        self.edge_size = 4.0
        self.title_height = 24.0
        self._padding = 4.0

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))
        self._pen_selected.setWidth(2)

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))

        self.init_title()
        self.init_node_type_title()

        self.title = self.node.title
        self.node_type_title = self.node.type

        # init sockets
        self._socket_height = 20
        self.init_sockets_input()
        self.init_sockets_output()


        # init content
        # self.init_content()

        self.init_ui()

    def boundingRect(self):
        return QRectF(
            0,
            0,
            2 * self.edge_size + self.width,
            2 * self.edge_size + self.height,
        ).normalized()

    def init_ui(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def init_sockets_input(self):
        # self.title_item = QGraphicsTextItem(self)
        # self.title_item.setDefaultTextColor(self._title_color)
        # self.title_item.setFont(self._title_font)
        # self.title_x_pos = self.width / 2 - self.title_width / 2
        # self.title_item.setPos(self.title_x_pos, 0)
        self.input_socket = QDMGraphicsSocket(self.width, self._socket_height, x=0, y=-self._socket_height, parent=self)

    def init_sockets_output(self):
        # self.title_item = QGraphicsTextItem(self)
        # self.title_item.setDefaultTextColor(self._title_color)
        # self.title_item.setFont(self._title_font)
        # self.title_x_pos = self.width / 2 - self.title_width / 2
        # self.title_item.setPos(self.title_x_pos, 0)
        self.output_socket = QDMGraphicsSocket(self.width, self._socket_height, x=0, y=self.height, parent=self)

    def init_title(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_x_pos = self.width / 2 - self.title_width / 2
        self.title_item.setPos(self.title_x_pos, 0)

    def init_node_type_title(self):
        self.node_type_title_item = QGraphicsTextItem(self)
        self.node_type_title_item.setDefaultTextColor(self._node_type_title_color)
        self.node_type_title_item.setFont(self._node_type_title_font)
        x_pos = self.width / 2 - self._node_type_width / 2
        self.node_type_title_item.setPos(x_pos, self.title_height+8)

    def init_content(self):
        self.gr_content = QGraphicsProxyWidget(self)
        self.content.setGeometry(
            self.edge_size,
            self.title_height + self.edge_size,
            self.width - 2 * self.edge_size,
            self.height - 2 * self.edge_size - self.title_height,
        )

        self.gr_content.setWidget(self.content)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    @property
    def node_type_title(self):
        return self._title

    @node_type_title.setter
    def node_type_title(self, value):
        self._node_type_title = value
        self.node_type_title_item.setPlainText(self._node_type_title)

    def paint(self, painter, style, widget=None):

        # title
        # path_title = QPainterPath()
        # path_title.setFillRule(Qt.WindingFill)
        # path_title.addRoundedRect(
        #     0,
        #     0,
        #     self.width,
        #     self.title_height,
        #     self.edge_size,
        #     self.edge_size
        # )
        # path_title.addRect(
        #     0,
        #     self.title_height - self.edge_size,
        #     self.edge_size,
        #     self.edge_size,
        # )
        # path_title.addRect(
        #     self.width - self.edge_size,
        #     self.title_height - self.edge_size,
        #     self.edge_size,
        #     self.edge_size,
        # )
        # painter.setPen(Qt.NoPen)
        # painter.setBrush(self._brush_title)
        # painter.drawPath(path_title.simplified())

        # # content (background)
        # path_content = QPainterPath()
        # path_content.setFillRule(Qt.WindingFill)
        # path_content.addRoundedRect(
        #     0,
        #     self.title_height,
        #     self.width,
        #     self.height - self.title_height,
        #     self.edge_size,
        #     self.edge_size
        # )
        # path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        # path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        # painter.setPen(Qt.NoPen)
        # painter.setBrush(self._brush_background)
        # painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.setFillRule(Qt.WindingFill)
        path_outline.addRoundedRect(
            0,
            0,
            self.width,
            self.height,
            self.edge_size,
            self.edge_size
        )

        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(QColor("#404040"))
        # painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

