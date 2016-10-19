from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
from math_objects import Add, Sub
from PacketBuilder import Packet
from copy import deepcopy
from BezierLine import BezierLine
from collections import namedtuple
from misc import createMenuFromDict, checkTypes
from SceneBackend import SceneBackend
from UtilityBlocks import *
from ControlStructure import *

from CodeObject import *


"""
GraphicsScene::collidingItems()
QGraphicsItem::collidesWithItem()
QGraphicsItem::collidesWithPath()
"""



Line = namedtuple("Line", ["line_obj", "start_node", "start_obj", "end_node", "end_obj"])
class CodeScene(QGraphicsScene):
	def __init__(self, backend = None):
		super(CodeScene, self).__init__()

		self._backend = backend
		
		#Draw control block
		self._mouse_press_pos = None
		self._mouse_release_pos = None
		self._control_struct = None

		#Control Structures
		self._control_structs = [
			("While Loop", WhileLoop),
			("Generic Structure", ControlStructure)]

		#Code Blocks
		self._code_blocks = [
			("Packet", Packet),
			("Sleep", Sleep),
			("Counter", Counter)]

		#Context menu
		self.menu = None
		self._createMenu()
		
		self.line = None
		self.connections = []

		self.obj_clipboard = []

		self.backend = None

	#(name, struct_class)
	def registerControlStruct(self, name, struct_class):
		self._control_structs.append((name, struct_class))

	#(name, obj_class)
	def registerCodeBlock(self, name, obj_class): 
		self._code_blocks.append((name, obj_class))


	def _createMenu(self):
		menu = QMenu("Scene")
		menu.setTearOffEnabled(True)

		#Run/Stop #######################
		menu.addAction("Run")
		#################################

		menu.addSeparator()

		paste = menu.addAction("Paste", self.paste)
		#paste.setShortcut('Ctrl+P')

		menu.addAction("Delete All", self.deleteAll)
		menu.addAction("Select All", self.selectAll)

		menu.addSeparator()

		#Control Structures Menu
		create_ctrl_struct = menu.addMenu("Create Control Structure")
		for (name, struct_class) in self._control_structs:
			create_ctrl_struct.addAction(name, lambda: self.setControlStructure(struct_class(self)))

		#Code Block Menu
		create_code_block = menu.addMenu("Create Code Block")
		actions = []
		for i, (name, obj_class) in enumerate(self._code_blocks): 
			actions.append(QAction(name, create_code_block))
			actions[i].triggered.connect(lambda: self.addItem(obj_class(self)))
			create_code_block.addAction(actions[i])

		print actions



		menu.addSeparator()

		debug = QAction("Debug", menu)
		debug.setCheckable(True)
		menu.addAction(debug)


		#Max CPU Cores ###################################
		core_limit = menu.addMenu("Max CPU Cores")
		action_group = QActionGroup(core_limit)
		cpu_cores = 3
		cores = []
		for i in range(0, cpu_cores):
			cores.append(QAction(str(i + 1), action_group)) #Set cores[i]
			cores[i].setCheckable(True)
			action_group.addAction(cores[i])
			core_limit.addAction(cores[i])

		cores[0].setChecked(True)

		action_group.setExclusive(True)
		####################################################

		self.menu = menu


	def setControlStructure(self, struct): 
		self._control_struct = struct
	def controlStructure(self): return self._control_struct
	
	def startDrawingControlStructure(self): 
		QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))

	def stopDrawingControlStructure(self): 
		self.setControlStructure(None)
		QApplication.restoreOverrideCursor()
		for item in self.selectedItems(): item.setSelected(False)

	def sceneChangeEvent(self):
		self.views()[0].capture()


	def addCodeObject(self, code_object, point = QPointF(0,0)):
		code_object.setPos(point)
		self.addItem(code_object)


	def removeItemConnections(self, item):
		for line in self.connections:
			if item == line.start_obj or line == line.end_obj: 
				self.removeItem(line.line_obj)

	#Destroy all connections to item
	def removeItem(self, item): 
		self.sceneChangeEvent()
		#Remove all connections to item
		if isinstance(item, CodeObject): self.removeItemConnections(item)

		super(CodeScene, self).removeItem(item)

	def addItem(self, item):
		self.sceneChangeEvent()
		super(CodeScene, self).addItem(item)
		
		
	def addToClipboard(self, obj): self.obj_clipboard.append(obj)
	def removeFromClipboard(self, obj): self.obj_clipboard.remove(obj)
	def clearClipboard(self, obj): self.obj_clipboard = []
	def setClipboard(self, objs): self.obj_clipboard = objs

	def keyPressEvent(self, event): 
		if event.key() == Qt.Key_Escape:

			#Esc: Stop Drawing line
			if self.line != None:
				self.removeItem(self.line.line_obj)
				self.line = None

			self.stopDrawingControlStructure()
			
			self.clearSelection()
			self.update()


		#Delete/Backspace: Delete selected items
		if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace: 
			self.deleteSelected()

		#Ctrl..
		if QApplication.keyboardModifiers() == Qt.ControlModifier:

			#Ctrl+X: Cut
			if event.key() == Qt.Key_X:
				self.copySelected()
				self.deleteSelected()

			#Ctrl+A: Select All
			if event.key() == Qt.Key_A:
				self.selectAll()
			#Ctrl+C: Copy
			if event.key() == Qt.Key_C:
				self.copySelected()

			#Ctrl+V: Paste
			if event.key() == Qt.Key_V: self.paste()

			#Ctrl+Z: Undo
			if event.key() == Qt.Key_Z: print "Ctrl+Z"
			#Ctrl+Y: Redo
			if event.key() == Qt.Key_Y: print "Ctrl+Y"










	

	def mousePressEvent(self, event):
		item_at_pos = self.itemAt(event.scenePos())
		self._mouse_press_pos = event.scenePos()

		if self.line != None and item_at_pos == None: 
			self.line.start_obj.setSelected(False)
			self.removeItem(self.line.line_obj)
			self.line = None
			self.update()

		#else: self.startDrawingControlStructure()
		                                       


		super(CodeScene, self).mousePressEvent(event)


	def mouseMoveEvent(self, event):
		for line in self.connections: self.updateLinePosition(line)
		if self.line != None: 
			self.line.start_obj.setSelected(False)
			self.line.line_obj.setP2(event.scenePos())
			self.line.line_obj.setSelected(True)
			#self.addItem(self.line)
			self.update()


		super(CodeScene, self).mouseMoveEvent(event)


	def mouseReleaseEvent(self, event):
		self._mouse_release_pos = event.scenePos()
		self.boxDrawn()
		super(CodeScene, self).mouseReleaseEvent(event)

	def dragMoveEvent(self, event):
		print "drag"
		super(CodeScene, self).dragMoveEvent(event)















	def boxDrawn(self):
		start = self._mouse_press_pos
		end = self._mouse_release_pos

		ctrl = self.controlStructure()
		if ctrl !=  None:  #Draw the control structure
			ctrl.setPoints(start, end)
			for item in self.selectedItems(): ctrl.addItem(item) #Add items to structure
			self.addItem(ctrl)
			self.stopDrawingControlStructure()
			self.update()


	def updateLinePosition(self, line):
		start_point = line.start_obj._getNodeCenter(line.start_node)
		end_point = line.end_obj._getNodeCenter(line.end_node)

		line.line_obj.setP1(start_point)
		line.line_obj.setP2(end_point)


	def nodeClicked(self, mouse_event, node, node_pos, node_owner):

		if self.line == None:
			line_obj = BezierLine(node_pos)
			line_obj.setSelected(False)
			line_obj.setColor(node.color)
			self.addItem(line_obj)

			self.line = Line(line_obj, node, node_owner, None, None)

		elif node != self.line.start_node:
			#self.line.end_node = node
			#self.line.end_obj = node_owner
			self.line.line_obj.setP2(node_pos)
			self.connections.append(self.line)
			self.line = None

	def contextMenuEvent(self, event):
		if self.itemAt(event.scenePos()): super(CodeScene, self).contextMenuEvent(event) #Call the objects context menu
		else: self.menu.exec_(event.screenPos())


	def paste(self): 
		for obj in self.obj_clipboard:
			cpy = deepcopy(obj)
			cpy.__init__(scene)
			pos = self.views()[0].mapToScene(QCursor.pos())
			cpy.setPos(pos)
			self.addItem(cpy)

	def deleteSelected(self): 
		for item in self.selectedItems(): self.removeItem(item)

	def deleteAll(self): 
		for item in self.items(): self.removeItem(item)

	def selectAll(self): 
		for item in self.items(): item.setSelected(True)

	def copySelected(self):
		self.setClipboard(self.selectedItems())

