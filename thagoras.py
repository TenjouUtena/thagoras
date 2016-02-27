
import wx
import logging, sys, getopt

from twisted.internet import wxreactor
wxreactor.install()

# import twisted reactor *only after* installing wxreactor
from twisted.internet import reactor, protocol
from twisted.protocols import basic

from gui import ThagMainFrame
from obj import World
from util import settings

class Thagoras(wx.App):
    def OnInit(self):
       return 1

if __name__ == "__main__":


    log_level = logging.WARNING
    ## Parse Command Line stuff:
    try:
        opts, args = getopt.getopt(sys.argv[1:],"",["log=",])
    except GetoptError as e:
        print "Error with command line options: %s" % e.msg
        sys.exit(2)
    for opt, arg in opts:
        if(opt.lower() == '--log'):
            log_level = numeric_level = getattr(logging, arg.upper(), None)
            if(not log_level):
                log_level = logging.WARNING

    ## Setup python logging
    logging.basicConfig(filename="thagoras.log", level=log_level)

    app = Thagoras(0)
    thag_main_frame = ThagMainFrame(None, wx.ID_ANY, "")

    ## Autoload the file
    thag_main_frame.load(safe = True)
    app.SetTopWindow(thag_main_frame)
    thag_main_frame.Show()
    reactor.registerWxApp(app)
    reactor.run()
