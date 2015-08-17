

class World():
	def __init__(self,name="",address="",port=0):
		self.gui = None
		self.telnet = None
		self.address = address
		self.port = port
		self.name = name
		self.user = ""
		self.password = ""

	def send(self, line):
		self.telnet.write(str(line))


	### Pickle Stuff
	def __getstate__(self):
		odict = self.__dict__.copy()
		odict.pop('gui')
		odict.pop('telnet')
		return odict

	def __setstate__(self, dd):
		self.__dict__.update(dd)
		if(not self.__dict__.has_key('gui')): self.gui = None
		if(not self.__dict__.has_key('telnet')): self.gui = None
		
