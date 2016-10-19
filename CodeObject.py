from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from collections import namedtuple
from misc import log, createMenuFromDict

In = True
Out = False

opacicy = 0.8
brush_color = Qt.white #QColor(150,150,150)

node_color = Qt.yellow
node_radius = 5
node_text_offset = 10

title_line_x_offset = 10
title_line_y_offset = 25

title_y_offset = 20

character_length = 7


Node = namedtuple('Node', ['name', 'color', 'is_in','tooltip', 'context_menu'])
	#context_menu: QMenu

NodePos = namedtuple('NodePos', ['node', 'pos'])

class CodeObject(QGraphicsItem):
	def __init__(self, scene, title = "", width = 75, height = 75, widget=None, tooltip="", point = QPointF(0,0)):
		super(CodeObject, self).__init__()
		self.scene = scene
		self.widget = widget
		self.width = float(width)
		self.height = float(height)
		self.title = title
		self.tooltip = tooltip
		self._threaded = True
		self.setPos(point)



		self._border_width = 2
		self._border_color = Qt.black
		self._text_color = Qt.black

		self.showing_title_line = True
		self.compensate_for_title = True

		self.setOpacity(opacicy)


		self._context_menu = {
			"Delete" : lambda e: [self.scene.removeItem(self), self.scene.deleteSelected()],
			"Copy" : lambda e: self.scene.setClipboard([self] + self.scene.selectedItems()),
			"Remove Connections" : lambda e: self.scene.removeItemConnections(self),
			}

		self.setAcceptHoverEvents(True)
		self.setFlags(
			self.flags() | 
			QGraphicsItem.ItemIsMovable | 
			QGraphicsItem.ItemIsSelectable | 
			QGraphicsItem.ItemSendsGeometryChanges |
			QGraphicsItem.ItemIsFocusable
			)

		#[Node(name, color, is_in)]
		self._nodes = []

		#NodePos(Node, QPoint)
		self.node_pos = []

	def setBorderWidth(self, width): self._border_width = width
	def borderWidth(self): return self._border_width

	def setBorderColor(self, color): self._border_color = color
	def borderColor(self): self._border_color

	def setTextColor(self, color): self._text_color = color
	def textColor(self): return self._text_color


	def compensateForTitle(self, comp): self.compensate_for_title = comp
	def showTitleLine(self, show_line): self.showing_title_line = show_line

	def setSize(self, width, height):
		self.width = width
		self.height = height

	def setTitle(self, title): self.title = title

	def setTooltip(self, tip): self.tooltip = tip

	def contextMenu(self): return self._context_menu

	def setContextMenu(self, menu):
		self._context_menu = menu

	def addSubmenu(self, menu): pass

	def contextMenuEvent(self, event):
		node = self._nodeAtPoint(event.pos())
		if node != None and node.context_menu != None: #Show the node contex menu if one exists
			node.context_menu.popup(event.screenPos())

		elif self.contextMenu() != None: 			   #Otherwise show object context menu
			menu = createMenuFromDict(self._context_menu)
			menu.exec_(event.screenPos()) 

	def showWidgetEvent(self, event):
		if self.widget != None:
			self.widget.move(event.screenPos())
			self.widget.show()

	def mouseDoubleClickEvent(self, event):
		node = self._nodeAtPoint(event.pos())
		if node != None: self.setSelected(False)

		self.showWidgetEvent(event)


	def hoverEnterEvent(self, event):
		node = self._nodeAtPoint(QPoint(event.screenPos()))
		
		#Show node tooltip
		if node != None: 
			QToolTip.showText(event.screenPos(), node.tooltip)

		#Show object tooltip
		else: 
			QToolTip.showText(event.screenPos(), self.tooltip)

	def hoverLeaveEvent(self, event):
		QToolTip.hideText()

	def mousePressEvent(self, event):
		node = self._nodeAtPoint(event.pos())
		if node != None and event.button() == Qt.LeftButton: 
			pos = self.mapToScene(self._getNodeCenter(node))
			self.scene.nodeClicked(event, node, pos, self)
			self.setSelected(False)

	
	def _nodeAtPoint(self, point): #Returns the Node node if there is a node at QPoint point. None otherwise
		for node, pos in self.node_pos:
			if (pos.x() - node_radius) <= point.x() <= (pos.x() + node_radius) and (pos.y() - node_radius) <= point.y() <= (pos.y() + node_radius):
				return node

	def _getNodeCenter(self, node):
		for n, pos in self.node_pos:
			if n == node: return pos



	def addNode(self, node): self._nodes.append(node)
	def addNodes(self, node_lst):
		for node in node_lst: self.addNode(node)
	def removeNode(self, node): self._nodes.remove(node)


	def paint(self, painter, option, widget):
		pen = QPen(self._border_color)

		if self.isSelected():
			pen.setWidth(1)
			pen.setStyle(Qt.DashLine)
			painter.setPen(pen)
			painter.drawRoundedRect(QRectF(0,0,self.width, self.height), 10,10)
			self._drawTitle(painter)

		else:
			pen.setWidth(self._border_width)
			painter.setPen(pen)

			painter.setBrush(QBrush(brush_color))
			painter.drawRoundedRect(QRectF(0,0,self.width, self.height), 10,10)

			pen.setWidth(1)
			painter.setPen(pen)
			self._drawTitle(painter)

			pen.setWidth(self._border_width)
			painter.setPen(pen)
			self._drawNodes(painter)


		#self.scene.update() #Force canvas update

	def _drawTitle(self, painter):
		title_length = len(self.title) * 7
		title_x_offset = (self.width - title_length)/2
		title_point = QPoint(title_x_offset,title_y_offset)
		painter.drawText(title_point, self.title)

		if self.showing_title_line:
			line_start = QPoint(title_line_x_offset, title_line_y_offset)
			line_end = QPoint(self.width - title_line_x_offset, title_line_y_offset)
			painter.drawLine(line_start, line_end)

	def _drawNodes(self, painter):
		if self.compensate_for_title: title_offset = title_line_y_offset
		else: title_offset = 0


		spacing = (self.height - title_offset) / (len(self._nodes) + 1)
		in_nodes = [i for i in self._nodes if i.is_in]
		out_nodes = [i for i in self._nodes if not i.is_in] 

		for i, node in enumerate(in_nodes + out_nodes):
			painter.setBrush(QBrush(node.color))
			y = spacing * (i+1) + title_offset
			self._drawNode(painter, node, y)


	def _drawNode(self, painter, node, y):
		if node.is_in:
			node_location = QPoint(0,y)
			text_location = QPoint(node_text_offset, y + node_radius)

		else: 
			text_length = len(node.name) * character_length
			node_location = QPoint(self.width, y)
			text_location = QPoint(self.width - node_radius -node_text_offset - text_length, y + node_radius)

		painter.drawEllipse(node_location, node_radius, node_radius)
		painter.drawText(text_location, node.name)

		self.node_pos = [node_pos for node_pos in self.node_pos if node_pos.node != node]
		self.node_pos.append(NodePos(node, node_location))


	def boundingRect(self): 
		return QRectF(-node_radius,0,self.width + 2*node_radius, self.height)

	def _drawModuleDock(self, painter):
		side_len = 8
		square = QRect(self.width/2, self.height - side_len/2, side_len, side_len)

		painter.setPen(QPen(Qt.DashLine))
		painter.setBrush(QBrush(Qt.black, Qt.Dense5Pattern))
		painter.drawRect(square)
















from PacketBuilder import Packet
if __name__ == '__main__':
	app = QApplication(sys.argv)



	scene = QGraphicsScene()
	item = scene.addItem(CodeObject(scene))


	pb = scene.addWidget(QPushButton("Test"))
	pb.setParentItem(item)

	view = QGraphicsView(scene)
	view.setRenderHints(
		QPainter.Antialiasing | 
		QPainter.SmoothPixmapTransform
		#QPainter.TextAntialiasing
		)

	view.show()

	app.exec_()
