from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from copy import deepcopy
import util.logger as logger
import re
import util.url as url

class Command():
    def __init__(self):
        self.type = "Generic"
        self.text = ""

class TextCommand(Command):
    def __init__(self, text=""):
        Command.__init__(self)
        self.type = "Text"
        self.text = text

class TagCommand(Command):
    def __init__(self):
        Command.__init__(self)
        self.type = "Tag"
        self.tagtype = ""
        self.tagsettings = {}

class EndTagCommand(Command):
    def __init__(self):
        Command.__init__(self)
        self.type = "EndTag"
        self.tagtype = ""
        self.tagsettings = {}
class NewLineCommand(Command):
    def __init__(self, text=""):
        Command.__init__(self)
        self.type = "Newline"
        self.text = text

class FontCommand(Command):
    def __init__(self, text=""):
        Command.__init__(self)
        self.type = "Font"
        self.sub = "Normal"
        self.color = 0
        self.text = text

class ContextCommand(Command):
    def __init__(self, text=""):
        Command.__init__(self)
        self.type = "Context"
        self.text = ""

class ContextEndCommand(Command):
    def __init__(self, text=""):
        Command.__init__(self)
        self.type = "EndContext"
        self.text = ""

class URLCommand(Command):
    def __init__(self, text=""):
        Command.__init__(self)
        self.type = "URL"
        self.url = ""

class URLEndCommand(Command):
    def __init__(self, text=""):
        Command.__init__(self)
        self.type = "EndURL"




class Input():
    def __init__(self, text):
        self.rawtext = text
        self.commands = []
        com = TextCommand(text)
        self.commands.append(com)


class MUFilter():
    def __init__(self):
        self.type = "Generic"

    def run(self, inp):
        pass

class MUF_URL_Handler():
    def __init__(self):
        self.type = "URL Decoder"
        self.ur = re.compile(url.urlre)

    def run(self, inp):
        new = []
        for c in inp.commands:
            contin = True
            if(c.type == "Text"):
                contin = False
                beat = 0
                res = self.ur.split(c.text)
                for tt in res:
                    if(beat == 0):
                        ff = TextCommand(tt)
                        new.append(ff)
                        beat = 1
                    else:
                        ff = URLCommand()
                        ff.url = tt
                        new.append(ff)
                        ff = TextCommand(tt)
                        new.append(ff)
                        ff = URLEndCommand()
                        new.append(ff)
                        beat = 0
            if contin:
                new.append(c)
        inp.commands = new



class MUF_MXP_Send_Handler():
    def __init__(self):
        self.type = "MXP SEND Tag Decoder"

    def run(self, inp):
        new = []
        for c in inp.commands:
            contin = True
            if(c.type == "Tag"):
                if(c.tagtype.lower() == "send"):
                    ff = ContextCommand()
                    ff.tag = c
                    new.append(ff)

            if(c.type == "EndTag"):
                if(c.tagtype.lower() == "send"):
                    ff = ContextEndCommand()
                    new.append(ff)

            if contin:
                new.append(c)
        inp.commands = new

class MUF_ANSI(MUFilter):
    def __init__(self):
        self.type = "ANSI Decoder"
        self.simple = re.compile("\x1b\[([0-9;]+)m")

    def interpretANSI(self, ansi, stack):
        if(ansi >= 30 and ansi < 40):
            ff = FontCommand()
            ff.sub = "SimpleColor"
            ff.color = ansi - 30
            stack.append(ff)
        if(ansi == 1):
            ff = FontCommand()
            ff.sub = "Bold"
            stack.append(ff)
        if(ansi == 0):
            ## Normal is Default
            ff = FontCommand()
            stack.append(ff)

    def run(self, inp):
        new = []
        for c in inp.commands:
            contin = True
            if(c.type == "Text"):
                contin = False

                ## Try Simple
                res = self.simple.split(c.text)
                beat = 0
                for tt in res:
                    if(beat == 0):
                        ff = TextCommand(tt)
                        new.append(ff)
                        beat = 1
                    else:
                        ll = tt.split(';')
                        if(len(ll) == 1):
                            c1 = int(ll[0])
                            self.interpretANSI(c1,new)

                        if(len(ll) == 2):
                            c1 = int(ll[0])
                            c2 = int(ll[1])
                            self.interpretANSI(c1, new)
                            self.interpretANSI(c2, new)

                        if(len(ll) == 3):
                            ## RBG - DUMB STYLE - I hate you xterm
                            ## i.e. a 3-set is probably a 256 color, look at it as such
                            c1 = int(ll[0])
                            c2 = int(ll[1])
                            c3 = int(ll[2])
                            if(c1 == 38 and c2 == 5):
                                ff = FontCommand()
                                ff.sub = "SimpleColor"
                                ff.color = c3
                                new.append(ff)
                        beat = 0
            if(contin):
                new.append(c)
        inp.commands = new



class MUF_SimpleTag_Interpreter(MUFilter):
    def __init__(self):
        self.type = "HTML Tag Decoder"

    def run(self, inp):
        new = []
        for c in inp.commands:
            contin = True
            if(c.type == "Tag"):
                if(c.tagtype.lower() == "br"):
                    gg = NewLineCommand()
                    new.append(gg)
                    contin = False
                ## More tag types here
            if(contin):
                new.append(c)
        inp.commands = new



class MUF_Tag_Decoder(MUFilter):
    class thagHTMLParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.curtag = ""
            self.output = []

        def handle_starttag(self, tag, attrs):
            self.curtag = tag
            tt = TagCommand()
            tt.tagtype = tag
            for attr in attrs:
                k,v = attr
                tt.tagsettings[k]=v
            self.output.append(tt)

        def handle_endtag(self, tag):
            tt = EndTagCommand()
            tt.tagtype = tag
            self.output.append(tt)

        def handle_data(self, data):
            tt = TextCommand(data)
            self.output.append(tt)

        def handle_entityref(self, name):
            c = unichr(name2codepoint[name])
            tt = TextCommand(c)
            self.output.append(tt)

        def handle_charref(self, name):
            if name.startswith('x'):
                c = unichr(int(name[1:], 16))
            else:
                c = unichr(int(name))
            tt = TextCommand(c)
            self.output.append(tt)



    def __init__(self):
        self.type = "HTML Tag Decoder"

    def run(self, inp):
        new = []
        for t in inp.commands:
            hh = MUF_Tag_Decoder.thagHTMLParser()
            if(t.type == "Text"):
                hh.feed(t.text)
                ff = deepcopy(hh.output)
                for l in ff:
                    new.append(l)
            else:
                new.append(t)
        inp.commands = new






