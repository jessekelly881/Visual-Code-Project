from misc import checkTypes
from CodeBlock import ExecutableBlock
from collections import namedtuple


class SceneBackend:
	def __init__(self):
		self._objects = []
		self._links = []

		self._known_objects = []

	@checkTypes(object, ExecutableBlock)
	def registerObject(self, obj):pass


	def removeObject(self, obj): pass

	def registerConnection(self, connection): pass

	def removeConnection(self, connection): pass

	def addKnownObject(self, obj): pass
	def knownObjects(self): pass