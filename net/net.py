

from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol
from twisted.internet import reactor

def connect(host, port, gui, world):
	ep = TCP4ClientEndpoint(reactor, host, port)
	tf = TelnetFactory(gui, world)
	tf.protocol = TelnetClient
	tt = ep.connect(tf)
	return tt

class TelnetFactory(ClientFactory):
    def __init__(self, gui, world):
    	self.gui = gui
    	self.world = world

    def buildProtocol(self, addr):
        self.transport = TelnetTransport(TelnetClient)
        self.transport.factory = self
        return self.transport

    def setLogoutCommand(self,cmd):
        self.exit_command = cmd
 
    def clientConnectionLost(self, connector, reason):
    	pass

    def clientConnectionFailed(self, connector, reason):
    	pass



class TelnetClient(StatefulTelnetProtocol):

    def connectionMade(self):
        self.setLineMode()

        gui = self.factory.gui
        world = self.factory.world 

        world.gui = gui
        world.telnet = self
        
        if(gui):
        	gui.telnet = self

    def lineReceived(self, line):
    	gui = self.factory.gui

    	if(gui):
    		gui.writeLine(line)


    def write(self,command):
        return self.sendLine(command)    	


