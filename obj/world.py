

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
		self.telnet.write(line)
