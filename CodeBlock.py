from CodeObject import CodeObject

class ExecutableBlock: 
	def __init__(self):
		self._variables = {}
		self._threaded = True

	def run(self): pass
	def isRunable(self): pass

	def setVariableValue(self, name, value): 
		self._variables[name] = value

	def variableValue(self, name): 
		return self._variables[name]

	def registerVariable(self, name, is_input, default = None): pass

	def setThreaded(self, threaded): self._threaded = threaded
	def threaded(self): return self._threaded





class CodeBlock(CodeObject, ExecutableBlock): 
	def __init__(self, scene):
		super(CodeBlock, self).__init__(scene)



if __name__ == '__main__':
	block = ExecutableBlock()