from PySide2.QtWidgets import (
    QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget,
    QGraphicsPixmapItem
)
from PySide2.QtCore import *
from PySide2.QtGui import *

import maya.cmds as cmds


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super(QDMGraphicsNode, self).__init__(parent)
        self.node = node
        self.content = self.node.content

        self.width = None
        self.title_item = None
        self.node_type_title_item = None

        self.update_ui()

    def update_ui(self):
        self._node_inner_width_padding = 60
        self._node_inner_height_padding = 35

        self._title_color = QColor("#cccccc")
        self._title_font = QFont("Ubuntu", 12)
        qfont_metrics = QFontMetrics(self._title_font)
        self.title_width = qfont_metrics.horizontalAdvance(self.node.title)
        self.title_height = qfont_metrics.height()

        self._node_type_title_color = QColor("#656565")
        self._node_type_title_font = QFont("Ubuntu", 7)
        node_type_qfont_metrics = QFontMetrics(self._node_type_title_font)
        self._node_type_width = node_type_qfont_metrics.horizontalAdvance(self.node.type)
        self._node_type_height = node_type_qfont_metrics.height()

        self.biggest_font_width = self.title_width if self.title_width > self._node_type_width else self._node_type_width

        self.width = 140*1.01
        self.height = 43
        self.edge_size = 9.0
        self.title_height = 20.0
        self._padding = 3.0

        # self.border_color = QColor("#5f777f")
        self.border_color = QColor("transparent")
        self._pen_default = QPen(self.border_color)
        self._pen_selected = QPen(QColor("#FFFFA637"))
        self._pen_selected.setWidth(3)

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#cccccc"))

        self.init_title()
        self.init_node_type_title()

        self.title = self.node.title
        self.node_type_title = self.node.type

        self.init_ui()

        icon_name = cmds.resourceManager(nameFilter="{0}.*".format(self.node.type))
        if icon_name:
            icon_name = [name for name in icon_name if name.count(".") == 1]
            if icon_name:
                icon_name = ":/{0}".format(icon_name[0])

        if not icon_name:
            icon_name = ":/transform.svg"

        icon_pixmap = QPixmap(icon_name)

        self.icon_pixmap_item = QGraphicsPixmapItem(
            icon_pixmap,
            parent=self
        )

        icon_scale_factor = 0.12
        self.icon_pixmap_item.setScale(icon_scale_factor)

        bound_rect = self.icon_pixmap_item.boundingRect()
        self.icon_width = bound_rect.width()*icon_scale_factor
        self.icon_height = bound_rect.height()*icon_scale_factor

        self.icon_x_pos = self.width/2 - self.icon_width/2
        self.icon_y_pos = self.height/2 - self.icon_height/2

        self.icon_pixmap_item.setPos(self.icon_x_pos, self.icon_y_pos)
        self.icon_pixmap_item.setTransformationMode(Qt.SmoothTransformation)

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

    def init_title(self):
        if self.title_item:
            self.title_item.setParent(None)
            del self.title_item

        self.title_item = QDMGraphicsTextItem(self)
        self.title_item.node = self.node
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_x_pos = self.width + 5
        self.title_item.setPos(self.title_x_pos, self.title_height - self.title_height/2-2)
        self.title_item.setTextInteractionFlags(Qt.TextEditorInteraction)

    def init_node_type_title(self):
        if self.node_type_title_item:
            self.node_type_title_item.setParent(None)
            del self.node_type_title_item

        self.node_type_title_item = QGraphicsTextItem(self)
        self.node_type_title_item.node = self.node
        self.node_type_title_item.setDefaultTextColor(self._node_type_title_color)
        self.node_type_title_item.setFont(self._node_type_title_font)
        x_pos = self.width + 5
        self.node_type_title_item.setPos(x_pos, -5)

    def init_content(self):
        self.gr_content = QGraphicsProxyWidget(self)
        self.content.setGeometry(
            self.edge_size,
            self.title_height + self.edge_size,
            self.width - 2 * self.edge_size,
            self.height - 2 * self.edge_size - self.title_height,
        )

        self.gr_content.setWidget(self.content)

    def mouseMoveEvent(self, event):
        super(QDMGraphicsNode, self).mouseMoveEvent(event)

        # optimise me, just update the selected nodes
        for node in self.scene().scene.nodes:
            if node.gr_node.isSelected():
                node.update_edge_positions()

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
        painter.setBrush(QColor("#cccccc"))

        painter.drawPath(path_outline.simplified())

        icon_line_padding = 15
        icon_line_delta = 6
        icon_line_y_padding = 5

        line1_p0_x = self.icon_x_pos + self.icon_width + icon_line_padding - icon_line_delta-3
        line1_p0_y = self.height - icon_line_y_padding

        line1_p1_x = self.icon_x_pos + self.icon_width + icon_line_padding-3
        line1_p1_y = icon_line_y_padding

        lines_color = QColor("#707070")
        lines_pen = QPen(lines_color)
        lines_pen.setWidth(1)
        painter.setPen(lines_pen)
        painter.setBrush(Qt.NoBrush)

        line_path = QPainterPath(QPointF(line1_p0_x, line1_p0_y))
        line_path.lineTo(line1_p1_x, line1_p1_y)
        painter.drawPath(line_path)

        line2_p0_x = self.icon_x_pos - self.icon_width + icon_line_padding - icon_line_delta+3
        line2_p0_y = self.height - icon_line_y_padding

        line2_p1_x = self.icon_x_pos - self.icon_width + icon_line_padding+3
        line2_p1_y = icon_line_y_padding

        painter.setPen(lines_pen)
        painter.setBrush(Qt.NoBrush)

        line_path = QPainterPath(QPointF(line2_p0_x, line2_p0_y))
        line_path.lineTo(line2_p1_x, line2_p1_y)
        painter.drawPath(line_path)




    def update_node_width(self):
        len_inp_conn = len(self.node.input_connections)
        len_out_conn = len(self.node.output_connections)

        max_len_conn = max(len_inp_conn, len_out_conn)
        if not max_len_conn:
            return

        step_size = self.width / max_len_conn
        min_step_size = 50
        if step_size < min_step_size:
            self.width = (max_len_conn+2) * min_step_size
            self.update_ui()
            self.node.input_socket.updateWidth(self.width)

            self.node.output_socket.updateWidth(self.width)


class QDMGraphicsTextItem(QGraphicsTextItem):
    def __init__(self, node):
        self.node = node
        super(QDMGraphicsTextItem, self).__init__(node)

    def focusOutEvent(self, event):
        super(QDMGraphicsTextItem, self).focusOutEvent(event)
        text = self.document().toPlainText()
        if self.node.title != text:
            self.node.title = text
