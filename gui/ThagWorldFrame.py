import wx
import copy
import obj.world
from ThagGuiBase import *
import webbrowser


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

        self.contexts = {}
        self.text_output.Bind(wx.EVT_TEXT_URL, self.OnURL)
        self.text_output.Bind(wx.richtext.EVT_RICHTEXT_RIGHT_CLICK, self.OnRightClick)
        self.text_output.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, evt):
        if(self.telnet):
            self.telnet.sendWindowSize()
        evt.Skip()

    def getWidth(self):
        f = self.text_output.GetFont()
        dc = wx.WindowDC(self.text_output)
        dc.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))

        (w1,h1) = dc.GetTextExtent("-" * 50)
        (w,h) = self.text_output.GetSize()

        #print w1,h1,w,h,float(w)/(float(w1)/50.0), w/(w1/50)
        ## 21% kerning?  idgaf
        return int(float((w-25))/(float(w1)/50.0))

    def OnOutFocus(self, evt):
        self.output.SetFocus()


    def OnRightClick(self, evt):
        sty = wx.richtext.RichTextAttr()
        self.text_output.GetStyle(evt.GetPosition(),style=sty)
        if(sty.HasURL()):
            sstr = sty.GetURL()
            if(self.contexts.has_key(sstr)):
                ## create Popup Menu
                popup = wx.Menu()
                ele = 0
                for xx in sstr.split('|'):
                    wxid = wx.NewId()
                    aa = popup.Append(wxid, self.contexts[sstr].tagsettings['hint'].split('|')[ele+1])
                    popup.Bind(wx.EVT_MENU, lambda evt, command=xx:self.DoCommand(evt, command),aa)
                    ele += 1
                self.text_output.PopupMenu(popup, self.text_output.ScreenToClient(wx.GetMousePosition()))
                popup.Destroy()

    def DoCommand(self, evt, command):
        self.world.send(command)

    def OnURL(self, evt):
        ## If I have a cached command, do that, otherise it's probably a URL
        if(self.contexts.has_key(evt.GetString())):
            #Send the default href command
            cmd = evt.GetString().split('|')[0]
            self.world.send(cmd)
        else:
            webbrowser.open(evt.GetString(),2)

    def setColors(self):
        self.color = {}
        self.color[0] = wx.Colour(0,0,0)
        self.color[1] = wx.Colour(128,0,0)
        self.color[2] = wx.Colour(0,128,0)
        self.color[3] = wx.Colour(128,128,0)
        self.color[4] = wx.Colour(0,0,128)
        self.color[5] = wx.Colour(128,0,128)
        self.color[6] = wx.Colour(0,128,128)
        self.color[7] = wx.Colour(0xAF,0xAF,0xAF)
        self.color[8] = wx.Colour(0x5F,0x5F,0x5F)
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
            if(c.type == "Context"):
                if(c.tag.tagsettings.has_key('href')):
                    self.contexts[c.tag.tagsettings['href']] = c.tag
                    self.text_output.BeginURL(c.tag.tagsettings['href'])

            if(c.type == "EndContext"):
                self.text_output.EndURL()
            if(c.type == "URL"):
                self.text_output.BeginURL(c.url)
            if(c.type == "EndURL"):
                self.text_output.EndURL()


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
    


