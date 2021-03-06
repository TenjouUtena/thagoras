from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from copy import deepcopy

import re
import util.url as url

class Command(object):
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




class Input(object):
    def __init__(self, text, output="main", outputlevel='char'):
        self.rawtext = text
        self.resultanttext = text
        self.commands = []
        self.output = output
        self.suboutput = None
        self.outputlevel = outputlevel
        com = TextCommand(text)
        self.commands.append(com)


class MUFilter(object):
    def __init__(self):
        self.type = "Generic"

    def run(self, inp):
        pass

class MUF_Pass_To_Sub(MUFilter):
    def __init__(self, pattern, dest, outputlevel):
        self.type = "Pass to Suboutput Window"
        
        ## If text matches pattern, output will be redirected to the 
        ## output described in dest/outputlevel
        ## Input.suboutput will match the first group in the regex
        self.pattern = re.compile(pattern)
        self.dest = dest
        self.outputlevel = outputlevel
        self.sub = ""

    def run(self, inp):
        mm = self.pattern.match(inp.resultanttext)
        if(mm):
            inp.output = self.dest
            inp.suboutput = mm.group(1)
            inp.outputlevel = self.outputlevel



class MUF_Calculate_Text(MUFilter):
    def __init__(self):
        self.type = "Calculate resultanttext field"

    def run(self, inp):
        inp.resultanttext = ""
        for c in inp.commands:
            if(c.type == "Text"):
                inp.resultanttext += c.text

class MUF_Add_Newline(MUFilter):
    def __init__(self):
        self.type = "Add a newline"

    def run(self, inp):
        nl = NewLineCommand()
        inp.commands.append(nl)

## Repair tags that dont' conform to XML spec
class MUF_Tag_Fixer(MUFilter):
    def __init__(self):
        self.type = "Tag Fixer"
        self.ur = re.compile(r'<([a-zA-Z]+)\s+(\".*?\")(.*?)>')

    def run(self, inp):
        for c in inp.commands:
            if c.type == "Text":
                newt = ""
                c.text = self.ur.sub(r"<\1 href=\2 \3>",c.text)

class MUF_Text_Combiner(MUFilter):
    def __init__(self):
        self.type = "URL Decoder"

    def run(self, inp):
        new = []
        text = ""
        for c in inp.commands:
            contin = True
            if c.type == "Text":
                text += c.text
                contin = False
            else:
                if text != "":
                    ff = TextCommand(text)
                    new.append(ff)
                    text = ""
            if contin:
                new.append(c)
        if text != "":
            ff = TextCommand(text)
            new.append(ff)
        inp.commands = new

class MUF_URL_Handler(MUFilter):
    def __init__(self):
        self.type = "URL Decoder"
        self.ur = re.compile(url.urlre)

    def run(self, inp):
        new = []
        for c in inp.commands:
            contin = True
            if c.type == "Text":
                contin = False
                beat = 0
                res = self.ur.split(c.text)
                for tt in res:
                    if beat == 0:
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



class MUF_MXP_Send_Handler(MUFilter):
    def __init__(self):
        self.type = "MXP SEND Tag Decoder"

    def run(self, inp):
        new = []
        for c in inp.commands:
            contin = True
            if c.type == "Tag":
                if c.tagtype.lower() == "send":
                    ff = ContextCommand()
                    ff.tag = c
                    new.append(ff)

            if c.type == "EndTag":
                if c.tagtype.lower() == "send":
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






