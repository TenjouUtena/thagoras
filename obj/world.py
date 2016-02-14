import util.logger as logger
import mufilter

class Character():
    def __init__(self, world, user="", password=""):
        self.world = world
        self.user = user
        self.password = password
        self.setupVars()

    def setupVars(self):
        self.gui = None
        self.telnet = None
        self.outputs = {}
        self.inputs = {}
        self.filters = []
        self.setDefaultFilters()

    def setDefaultFilters(self):
        self.filters = []
        ff = mufilter.MUF_Tag_Decoder()
        self.filters.append(ff)

        ff = mufilter.MUF_SimpleTag_Interpreter()
        self.filters.append(ff)

        ff = mufilter.MUF_ANSI()
        self.filters.append(ff)

        ff = mufilter.MUF_MXP_Send_Handler()
        self.filters.append(ff)

        ff = mufilter.MUF_URL_Handler()
        self.filters.append(ff)

    def send(self, line):
        self.telnet.write(str(line))

    def recv(self, line):
        logger.log(line)

        ### Setup Pueblo
        res = line.find("This world is Pueblo 1.10 Enhanced.")
        if(res != -1):
            self.telnet.write("PUEBLOCLIENT 1.10\n")

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
        self.setupVars()

    def setupVars(self):
        self.chars = []
        self.gui = None
        self.telnet = None
        self.outputs = {}
        self.inputs = {}
        self.filters = {}

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


        
