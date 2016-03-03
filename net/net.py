# -*- coding: utf-8 -*-

from twisted.internet.endpoints import TCP4ClientEndpoint, SSL4ClientEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol, IAC, SB, SE, Telnet
from twisted.internet import reactor, error
from twisted.python.modules import getModule
from twisted.protocols import basic

import logging

logger = logging.getLogger(__name__)

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
        ## NOTE: I don't think this code is every used.
        if(self.gui):
            self.gui.connectionFailed(reason)

    def clientConnectionFailed(self, connector, reason):
        ## NOTE: I don't think this code is ever used.
        if(self.gui):
            self.gui.connectionFailed(reason)



class TelnetClient(StatefulTelnetProtocol):

    def close(self):
        self.transport.loseConnection()

    def terminfo(self, bytes):
        ## We want to write directly, not have this interpreted like poop
        self.transport._write(IAC + SB + TERMINFO + chr(0) + "thagoras" + IAC + SE)

    def oob(self, by):
        string = ''.join(by)
        logger.debug("OOB: %s" % string)
        self.factory.world.oob(string)

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
        logger.info("Server wanted us to %d" % ord(option))

        return False

    def enableRemote(self, option):
        if(option == GMCP):
            return True

        ## Log anything er aren't currently responding too
        logger.info("Server wanted to %d" % ord(option))
        return False

    def disableLocal(self, option):
        logger.info("Server told us to stop %d" % ord(option))
        return False

    def disableRemote(self, option):
        logger.info("Server wanted to stop %d" % ord(option))
        return False

    def connectionLost(self, reason):
        if not reason.check(error.ConnectionClosed):
            logger.warning("Lost Connection: %s" % reason.value)
            if(self.factory.gui):
                self.factory.gui.connectionFailed(reason.value)
        else:
            if(self.factory.gui):
                self.factory.gui.connectionFailed("Closed")


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
        world.mxp = False
        if(gui):
            gui.telnet = self

    def lineReceived(self, line):
        ## Debug log every line
        logger.debug("LINE: %s" % line)

        gui = self.factory.gui
        world = self.factory.world

        ### Setup Pueblo if we see the command
        res = line.find("This world is Pueblo 1.10 Enhanced.")
        if(res != -1):
            self.transport.write("PUEBLOCLIENT 1.10\n")
            self.factory.world.mxp = True

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

