
import wx


from twisted.internet import wxreactor
wxreactor.install()

from gui import ThagMainFrame
from obj import World
from util import settings


# import twisted reactor *only after* installing wxreactor
from twisted.internet import reactor, protocol
from twisted.protocols import basic


# end of class ThagMainFrame
class Thagoras(wx.App):
    def OnInit(self):
       return 1



if __name__ == "__main__":
#    gettext.install("app") # replace with the appropriate catalog name

    worlds = []

    data = settings.LoadSafe()
    if(data):
        worlds = data[0]

    #Debug World:
    #worlds.append(World("Penn - Asuka","penultimatemush.com",9500))

    app = Thagoras(0)
    thag_main_frame = ThagMainFrame(None, wx.ID_ANY, "",worlds=worlds)
    app.SetTopWindow(thag_main_frame)
    thag_main_frame.Show()

    reactor.registerWxApp(app)
    reactor.run()


    #app.MainLoop()
