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
        self.setColors()
        # Set default Style
        sty = wx.richtext.RichTextAttr()
        sty.SetBackgroundColour(wx.Colour(0,0,0))
        sty.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
        sty.SetTextColour(self.color[7])
        self.text_output.SetBasicStyle(sty)

    def setColors(self):
        self.color = {}
        self.color[0] = wx.Colour(0,0,0)
        self.color[1] = wx.Colour(128,0,0)
        self.color[2] = wx.Colour(0,128,0)
        self.color[3] = wx.Colour(128,128,0)
        self.color[4] = wx.Colour(0,0,128)
        self.color[5] = wx.Colour(128,0,128)
        self.color[6] = wx.Colour(0,128,128)
        self.color[7] = wx.Colour(128,128,128)
        self.color[8] = wx.Colour(50,50,50)
        self.color[9] = wx.Colour(255,0,0)
        self.color[10] = wx.Colour(0,255,0)
        self.color[11] = wx.Colour(255,255,0)
        self.color[12] = wx.Colour(0,0,255)
        self.color[13] = wx.Colour(255,0,255)
        self.color[14] = wx.Colour(0,255,255)
        self.color[15] = wx.Colour(255,255,255)
        grayscale_start = 0x08
        grayscale_end = 0xf8
        grayscale_step = 10
        intensities = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]
        c = 16
        for i in intensities:
            for j in intensities:
                for k in intensities:
                    self.color[c] = wx.Colour(i,j,k)
                    c += 1


        c = 232
        for hex in list(range(grayscale_start, grayscale_end, grayscale_step)):
            self.color[c] = wx.Colour(hex,hex,hex)
            c += 1

    def writeLine(self, line):
        self.text_output.AppendText(line)
        self.text_output.AppendText("\n")
        self.text_output.ShowPosition(self.text_output.LastPosition)

    def writeGUI(self, inp):
        self.text_output.SetInsertionPointEnd()
        bold = False
        for c in inp.commands:
            ## Interprets Commands Here
            if(c.type == "Text"):
                if(c.text != ""):
                    self.text_output.WriteText(c.text)
            if(c.type == "Newline"):
                self.text_output.WriteText("\n")
            if(c.type == "Font"):
                if(c.sub == "Normal"):
                    self.text_output.EndBold()
                    self.text_output.EndTextColour()
                    bold = False
                if(c.sub == "Bold"):
                    self.text_output.BeginBold()
                    self.text_output.BeginTextColour(self.color[15]);
                    bold = True
                if(c.sub == "SimpleColor"):
                    d = c.color
                    if(bold and d < 8):
                        d += 8
                    self.text_output.EndTextColour()
                    self.text_output.BeginTextColour(self.color[d])
        
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
    


