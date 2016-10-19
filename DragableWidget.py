from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

class DragableWidgetProxy(QGraphicsProxyWidget): 
	def __init__(self, scene, parent = None):
		super(DragableWidgetProxy, self).__init__(parent)
		self.scene = scene

		self.setFlags(
			self.flags() | 
			QGraphicsItem.ItemIsMovable | 
			QGraphicsItem.ItemIsSelectable | 
			QGraphicsItem.ItemSendsGeometryChanges |
			QGraphicsItem.ItemIsFocusable
			)

	def mousePressEvent(self, event): self.scene.mousePressEvent(event)
	def mouseMoveEvent(self, event): self.scene.mouseMoveEvent(event)
	def mouseReleaseEvent(self, event): self.scene.mouseReleaseEvent(event)
	def dragEnterEvent (self, event): self.scene.dragEnterEvent(event)
	def dragLeaveEvent (self, event): self.scene.dragLeaveEvent(event)
	def dragMoveEvent (self, event): self.scene.dragMoveEvent(event)


if __name__ == '__main__':
	app = QApplication(sys.argv)

	scene = QGraphicsScene()
	proxy = DragableWidgetProxy(scene)
	proxy.setWidget(QPushButton("Test"))
	scene.addItem(proxy)

	view = QGraphicsView(scene)

	view.show()
	app.exec_()