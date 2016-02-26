# -*- coding: utf-8 -*-

from twisted.internet.endpoints import TCP4ClientEndpoint, SSL4ClientEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol, IAC, SB, SE, Telnet
from twisted.internet import reactor, error
from twisted.python.modules import getModule
from twisted.protocols import basic

import util.logger as logger

## Defines

TERMINFO = chr(24)
NAWS = chr(31)

GMCP = chr(201)


def connect(host, port, gui, world):
    if(world.world.ssl):
        from twisted.internet import ssl
        ep = SSL4ClientEndpoint(reactor, host, port, ssl.ClientContextFactory())
    else:
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

    def close(self):
        self.transport.loseConnection()

    def terminfo(self, bytes):
        ## We want to write directly, not have this interpreted like poop
        self.transport._write(IAC + SB + TERMINFO + chr(0) + "thagoras" + IAC + SE)

    def oob(self, by):
        self.factory.world.oob(''.join(by))

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
        self.transport.negotiationMap[GMCP] = self.oob
        self.naws = False
        self.hasconned = False
        self.setLineMode()
        gui = self.factory.gui
        world = self.factory.world 
        world.telnet = self
        if(gui):
            gui.telnet = self

    def lineReceived(self, line):
        gui = self.factory.gui
        world = self.factory.world

        ### Setup Pueblo if we see the command
        res = line.find("This world is Pueblo 1.10 Enhanced.")
        if(res != -1):
            self.transport.write("PUEBLOCLIENT 1.10\n")

        ## We want to make sure we're sending the autocon at _about_ the right time
        ## so we look for the sting 'con' as in 'connect'
        ## Only MUSH-style supported right now.   ゴメンナサイ
        if(not self.hasconned):
            if(line.find('con') != -1):
                self.transport.write(("con %s %s\n" % (world.user, world.password)).encode('cp1252'))
                self.hasconned = True


        if(world):
            world.recv(line)

    def write(self,command):
        return self.sendLine(command)

