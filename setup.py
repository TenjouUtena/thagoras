from distutils.core import setup
import py2exe

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.0.1.0"
    processorArchitecture="x86"
    name="Thagoras"
    type="win32"
/>
<description>Thagoras</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="x86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
    <dependency>
        <dependentAssembly>
            <assemblyIdentity
                type="win32"
                name="Microsoft.VC90.CRT"
                version="9.0.30729.1"
                processorArchitecture="x86"
                publicKeyToken="1fc8b3b9a1e18e3b"
                />
        </dependentAssembly>
    </dependency>
</assembly>
"""

setup(windows=[{
    'script':'thagoras.py',
    "other_resources": [(24,1,manifest)]
    }], 
    zipfile = None,
    options = 
    {"py2exe": {

    "dll_excludes": ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                     'tk84.dll',"MSVCP90.dll", "mswsock.dll", "MSWSOCK.dll"],
    "excludes" : ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter'],
    "bundle_files": 2,
    "includes": ["cffi"]
    }})