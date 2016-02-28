
import mufilter
import re, json

class Character():
    def __init__(self, world, user="", password=""):
        self.world = world
        self.user = user
        self.password = password
        self.setupVars()

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
        return self.gui.getWidth()

    def setupVars(self):
        self.gui = None
        self.telnet = None
        self.outputs = {}
        self.inputs = {}
        self.filters = []
        self.setDefaultFilters()
        self.oobre = re.compile(r'(([0-9a-zA-Z_\'\"\- ]+\.)*[0-9a-zA-Z_\'\"\-]+) ({.*?})')

    def setDefaultFilters(self):
        self.filters = []


        ff = mufilter.MUF_Tag_Fixer()
        self.filters.append(ff)

        ff = mufilter.MUF_Tag_Decoder()
        self.filters.append(ff)

        ff = mufilter.MUF_SimpleTag_Interpreter()
        self.filters.append(ff)

        ff = mufilter.MUF_ANSI()
        self.filters.append(ff)

        ff = mufilter.MUF_MXP_Send_Handler()
        self.filters.append(ff)

        ff = mufilter.MUF_Text_Combiner()
        self.filters.append(ff)

        ff = mufilter.MUF_URL_Handler()
        self.filters.append(ff)

    def send(self, line):
        self.telnet.write(str(line))

    def recv(self, line):
        ## Run Filters
        ii = mufilter.Input(line)
        for f in self.filters:
            f.run(ii)

        self.gui.writeGUI(ii)

    def __getstate__(self):
        odict = self.__dict__.copy()
        odict.pop('world')
        odict.pop('gui')
        odict.pop('telnet')
        return odict

    def __setstate__(self, dd):
        self.setupVars()
        self.__dict__.update(dd)
        self.setDefaultFilters()

class World():
    def __init__(self,name="",address="",port=0):
        self.address = address
        self.port = port
        self.name = name
        self.ssl = False
        self.setupVars()


    def setupVars(self):
        self.chars = []
        self.gui = None
        self.telnet = None
        self.ssl = False
        self.outputs = {}
        self.inputs = {}
        self.filters = {}
        self.profiles = {}
        self.lines = 500

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
        return odict

    def __setstate__(self, dd):
        self.setupVars()
        self.__dict__.update(dd)
        self.setCharWorld()


        
