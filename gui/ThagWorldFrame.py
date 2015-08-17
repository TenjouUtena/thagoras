import wx
import copy


import obj.world

from ThagGuiBase import *


class ThagWorldFrame(ThagWorldFrameBase):
    def __init__(self, *args, **kwds):
        self.world = kwds['world']
        kwds.pop('world')
        ThagWorldFrameBase.__init__(self, args[0])
        self.telnet = None

    def writeLine(self, line):
        self.text_output.AppendText(line)
        self.text_output.AppendText("\n")
        self.text_output.ShowPosition(self.text_output.LastPosition)

    def OnSend(self, event):
        tts = self.output.GetLineText(0)

        ## Let the world handle the text output.
        self.world.send(tts)
        self.output.Clear()

class ThagWorldDialog(ThagWorldDialogBase):
    def __init__(self, parent):
        ThagWorldDialogBase.__init__(self, parent)

        self.char_list.InsertColumn(0, "Character")
        self.char_list.InsertColumn(1, "Password")

        self.clist = {}

    def fillForm(self, world):
         ## Setup Dialog in here....
        self.world_name.SetValue(world.name)
        self.world_address.SetValue(world.address)
        self.world_port.SetValue(str(world.port))


        cc = 0
        for c in world.chars :
            self.char_list.InsertStringItem(cc,c.user)
            self.char_list.SetStringItem(cc,1,c.password)
            self.char_list.SetItemData(cc,cc)
            self.clist[cc] = copy.copy(c)

            cc = cc + 1


    def writeObj(self, world):
        world.name = self.world_name.GetValue()
        world.address = self.world_address.GetValue()
        world.port = int(self.world_port.GetValue())

        world.chars = copy.copy(self.clist.values())
        world.setCharWorld()

    def OnCharSelect(self, event):
        #ii=self.char_list.GetNextSelected(0)
        ii = event.Index
        cc = self.char_list.GetItemData(ii)
        self.char_name.SetValue(self.clist[cc].user)
        self.char_pass.SetValue(self.clist[cc].password)


    def OnCharAdd( self, event ):
        cc = self.char_list.GetItemCount()

        c = obj.world.Character(None, "New", "New")

        self.clist[cc] = c

        self.char_list.InsertStringItem(cc,"New")
        self.char_list.SetStringItem(cc,1,"New")
        self.char_list.SetItemData(cc,cc)

        self.char_name.SetValue("New")
        self.char_pass.SetValue("New")

    def OnCharSave( self, event ):
        ii=self.char_list.GetNextSelected(-1)
        self.char_list.SetStringItem(ii,0, self.char_name.GetValue())
        self.char_list.SetStringItem(ii,1, self.char_pass.GetValue())
        cc = self.char_list.GetItemData(ii)
        c = self.clist[cc]
        c.user = self.char_name.GetValue()
        c.password = self.char_pass.GetValue()
    
    def OnCharRemove( self, event ):
        event.Skip()
    


