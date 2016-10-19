from PyQt4.QtCore import Qt
from CodeObject import Node, node_color, In, Out
from CodeObject import CodeObject


class TwoVariableMathObject(CodeObject):
	def __init__(self, scene, name = "", return_str = "Out", operator_func = None):
		super(TwoVariableMathObject, self).__init__(scene)
		self.setSize(85,85)
		self.setTitle(name)
		self.addNodes([
			Node("x", Qt.red, In, "x", None),
			Node("y", Qt.red, In, "y", None),
			Node(return_str, Qt.red, Out, "out", None)
			])
		self.setTooltip(
"""x: numpy array
y: numpy array
Returns: numpy array""")

		#self.setInputVariableList(['x','y'])		

Add = lambda scene: TwoVariableMathObject(scene, "x+y")
Sub = lambda scene: TwoVariableMathObject(scene, "Subtract", "x-y")



def ModuleMain(scene): pass
	#Register objects in file
	




