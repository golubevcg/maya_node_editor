import sys

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from PySide2.QtWidgets import QPushButton, QSizePolicy, QApplication
from node_editor_window import NodeEditorWindow


# class NodeEditor(MayaQWidgetDockableMixin, QPushButton):
#     def __init__(self, parent=None):
#         super(NodeEditor, self).__init__(parent=parent)
#         self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
#         self.setText('Push Me')
#
#
# node_editor_widget = NodeEditor()
# node_editor_widget.show(dockable=True)

if __name__ == "__main__":
    wnd = NodeEditorWindow()

    wnd.init_ui()