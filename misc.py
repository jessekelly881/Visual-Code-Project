import datetime
from PyQt4.QtGui import QMenu

def checkTypes(*types):
	def decorator(func):
		def newFunc(*args, **kw):
			length = min(len(args), len(types))
			for i in range(0,length): 
				assert isinstance(args[i], types[i])

			ret = func(*args)
			return ret

		return newFunc
	return decorator



#{'name' : action}
def createMenuFromDict(dictionary):
	menu = QMenu()
	for name, item in dictionary.iteritems(): 
		if isinstance(item, dict): 
			submenu = createMenuFromDict(item)
			submenu.setTitle(name)
			menu.addMenu(submenu)
		
		else:
			menu_action = menu.addAction(name)
			menu_action.triggered.connect(item)

	return menu

def log(f):
	def _decorator(*arg, **kw):
		ret = f(*arg)
		time_str = "[" + str(datetime.datetime.utcnow()) + "]"    
		print time_str + "\t" + f.__name__, "(" +  ",".join(map(str,arg)) + ") -> ", str(ret)
		return ret

	return _decorator

if __name__ == '__main__':
	@checkTypes(int, str)
	def add(a,b):
		return a + b

	print add(6,6)