# from PySide2.QtCore import Qt, QPointF
# from PySide2.QtWidgets import QGraphicsPathItem, QGraphicsItem
# from PySide2.QtGui import *
#
#
# class Path(QGraphicsPathItem):
#     def __init__(self, source = None, destination = None, *args, **kwargs):
#         '''source: QtCore.QPointF = None, destination: QtCore.QPointF = None'''
#         super(Path, self).__init__(*args, **kwargs)
#
#         self._sourcePoint = source
#         self._destinationPoint = destination
#
#         self._arrow_height = 5
#         self._arrow_width = 4
#
#     def setSource(self, point):
#         '''point: QtCore.QPointF'''
#         self._sourcePoint = point
#
#     def setDestination(self, point):
#         '''QtCore.QPointF'''
#         self._destinationPoint = point
#
#     def directPath(self):
#         path = QtGui.QPainterPath(self._sourcePoint)
#         path.lineTo(self._destinationPoint)
#         return path
#
#     def arrowCalc(self, start_point=None, end_point=None):  # calculates the point where the arrow should be drawn
#         try:
#             startPoint, endPoint = start_point, end_point
#
#             if start_point is None:
#                 startPoint = self._sourcePoint
#
#             if endPoint is None:
#                 endPoint = self._destinationPoint
#
#             dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()
#
#             leng = math.sqrt(dx ** 2 + dy ** 2)
#             normX, normY = dx / leng, dy / leng  # normalize
#
#             # perpendicular vector
#             perpX = -normY
#             perpY = normX
#
#             leftX = endPoint.x() + self._arrow_height * normX + self._arrow_width * perpX
#             leftY = endPoint.y() + self._arrow_height * normY + self._arrow_width * perpY
#
#             rightX = endPoint.x() + self._arrow_height * normX - self._arrow_width * perpX
#             rightY = endPoint.y() + self._arrow_height * normY - self._arrow_width * perpY
#
#             point2 = QtCore.QPointF(leftX, leftY)
#             point3 = QtCore.QPointF(rightX, rightY)
#
#             return QtGui.QPolygonF([point2, endPoint, point3])
#
#         except (ZeroDivisionError, Exception):
#             return None
#
#     def paint(self, painter: QtGui.QPainter, option, widget=None) -> None:
#
#         painter.setRenderHint(painter.Antialiasing)
#
#         painter.pen().setWidth(2)
#         painter.setBrush(QtCore.Qt.NoBrush)
#
#         path = self.directPath()
#         painter.drawPath(path)
#         self.setPath(path)
#
#         triangle_source = self.arrowCalc(path.pointAtPercent(0.1), self._sourcePoint)  # change path.PointAtPercent() value to move arrow on the line
#
#         if triangle_source is not None:
#             painter.drawPolyline(triangle_source)