import wx
import copy
import webbrowser, re, urllib2, StringIO
import threading

from twisted.internet import reactor, task

import obj.world
from ThagGuiBase import *
from util.url import urlre, urlImageGetter


import logging
logger = logging.getLogger(__name__)

class ThagOutputWindow(object):

    def __init__(self, *args, **kwds):
        self.telnet = None
        self.infowindow = None
        self.setColors()
        # Set default Style
        sty = wx.richtext.RichTextAttr()
        sty.SetBackgroundColour(wx.Colour(0,0,0))
        sty.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
        sty.SetTextColour(self.color[7])
        self.text_output.SetBasicStyle(sty)

        
        self.commandHistory = []
        self.isRecall = False

        self.contexts = {}
        self.text_output.Bind(wx.richtext.EVT_RICHTEXT_RIGHT_CLICK, self.OnRightClick)

        self.trimout = task.LoopingCall(self.setTrimLength)
        self.trimout.start(30.0)
        self.trimclean = True

    def commandMessage(self, message):
        self.text_output.SetInsertionPointEnd()
        self.text_output.BeginTextColour(self.color[9]);
        self.text_output.BeginBold()
        self.text_output.WriteText(message + "\n")
        self.text_output.ShowPosition(self.text_output.LastPosition)

    def connectionFailed(self, reason):
        self.commandMessage("Connection Failed: %s" % reason)
        self.telnet = None
        self.output.Disable()
        self.button_1.Disable()

    def setTrimLength(self):
        self.trimclean = False

    def trimLength(self):
        ltt = self.world.lines
        lines = self.text_output.GetNumberOfLines()
        if lines > ltt:
            diff = lines - ltt
            finalpos = self.text_output.XYToPosition(0,diff)
            self.text_output.Delete((0,finalpos))
        self.trimclean = True


    def OnKeyDown(self, event):
        key = event.GetKeyCode()

        ## Check for command recall
        if (key == wx.WXK_UP or key == wx.WXK_DOWN):
            if key == wx.WXK_UP:
                if not self.isRecall :
                    self.isRecall = True
                    self.commandHistoryIndex = 0
                else:
                    if self.commandHistoryIndex < (len(self.commandHistory)-1):
                        self.commandHistoryIndex += 1

            if key == wx.WXK_DOWN:
                if self.isRecall:
                    if self.commandHistoryIndex == 0:
                        self.isRecall = False
                        self.output.Clear()
                    else:
                        self.commandHistoryIndex -= 1

            if self.commandHistoryIndex < len(self.commandHistory) and self.isRecall:
                self.output.Clear()
                self.output.AppendText(self.commandHistory[self.commandHistoryIndex])

        event.Skip()


    def pushInput(self, inp):
        self.commandHistory.insert(0,inp)
        self.commandHistory = self.commandHistory[:15]
        self.isRecall = False

    def OnClose( self, event):
        ## Close the Telet Connection
        if self.telnet:
            self.telnet.close()

        ## Stop Trimming the output
        self.trimout.stop()

        ## Let wx handle the rest of the cleanup.
        event.Skip()

    def OnScroll(self, evt):
        self.text_output.ScrollLines(evt.GetWheelRotation()*-0.1)

    def OnSize(self, evt):
        if self.telnet:
            self.telnet.sendWindowSize()
        evt.Skip()

    def getWidth(self):
        f = self.text_output.GetFont()
        dc = wx.WindowDC(self.text_output)
        dc.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))

        (w1,h1) = dc.GetTextExtent("-" * 50)
        (w,h) = self.text_output.GetSize()

        return int(float((w-25))/(float(w1)/50.0))

    def OnOutFocus(self, evt):
        self.output.SetFocus()


    def OnRightClick(self, evt):
        sty = wx.richtext.RichTextAttr()
        self.text_output.GetStyle(evt.GetPosition(),style=sty)
        if sty.HasURL():
            sstr = sty.GetURL()
            if self.contexts.has_key(sstr):
                ## create Popup Menu
                popup = wx.Menu()
                ele = 0
                wantInfoWindow = False
                character = ""
                for xx in sstr.split('|'):
                    ## This is kind of a hackish way to do this, but assume it's a character if
                    ## We see a finger prompt
                    if xx.split(' ')[0].lower() == '+finger':
                        wantInfoWindow = True
                        character = ' '.join(xx.split(' ')[1:])

                    wxid = wx.NewId()

                    ## use the command if no hint field is given
                    if not self.contexts[sstr].tagsettings.has_key('hint'):
                        label = xx
                    else:
                        label = self.contexts[sstr].tagsettings['hint'].split('|')[ele+1]
                    aa = popup.Append(wxid, label)
                    popup.Bind(wx.EVT_MENU, lambda evt, command=xx:self.DoCommand(evt, command),aa)
                    ele += 1
                if wantInfoWindow:
                    ## Add a line to the menu to call the character info popout

                    popup.AppendSeparator()
                    charLabel = "Info Window for %s" % character
                    wxid = wx.NewId()
                    res = popup.Append(wxid, charLabel)
                    popup.Bind(wx.EVT_MENU, lambda evt, player=character:self.ShowInfo(evt, player), res)

                self.text_output.PopupMenu(popup, self.text_output.ScreenToClient(wx.GetMousePosition()))
                popup.Destroy()

    def ShowInfo(self, evt, player):
        if not self.infowindow:
            newWindow = ThagPersonInfo(self, self.world.world.profiles, player)
            self.infowindow = newWindow
            newWindow.Show()
        else:
            self.infowindow.updateInfo(self.world.world.profiles)
            self.infowindow.Select(player)
            self.infowindow.buildData()
            self.infowindow.Show()

    def HideInfo(self):
        self.infowindow = None

    def DoCommand(self, evt, command):
        self.world.send(command)

    def OnURL(self, evt):
        ## If I have a cached command, do that, otherise it's probably a URL
        if self.contexts.has_key(evt.GetString()):
            #Send the default href command
            cmd = evt.GetString().split('|')[0]
            self.DoCommand(evt, cmd)
        else:
            webbrowser.open(evt.GetString(), 2)

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
        pass

    def writeTo(self, inp, dest=None):
        ## Simple, we can ignore dest
        self.writeGUI(inp)

    def writeGUI(self, inp):

        destCtrl = self.text_output

        destCtrl.SetInsertionPointEnd()
        bold = False
        for c in inp.commands:
            ## Interprets Commands Here
            if c.type == "Text":
                if c.text != "":
                    destCtrl.WriteText(c.text)
            if c.type == "Newline":
                destCtrl.EndBold()
                destCtrl.EndTextColour()
                bold = False
                destCtrl.WriteText("\n")
            if c.type == "Font":
                if c.sub == "Normal":
                    destCtrl.EndBold()
                    destCtrl.EndTextColour()
                    bold = False
                if c.sub == "Bold":
                    destCtrl.BeginBold()
                    destCtrl.BeginTextColour(self.color[15]);
                    bold = True
                if c.sub == "SimpleColor":
                    d = c.color
                    if bold and d < 8:
                        d += 8  
                    destCtrl.EndTextColour()
                    destCtrl.BeginTextColour(self.color[d])
            if c.type == "Context":
                if c.tag.tagsettings.has_key('href'):
                    self.contexts[c.tag.tagsettings['href']] = c.tag
                    destCtrl.BeginURL(c.tag.tagsettings['href'])

            if c.type == "EndContext":
                destCtrl.EndURL()
            if c.type == "URL":
                destCtrl.BeginURL(c.url)
            if c.type == "EndURL":
                destCtrl.EndURL()

        if not self.trimclean:
            self.trimLength()
        destCtrl.SetInsertionPointEnd()
        destCtrl.ShowPosition(destCtrl.LastPosition)

    def OnSend(self, event):
        tts = self.output.GetLineText(0)

        self.pushInput(tts)

        ## Let the world handle the text output.
        self.world.send(tts)
        self.output.Clear()


