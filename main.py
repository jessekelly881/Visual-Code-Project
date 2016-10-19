#!/usr/bin/env python

from IPEmbeded import IPythonWidget
#from IPython.external.qt import QtCore, QtGui

from PyQt4 import QtGui, QtCore
from CodeScene import CodeScene, CodeView

class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.resize(800,700)
		self.frameless = False

		status_bar = QtGui.QStatusBar(self)
		self.setStatusBar(status_bar)

		self._ipyActive = False
		self.ipWidget = None

		self._createMenuBar()
		self._setupLayout()
		self._addCanvasTab()

	def _setupLayout(self):
		self.splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
		self.setCentralWidget(self.splitter)

		self.tabs = QtGui.QTabWidget()
		self.tabs.setTabsClosable(True)
		self.tabs.setMovable(True)
		self.tabs.tabCloseRequested.connect(self._removeCanvasTab)
		self.splitter.addWidget(self.tabs)


	def _addCanvasTab(self, name = 'untitled'): 
		scene = CodeScene()
		self.tabs.addTab(CodeView(scene),name)

	def _removeCanvasTab(self, index):
		self.tabs.removeTab(index)

	def _createMenuBar(self): 
		menubar = self.menuBar()
		#menubar.setNativeMenuBar(False)

		#File Menu--------------------------------
		fileMenu = menubar.addMenu('&File')

		newAction = QtGui.QAction('New', self)
		newAction.setShortcuts(['Ctrl+N', 'Ctrl+T'])
		newAction.triggered.connect(self.new)
		fileMenu.addAction(newAction)

		saveAction = QtGui.QAction('Save', self)
		saveAction.setShortcut('Ctrl+S')
		saveAction.triggered.connect(self.save)
		fileMenu.addAction(saveAction)

		saveAsAction = QtGui.QAction('Save As', self)
		saveAsAction.triggered.connect(self.saveAs)
		fileMenu.addAction(saveAsAction)

		exitAction = QtGui.QAction('Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.triggered.connect(self.quit)
		fileMenu.addAction(exitAction)
		#-----------------------------------------


		#View Menu--------------------------------
		viewMenu = menubar.addMenu('&View')

		self.showIPythonAction = QtGui.QAction('Show IPython Console', self)
		self.showIPythonAction.triggered.connect(self.showIPython)
		self.showIPythonAction.setShortcut('Ctrl+I')
		viewMenu.addAction(self.showIPythonAction)

		self.borderless = QtGui.QAction('Toggle Borderless', self)
		self.borderless.triggered.connect(self.toggleBorderless)
		self.borderless.setShortcut('F12')
		viewMenu.addAction(self.borderless)
		#-----------------------------------------


	def toggleBorderless(self): 
		if not self.frameless: self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
		else: self.setWindowFlags(self.windowFlags() & QtCore.Qt.FramelessWindowHint & QtCore.Qt.WindowStaysOnTopHint)
		self.show()
		self.frameless = not self.frameless


	def new(self): self._addCanvasTab('untitled')
	def save(self): print "save"
	def saveAs(self): print "save as"
	def quit(self): sys.exit()

	
	def showIPython(self): 
		if self.ipWidget == None: #Construct the widget
			self.ipWidget = IPythonWidget(self)
			#self.ipWidget.setMinimumSize(800,300)
			self.splitter.addWidget(self.ipWidget)

		else: #Show an already constructed widget that has been hiden
			self.ipWidget.setParent(self)
			self.splitter.addWidget(self.ipWidget)

		#Change visable menu buttont 
		self._ipyActive = True
		self.showIPythonAction.setText('Hide IPython Console')
		self.showIPythonAction.triggered.connect(self.hideIPython)


	def hideIPython(self):
		self.ipWidget.setParent(None)

		#Change visable menu button
		self._ipyActive = False
		self.showIPythonAction.setText('Show IPython Console')
		self.showIPythonAction.triggered.connect(self.showIPython)

	


if __name__ == '__main__':
	import sys

	app = QtGui.QApplication(sys.argv)
	main = MainWindow()
	main.show()
	app.exec_()

