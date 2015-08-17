

class Character():
	def __init__(self, world, user="", password=""):
		self.world = world
		self.user = user
		self.password = password
		self.setupVars()

	def setupVars(self):
		self.gui = None
		self.telnet = None
		self.outputs = {}
		self.inputs = {}
		self.filters = {}

	def __getstate__(self):
		odict = self.__dict__.copy()
		odict.pop('world')
		return odict

	def __setstate__(self, dd):
		self.setupVars()
		self.__dict__.update(dd)

class World():
	def __init__(self,name="",address="",port=0):
		self.address = address
		self.port = port
		self.name = name
		self.setupVars()

	def setupVars(self):
		self.chars = []
		self.gui = None
		self.telnet = None
		self.outputs = {}
		self.inputs = {}
		self.filters = {}

	def send(self, line):
		self.telnet.write(str(line))

	def setCharWorld(self):
		for c in self.chars:
			c.world = self		

	### Pickle Stuff
	def __getstate__(self):
		odict = self.__dict__.copy()
		odict.pop('gui')
		odict.pop('telnet')
		return odict

	def __setstate__(self, dd):
		self.setupVars()
		self.__dict__.update(dd)
		self.setCharWorld()


		
