import wx
import net.net as net
from ThagWorldFrame import ThagWorldFrame, ThagWorldDialog
from ThagGuiBase import *

from obj.world import World

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

        self.prefs = {}

        self.connectmenus = []
        self.subconmenus = {}
        self.editmenus = []

        ## Programatically add the worlds.
        self.makeWorldMenus()

    def OnExitCommand(self, event):
        self.Destroy()


    def makeWorldMenus(self):
        if(self.worlds):
            for ww in self.worlds:
                wsubmenu1 = wx.MenuItem(self.connect_menu, wx.ID_ANY, ww.name, "", wx.ITEM_NORMAL)
                wsubmenuM = wx.Menu()
                self.subconmenus[wsubmenuM] = []

                for cc in ww.chars:
                    submenu1 = wx.MenuItem(wsubmenuM, wx.ID_ANY, "%s - %s" % (ww.name, cc.user), "", wx.ITEM_NORMAL)
                    self.Bind(wx.EVT_MENU, lambda evt, charr=cc: self.DoConnect(evt, charr), submenu1)
                    wsubmenuM.AppendItem(submenu1)
                    self.subconmenus[wsubmenuM].append(submenu1)

                wsubmenu1.SetSubMenu(wsubmenuM)
                self.connect_menu.AppendItem(wsubmenu1)
                self.connectmenus.append(wsubmenu1)

                submenu2 = wx.MenuItem(self.connect_menu, wx.ID_ANY, ww.name, "", wx.ITEM_NORMAL)
                self.edit_menu.AppendItem(submenu2)
                self.Bind(wx.EVT_MENU, lambda evt, world=ww: self.DoEdit(evt, world), submenu2)
                self.editmenus.append(submenu2)

    def destroyWorldMenus(self):
        for o in self.subconmenus.keys():
            for p in self.subconmenus[o]:
                o.Delete(p.GetId())

        for o in self.connectmenus:
            self.connect_menu.Delete(o.GetId())

        for o in self.editmenus:
            self.edit_menu.Delete(o.GetId())

        self.connectmenus = []
        self.editmenus = []
        self.subconmenus = {}

    def refresh(self):
        self.destroyWorldMenus()
        self.makeWorldMenus()
                
    def DoConnect(self, event, charr):
        ## Create window
        ww = ThagWorldFrame(self, world=charr)
        ww.SetTitle(charr.world.name + ' - ' + charr.user)
        charr.gui = ww

        tt = net.connect(charr.world.address, charr.world.port, ww, charr)
        ww.Show()

    def DoEdit(self, event, world):
        dlg = ThagWorldDialog(self)

        dlg.fillForm(world)

        if dlg.ShowModal() == wx.ID_OK:
            dlg.writeObj(world)
            self.refresh()

    def OnClose(self, event):
        if(self.prefs.get('saveonclose')):
            self.save()
        event.Skip()

    def save(self):
        settings.Save(self.worlds, self.prefs)

    def OnNewWorld(self, event):
        dlg = ThagWorldDialog(self)

        if dlg.ShowModal() == wx.ID_OK:
            world = World()
            dlg.writeObj(world)
            self.worlds.append(world)
            self.refresh()


    def OnSettings(self, event):
        dlg = ThagMainDialog(self)

        dlg.fillForm(self.prefs)

        if dlg.ShowModal() == wx.ID_OK:
            dlg.writeObj(self.prefs)

    def DoLoad(self, event):
        self.load()

    ## Unpack the loaded data
    def load(self):
        self.destroyWorldMenus()
        data = settings.Load()
        if(data):
            self.worlds = data[0]
        if(len(data) >= 2):
            self.prefs = data[1]
        self.makeWorldMenus()

    def DoSave(self, event):
        self.save()






class ThagMainDialog(ThagMainDialogBase):
    def fillForm(self, prefs):
        if(prefs.get('saveonclose')):
            self.save_on_close.SetValue(True);


    def writeObj(self, prefs):
        prefs['saveonclose'] = self.save_on_close.GetValue()


