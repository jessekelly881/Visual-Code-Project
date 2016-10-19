from collections import namedtuple


#Immutable objects
Variable = namedtuple("Variable", ['name', 'valid_datatypes', 'value', 'is_input', 'owner', 'connections', 'active'])
Connection = namedtuple("Connection", ['input_var', 'input_block', 'output_var', 'output_block'])
CodeBlock = namedtuple("CodeBlock", ['name', 'variables', 'run_function', 'threaded'])

class State (
	namedtuple("State", ['codeblocks', 'variables', 'connections'])):

	#Check if all active variables have input connections of the right type
	def isExecutable(self):
		pass

	#Display state tree
	def __str__(self): pass

	#Way to combine two states and form a new one
	def __add__(self, other_state): 
		return self._replace(
			codeblocks= self.codeblocks + other_state.codeblocks,
			variables=self.variables + other_state.variables,
			connections=self.connections + other_state.connections)

