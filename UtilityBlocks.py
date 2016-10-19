from PyQt4.QtCore import Qt
from CodeObject import CodeObject, Node, In, Out, node_color
from CodeBlock import CodeBlock
import time

default_sleep_time = 500 #ms
class Sleep(CodeBlock):
	def __init__(self, scene): 
		super(Sleep, self).__init__(scene)
		self.sleep_time = default_sleep_time

		self.setTitle("Sleep")
		self.showTitleLine(False)
		self.setSize(50,30)
		self.setBorderColor(Qt.red)
		self.setThreaded(False)
		self.setTooltip(str(self.sleep_time) + "ms")

		self.registerVariable("time", In, default=default_sleep_time)

	def run(self): 
		time.sleep(self.sleep_time)




class Counter(CodeBlock):
	def __init__(self, scene):
		super(Counter, self).__init__(scene)
		self.setSize(30,30)
		#self.setTitle("")
		self.showTitleLine(False)
		self.addNode(Node("i", Qt.black, Out, "", None))

		self._count = 0

	def run(self): self._count += 1


#Class Break
