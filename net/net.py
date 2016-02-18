from twisted.internet.endpoints import TCP4ClientEndpoint, SSL4ClientEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol,   IAC, SB, SE, Telnet
from twisted.internet import reactor, ssl, error
from twisted.python.modules import getModule
from twisted.protocols import basic

from OpenSSL import crypto

import util.logger as logger

## Defines

TERMINFO = chr(24)
NAWS = chr(31)

GMCP = chr(201)


def connect(host, port, gui, world):
    ep = TCP4ClientEndpoint(reactor, host, port)
    tf = TelnetFactory(gui, world)
    tf.protocol = TelnetClient
    tt = ep.connect(tf)
    return tt

def connectSSL(host, port, gui, world):
    ep = SSL4ClientEndpoint(reactor, host, port, ssl.ClientContextFactory())
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

    def terminfo(self, bytes):
        ## We want to write directly, not have this interpreted like poop
        self.transport._write(IAC + SB + TERMINFO + chr(0) + "thagoras" + IAC + SE)

    def sendWindowSize(self):
        if(not self.factory.world):
            return

        if(not self.naws):
            return

        width = self.factory.world.getWidth()
        ## Always return 24 for height, it shouldn't matter.
        wbig = int(width / 256)
        wsmall = int(width % 256)

        self.transport._write(IAC + SB + NAWS + chr(wbig) + chr(wsmall) + chr(0) + chr(24) + IAC + SE)



    def unhandledSubnegotiation(self, command, by):
        rr = StatefulTelnetProtocol.unhandledSubnegotiation(self, command, by)
        logger.log("SUB NEG Command: %s  %s" % (command,by))
        return rr

    def enableLocal(self, option):
        
        ## Allow us to be asked about TERMINFO
        if(option == TERMINFO):
            return True

        ## Allow us to be asked about NAWS
        if(option == NAWS):
            self.naws = True
            self.sendWindowSize()
            return True

        ## Log anything er aren't currently responding too
        logger.log("NEGOTIATE>%d" % ord(option))

        return False

    def enableRemote(self, option):
        if(option == GMCP):
            return True

        ## Log anything er aren't currently responding too
        logger.log("NEGOTIATE SERVER>%d" % ord(option))
        return False

    def disableLocal(self, option):
        rr = StatefulTelnetProtocol.enableLocal(self, option)
        logger.log("D.NEGOTIATE>%d" % ord(option))
        return rr

    def disableRemote(self, option):
        rr = StatefulTelnetProtocol.enableLocal(self, option)
        logger.log("D.NEGOTIATE SERVER>%d" % ord(option))
        return rr

    def connectionLost(self, reason):
        #print("Lost.")
        if not reason.check(error.ConnectionClosed):
            print("BAD:", reason.value)

    def connectionMade(self):
        ## Twisted is put together weird
        ## So initialization is here
        ## No real biggie


        self.transport.negotiationMap[TERMINFO] = self.terminfo
        self.naws = False
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


