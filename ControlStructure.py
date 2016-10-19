from PyQt4.QtGui import *
from PyQt4.QtCore import *
from misc import createMenuFromDict
from copy import deepcopy

class ControlStructure(QGraphicsItem):
	def __init__(self, scene, label = ""):
		super(ControlStructure, self).__init__()
		self._rect = None
		self._scene = scene
		self._label = label

		#Menu
		self.menu = deepcopy(self._scene.menu)
		print self.menu
		#self.menu.addAction("Destroy")
		#self.menu.addAction("Collapse")

		self.setFlags(
			self.flags() | 
			QGraphicsItem.ItemIsMovable | 
			QGraphicsItem.ItemIsSelectable | 
			QGraphicsItem.ItemSendsGeometryChanges
			)

	def setLabel(self, label): self._label = label

	def destroy(self): 
		self._scene.removeItem(self)
		self._scene.update()

	def collapse(self): pass


	def addItem(self, item):
		item.setParentItem(self)
		print item

	

	def setPoints(self, start_pt, end_pt):
		self._rect = QRectF()
		self._rect.setTopLeft(start_pt)
		self._rect.setBottomRight(end_pt)

	def contextMenuEvent(self, event):
		self.menu.exec_(event.screenPos())


	def paint(self, painter, option, widget):
		pen = QPen(Qt.black)
		pen.setWidth(2)
		painter.setPen(pen)

		#Body
		painter.drawRoundedRect(self._rect, 10, 10)


		#Title
		text_width = len(self._label) * 8 #6 pixels per letter(ish..)
		text_height = 3
		text_offset = 5 #Distance of text from line
		text_pt = self._rect.bottomRight()

		label_offset = QPointF(text_width + text_offset, text_height + text_offset)
		painter.drawText(text_pt - label_offset, self._label)


		self._scene.update()

	def boundingRect(self): 
		return self._rect



class WhileLoop(ControlStructure):
	def __init__(self, scene):
		super(WhileLoop, self).__init__(scene)
		self.setLabel("While Loop")

		