background_color = Qt.white #QColor(128,128,128)
class CodeView(QGraphicsView):
	def __init__(self, scene):
		super(CodeView, self).__init__(scene)
		self.setAttribute(Qt.WA_StyledBackground)

		self.img_count = 0
		self.img_folder = '/home/jesse/Desktop/Img/'

		self._zoom_in_factor = 1.1
		self._zoom_out_factor = .9

		self.setRenderHints(
			QPainter.Antialiasing | 
			QPainter.SmoothPixmapTransform
			#QPainter.TextAntialiasing
		)

		self.setDragMode(QGraphicsView.RubberBandDrag)
		self.setBackgroundBrush(background_color)

		self.resize(750,400)


	def zoomIn(self):
		self.scale(self._zoom_in_factor, self._zoom_in_factor)

	def zoomOut(self):
		self.scale(self._zoom_out_factor, self._zoom_out_factor)

	def capture(self):
		self.img_count += 1
		file_name = "test.jpg" #self.img_folder + str(self.img_count)
		file_type = "JPG"

		viewport = self.viewport().rect()
		pix = QPixmap(viewport.width(), viewport.height())
		
		painter = QPainter(pix)
		painter.setRenderHints(
			QPainter.Antialiasing | 
			QPainter.SmoothPixmapTransform
			#QPainter.TextAntialiasing
		)

		self.render(painter)
		pix.save(file_name, file_type)
		del painter

	#def mouseReleaseEvent(self, event):
		#print QGraphicsView.rubberBandRect()
		#super(CodeScene, self).mouseReleaseEventevent(event)


	def keyPressEvent(self, event):
		
		#Ctrl..
		if QApplication.keyboardModifiers() == Qt.ControlModifier: 

			#Zoom in(Equal is Plus w/o pressing shift)
			if event.key() == Qt.Key_Equal: self.zoomIn()

			#Zoom out
			elif event.key() == Qt.Key_Minus: self.zoomOut()

		super(CodeView, self).keyPressEvent(event)



if __name__ == '__main__':

	app = QApplication(sys.argv)
	scene_backend = SceneBackend()
	scene = CodeScene()
	view = CodeView(scene)
	scene.addCodeObject(Packet(scene))
	scene.addCodeObject(Sleep(scene))
	#view.capture()
	view.show()
	app.exec_()


