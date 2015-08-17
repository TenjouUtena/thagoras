import wx
import net.net as net
from ThagWorldFrame import ThagWorldFrame
from ThagGuiBase import *
from util import settings


def setTelnetProps(gui, telnet):
    print called
    print gui
    print telnet
    gui.telnet = telnet

class ThagMainFrame(ThagMainFrameBase):
    def __init__(self, *args, **kwds):
        self.worlds = kwds['worlds']
        kwds.pop('worlds')

        ThagMainFrameBase.__init__(self, None)

        self.connectmenus = []
        self.editmenus = []

        ## Programatically add the worlds.
        self.makeWorldMenus()



    def makeWorldMenus(self):
        if(self.worlds):
            for ww in self.worlds:
                submenu1 = wx.MenuItem(self.connect_menu, wx.ID_ANY, ww.name, "", wx.ITEM_NORMAL)
                self.connect_menu.AppendItem(submenu1)
                self.Bind(wx.EVT_MENU, lambda evt, world=ww: self.DoConnect(evt, world), submenu1)
                self.connectmenus.append(submenu1)

                submenu2 = wx.MenuItem(self.connect_menu, wx.ID_ANY, ww.name, "", wx.ITEM_NORMAL)
                self.edit_menu.AppendItem(submenu2)
                self.Bind(wx.EVT_MENU, lambda evt, world=ww: self.DoEdit(evt, world), submenu2)
                self.editmenus.append(submenu2)
                
    def DoConnect(self, event, world):
        ## Create window
        ww = ThagWorldFrame(self, world=world)
        world.gui = ww

        tt = net.connect(world.address, world.port, ww, world)
        ww.Show()

    def DoEdit(self, event, world):
        dlg = ThagWorldDialog(self)
        ## Setup Dialog in here....
        dlg.world_name.SetValue(world.name)
        dlg.world_address.SetValue(world.address)
        dlg.world_port.SetValue(str(world.port))
        #dlg.world_name.SetValue(world.name)

        dlg.ShowModal();


    def OnNewWorld(self, event):
        dlg = ThagWorldDialog(self)
        dlg.ShowModal();

    def DoLoad(self, event):
        pass

    def DoSave(self, event):
        settings.Save(self.worlds)





