from PySide2.QtWidgets import *


class QDMNodeContentWidget(QWidget):
    def __init__(self, parent = None):
        super(QDMNodeContentWidget, self).__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.node_type_label = QLabel("node type")
        self.layout.addWidget(self.node_type_label)