class ThagOutputPanel(ThagOutputWindow, ThagOutputPanelBase):
    def __init__(self, *args, **kwds):
        self.world = kwds['world']
        kwds.pop('world')
        ThagOutputPanelBase.__init__(self, *args, **kwds)
        self.setColors()

        # Set default Style
        sty = wx.richtext.RichTextAttr()
        sty.SetBackgroundColour(wx.Colour(0,0,0))
        sty.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN,wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL))
        sty.SetTextColour(self.color[7])
        self.text_output.SetBasicStyle(sty)

        self.contexts = {}
        self.text_output.Bind(wx.richtext.EVT_RICHTEXT_RIGHT_CLICK, self.OnRightClick)

        self.trimout = task.LoopingCall(self.setTrimLength)
        self.trimout.start(30.0)
        self.trimclean = True

        self.parent = None

    def OnOutFocus(self, evt):
        self.parent.output.SetFocus()

    def DoCommand(self, evt, command):
        self.parent.character.send(command)


class ThagChannelOutputWindow(ThagOutputWindow):
    def __init__(self, *args, **kwds):
        self.telnet = None
        self.infowindow = None

        self.commandHistory = []
        self.isRecall = False

        # ThagOutputWindow.__init__(self)
        self.panels = {}
        self.last_inputs = dict()

        self.buildChars()

        ## Setup Images
        self.image_list = wx.ImageList(16, 16)
        self.greennum = self.image_list.Add(wx.Image("img/green.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap())

        self.chan_notebook.SetImageList(self.image_list)

    def OnScroll(self, evt):
        self.chan_notebook.GetCurrentPage().text_output.ScrollLines(evt.GetWheelRotation()*-0.1)

    def createPanel(self, panelName):
        newp = ThagOutputPanel(self.chan_notebook, world=self.world)
        newp.parent = self
        self.panels[panelName] = newp
        self.chan_notebook.AddPage(newp, panelName)

    def writeTo(self, inp, dest=None):
        ## Dedup inputs
        destpanel = inp.suboutput
        if not destpanel in self.last_inputs:
            self.last_inputs[destpanel] = list()

        # If we've already seen it, return.
        # use list str comp for now.  If too slow,
        # switch to city hash or something
        if inp.resultanttext in self.last_inputs[destpanel]:
            return

        self.last_inputs[destpanel].append(inp.resultanttext)

        # Only remember the last 10 or so.
        self.last_inputs[destpanel] = self.last_inputs[destpanel][-10:]

        if inp.suboutput not in self.panels:
            self.createPanel(inp.suboutput)
        self.panels[inp.suboutput].writeGUI(inp)

        if self.panels[inp.suboutput] != self.chan_notebook.GetCurrentPage():
            # This is the most ridiculous thing omg.
            for x in range(self.chan_notebook.GetPageCount()):
                if self.chan_notebook.GetPage(x) == self.panels[inp.suboutput]:
                    self.chan_notebook.SetPageImage(x, self.greennum)

    def OnChange(self, event):
        self.chan_notebook.SetPageImage(event.GetSelection(), wx.BookCtrlBase.NO_IMAGE)

    def buildChars(self):
        self.char_choice.Clear()
        for ch in self.world.chars:
            if ch.telnet:
                self.char_choice.Insert(ch.user, 0, ch)
        self.char_choice.SetSelection(0)

    @property
    def character(self):
        return self.char_choice.GetClientData(self.char_choice.GetSelection())

    def OnSend(self, event):
        tts = self.output.GetLineText(0)

        self.pushInput(tts)

        ## Let the world handle the text output.
        self.character.send(tts)
        self.output.Clear()


class ThagChannelFrame(ThagChannelOutputWindow, ThagWorldChannelFrameBase):
    def __init__(self, *args, **kwds):
        self.world = kwds['world']
        kwds.pop('world')
        ThagWorldChannelFrameBase.__init__(self, *args, **kwds)
        ThagChannelOutputWindow.__init__(self, *args, **kwds)


class ThagWorldFrame(ThagOutputWindow, ThagWorldFrameBase):
    def __init__(self, *args, **kwds):
        self.world = kwds['world']
        kwds.pop('world')
        ThagWorldFrameBase.__init__(self, *args, **kwds)
        ThagOutputWindow.__init__(self, *args, **kwds)


class ThagWorldDialog(ThagWorldDialogBase):
    def __init__(self, parent):
        ThagWorldDialogBase.__init__(self, parent)

        self.char_list.InsertColumn(0, "Character")
        self.char_list.InsertColumn(1, "Password")

        self.clist = {}
        self.deleteme = False

    def OnDeleteWorld(self, event):
        if self.deleteme:
            self.deleteme = False
            self.delete_button.SetLabel("Delete World")
        else:
            self.deleteme = True
            self.delete_button.SetLabel("Undelete World")

    def fillForm(self, world):
         ## Setup Dialog in here....
        self.world_name.SetValue(world.name)
        self.world_address.SetValue(world.address)
        self.world_port.SetValue(str(world.port))
        self.world_ssl.SetValue(world.ssl)
        self.lines_scrollback.SetValue(str(world.lines))


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
        world.ssl = self.world_ssl.GetValue()
        world.lines = int(self.lines_scrollback.GetValue())

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

    def OnInit(self, event):
        self.char_list.Select(0)

    def OnCharSave( self, event ):
        ii=self.char_list.GetNextSelected(-1)
        self.char_list.SetStringItem(ii,0, self.char_name.GetValue())
        self.char_list.SetStringItem(ii,1, self.char_pass.GetValue())
        cc = self.char_list.GetItemData(ii)
        c = self.clist[cc]
        c.user = self.char_name.GetValue()
        c.password = self.char_pass.GetValue()
    
    def OnCharRemove( self, event ):
        if self.char_list.GetItemCount() == 1:
            return

        ii=self.char_list.GetNextSelected(-1)

        cc = self.char_list.GetItemData(ii)
        self.clist.pop(cc)

        self.char_list.DeleteItem(ii)

        self.char_list.Select(0)

class ThagPersonInfo(ThagPersonInfoBase):
    def __init__(self, parent, information, selected = ""):
        self.parent = parent
        ThagPersonInfoBase.__init__(self, parent)
        self.notebookpanels = {}
        self.updateInfo(information)

        self.Select(selected)
        self.buildData()

    def Select(self, selected):
        n = self.person_selector.FindString(selected)
        if(n):
            self.person_selector.SetSelection(n)

    def OnClose(self, evt):
        self.parent.HideInfo()
        evt.Skip()

    def updateInfo(self, information):
        self.info = information
        self.people = self.info.keys()

        self.person_selector.Clear()
        for person in self.people:
            self.person_selector.Append(person)

    def OnSelectPerson(self, evt):
        self.buildData()
        evt.Skip()

    def buildData(self):
        ## Clean it out
        self.notebook.DeleteAllPages()

        person = self.person_selector.GetStringSelection()

        if(not self.info.has_key(person)):
            return

        for page, info in self.info[person].iteritems():
            newp = ThagPersonInfoPane(self.notebook, info)
            self.notebook.AddPage(newp, page)
        

class ThagPersonInfoPane(ThagPersonInfoPaneBase):
    def __init__(self, parent, info):
        self.info = info
        ThagPersonInfoPaneBase.__init__(self, parent)
        self.buildPage()

    def buildPage(self):
        self.info_list.InsertColumn(0,'Item')
        self.info_list.InsertColumn(1,'Value')
        self.general_info.Clear()
        ii = 0
        picture = None
        for key, value in self.info.iteritems():
            if(key.lower() == 'general'):

                self.general_info.AppendText(value)
            else:
                ##TODO: Make this better
                ## Not perfect, but try and find picture value
                if(key.lower() == 'picture'):
                    picture = key
                elif(key.lower().startswith('picture') and not picture):
                    picture = key

                self.info_list.InsertStringItem(ii,key)
                self.info_list.SetStringItem(ii,1,value)
                ii += 1

        self.info_list.SetColumnWidth(1, wx.LIST_AUTOSIZE)

        ##TODO:  Look for picture URLs
        ## Find a picture URL to show
        ### If we found a 'picture' 
        if(picture):
            rx = re.compile(urlre)
            mm = rx.search(self.info[picture])
            if(mm):
                tt = threading.Thread(target=self.showPicture, args=(mm.group(1),))
                tt.start()
                #self.showPicture(mm.group(1))

    def SetPicture(self, pic):
        try:
            self.person_picture.SetBitmap(pic)
        except:
            pass
        self.m_scrolledWindow1.SendSizeEvent()

    def showPicture(self, surl):
        url = urlImageGetter(surl)

        ## If the funciton returns None, then nothing to do
        if(not url):
            logger.info("Error finding URL for %s" % surl)
            return
        
        logger.info("Tried to load URL: %s" % url)
        try:
            buf = urllib2.urlopen(url).read()
            sbuf = StringIO.StringIO(buf)
            img = wx.ImageFromStream(sbuf).ConvertToBitmap()
        except:
            return
        wx.CallAfter(self.SetPicture,img)

