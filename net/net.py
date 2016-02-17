from twisted.internet.endpoints import TCP4ClientEndpoint, SSL4ClientEndpoint
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol
from twisted.internet import reactor, ssl, error
from twisted.python.modules import getModule

from OpenSSL import crypto

import util.logger as logger

def connect(host, port, gui, world):
    ep = TCP4ClientEndpoint(reactor, host, port)
    tf = TelnetFactory(gui, world)
    tf.protocol = TelnetClient
    tt = ep.connect(tf)
    return tt

def connectSSL(host, port, gui, world):
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "Minnesota"
    cert.get_subject().L = "Minnetonka"
    cert.get_subject().O = "my company"
    cert.get_subject().OU = "my organization"
    cert.get_subject().CN = "blah"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    #authData = getModule(__name__).filePath.sibling('mykey.pem').getContent()
    cc =ssl.PrivateCertificate.loadPEM(crypto.dump_certificate(crypto.FILETYPE_PEM, cert) + crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
    options = ssl.optionsForClientTLS(u'penultimatemush.com', clientCertificate=cc)
    ep = SSL4ClientEndpoint(reactor, host, port, options)
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

    def unhandledSubnegotiation(self, command, by):
        rr = StatefulTelnetProtocol.unhandledSubnegotiation(self, command, by)
        logger.log("SUB NEG Command: %d  %")
        return rr

    def enableLocal(self, option):
        #rr = StatefulTelnetProtocol.enableLocal(self, option)
        logger.log("NEGOTIATE>%d" % ord(option))
        if(option == chr(24)):
            return True
        return False

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

    def connectionLost(self, reason):
        print("Lost.")
        if not reason.check(error.ConnectionClosed):
            print("BAD:", reason.value)

    def connectionMade(self):
        #self.transport.do(chr(24)  ## We want to negotiate about this
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


