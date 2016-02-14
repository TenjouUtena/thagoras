from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol
from twisted.internet import reactor

import util.logger as logger

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

    def enableLocal(self, option):
        rr = StatefulTelnetProtocol.enableLocal(self, option)
        logger.log("NEGOTIATE>%d" % ord(option))
        return rr

    def enableRemote(self, option):
        rr = StatefulTelnetProtocol.enableLocal(self, option)
        logger.log("NEGOTIATE SERVER>%d" % ord(option))
        return rr

    def disableLocal(self, option):
        rr = StatefulTelnetProtocol.enableLocal(self, option)
        logger.log("D.NEGOTIATE>%d" % ord(option))
        return rr

    def disableRemote(self, option):
        rr = StatefulTelnetProtocol.enableLocal(self, option)
        logger.log("D.NEGOTIATE SERVER>%d" % ord(option))
        return rr

    def connectionMade(self):
        self.setLineMode()
        gui = self.factory.gui
        world = self.factory.world 
        world.telnet = self
        if(gui):
            gui.telnet = self

    def lineReceived(self, line):
        gui = self.factory.gui
        world = self.factory.world
        if(world):
            world.recv(line)

    def write(self,command):
        return self.sendLine(command)       


