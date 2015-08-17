import wx

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

