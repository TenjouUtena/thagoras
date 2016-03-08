
import mufilter
import re, json

import gui

class NoSuchOutputException(Exception):
    pass

class ParseObject(object):
    # TODO:  Clean up this dirty inheritance bullshit.
    def __init__(self):
        self.telnet = None

    def dispatch(self, inp):

        # This probably isn't the best place for this code
        # But literally nowhere makes any logical sense
        if(not self.outputs.has_key(inp.output)):
            if(not self.outputtypes.has_key(inp.output)):
                raise NoSuchOutputException(inp.output)
            self.outputs[inp.output] = self.outputtypes[inp.output](self.mainframe, world=self)
            self.outputs[inp.output].SetTitle(self.name + ' - ' + inp.output)
            self.outputs[inp.output].Show()

        self.outputs[inp.output].writeTo(inp)

    def connected(self, telobj):
        self.telnet = telobj

    def disconnected(self):
        self.telnet = None

    @property
    def lines(self):
        return self._lines

class Character(ParseObject):
    def __init__(self, world, user="", password=""):
        ParseObject.__init__(self)
        self.world = world
        self.user = user
        self.password = password
        self.setupVars()
        self.mainframe = None

    def connected(self, telobj):
        ParseObject.connected(self, telobj)
        self.world.connected(telobj)

    def disconnected(self):
        ParseObject.disconnected(self)
        self.world.disconnected()

    @property
    def lines(self):
        return self.world._lines

    def setFrame(self, gui):
        self.gui = gui
        self.outputs['main'] = gui

    def oob(self, info):
        res = self.oobre.match(info)
        if(res):
            command = res.group(1)
            comlist = command.split('.')

            if(comlist[0].lower() == 'info'):
                ## We have an info message
                if(not self.world.profiles.has_key(comlist[1])):
                    self.world.profiles[comlist[1]] = {}
                self.world.profiles[comlist[1]][comlist[2]] = json.loads(res.group(3))

    def getWidth(self):
        return self.outputs['main'].getWidth()

    def setupVars(self):
        # TODO: Fix this
        self.gui = None
        self.telnet = None
        self.outputs = {}
        self.inputs = {}
        self.filters = {}
        self.outputtypes = {}
        self.setDefaultFilters()
        self.oobre = re.compile(r'(([0-9a-zA-Z_\'\"\- ]+\.)*[0-9a-zA-Z_\'\"\-]+) ({.*?})')
        self.mxp = 'mxp'
        self.notmxp = 'notmap'
        self.mxp = False
        self.mainframe = None

    def setDefaultFilters(self):
        self.filters = {}

        ## Set MXp filters
        self.filters['mxp'] = []

        ff = mufilter.MUF_Tag_Fixer()
        self.filters['mxp'].append(ff)

        ff = mufilter.MUF_Tag_Decoder()
        self.filters['mxp'].append(ff)

        ff = mufilter.MUF_SimpleTag_Interpreter()
        self.filters['mxp'].append(ff)

        ff = mufilter.MUF_ANSI()
        self.filters['mxp'].append(ff)

        ff = mufilter.MUF_MXP_Send_Handler()
        self.filters['mxp'].append(ff)

        ff = mufilter.MUF_Text_Combiner()
        self.filters['mxp'].append(ff)

        ff = mufilter.MUF_URL_Handler()
        self.filters['mxp'].append(ff)

        ff = mufilter.MUF_Calculate_Text()
        self.filters['mxp'].append(ff)

        ff = mufilter.MUF_Pass_To_Sub(r'^<(.*?)>.*', 'channel', 'world')
        self.filters['mxp'].append(ff)

        ## Set non-MXP Filters
        self.filters['notmxp'] = []

        ff = mufilter.MUF_ANSI()
        self.filters['notmxp'].append(ff)

        ff = mufilter.MUF_Text_Combiner()
        self.filters['notmxp'].append(ff)

        ff = mufilter.MUF_URL_Handler()
        self.filters['notmxp'].append(ff)

        ff = mufilter.MUF_Add_Newline()
        self.filters['notmxp'].append(ff)



    def send(self, line):
        self.telnet.write(str(line))

    def recv(self, line):
        ## Run Filters
        ilist = [mufilter.Input(line)]

        if(self.mxp):
            fil = 'mxp'
        else:
            fil = 'notmxp'


        ibase = ilist[0]
        for f in self.filters[fil]:
            f.run(ibase)

        for ii in ilist:
            if(ii.outputlevel == 'char'):
                self.dispatch(ii)
            if(ii.outputlevel == 'world'):
                self.world.dispatch(ii)



    def __getstate__(self):
        odict = self.__dict__.copy()
        odict.pop('world')
        odict.pop('gui')
        odict.pop('telnet')
        odict.pop('outputs')
        odict.pop('mainframe')
        return odict

    def __setstate__(self, dd):
        self.setupVars()
        self.__dict__.update(dd)
        self.setDefaultFilters()


class World(ParseObject):
    def __init__(self,name="",address="",port=0):
        ParseObject.__init__(self)
        self.address = address
        self.port = port
        self.name = name
        self.ssl = False
        self.setupVars()
        self.mainframe = None

    def connected(self, telobj):
        if 'channel' in self.outputs:
            self.outputs['channel'].buildChars()

    def disconnected(self):
        if 'channel' in self.outputs:
            if self.outputs['channel']:
                self.outputs['channel'].buildChars()

    def setupVars(self):
        self.chars = []
        self.gui = None
        self.telnet = None
        self.ssl = False
        self.outputs = {}
        self.inputs = {}
        self.filters = {}
        self.profiles = {}
        self.outputtypes = {}
        self._lines = 500
        self.outputtypes['channel'] = gui.ThagChannelFrame

    def send(self, line):
        self.telnet.write(str(line))

    def setCharWorld(self):
        for c in self.chars:
            c.world = self

    ### Pickle Stuff
    def __getstate__(self):
        odict = self.__dict__.copy()
        odict.pop('gui')
        odict.pop('telnet')
        odict.pop('outputs')
        odict.pop('mainframe')
        return odict

    def __setstate__(self, dd):
        self.setupVars()
        self.__dict__.update(dd)
        self.setCharWorld()

    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, ll):
        self._lines = ll

        
