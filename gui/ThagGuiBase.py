# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.richtext

###########################################################################
## Class ThagMainFrameBase
###########################################################################

class ThagMainFrameBase ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Thagoras", pos = wx.DefaultPosition, size = wx.Size( 356,82 ), style = wx.DEFAULT_FRAME_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.thag_main_frame_menubar = wx.MenuBar( 0 )
		self.m_menu3 = wx.Menu()
		self.m_menuItem3 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"Load", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu3.AppendItem( self.m_menuItem3 )
		
		self.m_menuItem4 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu3.AppendItem( self.m_menuItem4 )
		
		self.thag_main_frame_menubar.Append( self.m_menu3, u"File" ) 
		
		self.connect_menu = wx.Menu()
		self.thag_main_frame_menubar.Append( self.connect_menu, u"Connect" ) 
		
		self.edit_menu = wx.Menu()
		self.m_menuItem2 = wx.MenuItem( self.edit_menu, wx.ID_ANY, u"Add World...", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit_menu.AppendItem( self.m_menuItem2 )
		
		self.edit_menu.AppendSeparator()
		
		self.thag_main_frame_menubar.Append( self.edit_menu, u"Edit" ) 
		
		self.SetMenuBar( self.thag_main_frame_menubar )
		
		gSizer1 = wx.GridSizer( 1, 4, 1, 1 )
		
		
		self.SetSizer( gSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.DoLoad, id = self.m_menuItem3.GetId() )
		self.Bind( wx.EVT_MENU, self.DoSave, id = self.m_menuItem4.GetId() )
		self.Bind( wx.EVT_MENU, self.OnNewWorld, id = self.m_menuItem2.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def DoLoad( self, event ):
		event.Skip()
	
	def DoSave( self, event ):
		event.Skip()
	
	def OnNewWorld( self, event ):
		event.Skip()
	

###########################################################################
## Class ThagWorldFrameBase
###########################################################################

class ThagWorldFrameBase ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"World", pos = wx.DefaultPosition, size = wx.Size( 977,549 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.thag_world_frame_menubar = wx.MenuBar( 0 )
		self.SetMenuBar( self.thag_world_frame_menubar )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.text_output = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		bSizer1.Add( self.text_output, 100, wx.EXPAND |wx.ALL, 1 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.output = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.output.SetMaxLength( 0 ) 
		self.output.SetMinSize( wx.Size( -1,20 ) )
		self.output.SetMaxSize( wx.Size( -1,27 ) )
		
		bSizer2.Add( self.output, 8, wx.EXPAND, 0 )
		
		self.button_1 = wx.Button( self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.button_1.SetDefault() 
		bSizer2.Add( self.button_1, 1, 0, 0 )
		
		
		bSizer1.Add( bSizer2, 1, wx.ALIGN_BOTTOM|wx.EXPAND|wx.FIXED_MINSIZE|wx.TOP, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.output.Bind( wx.EVT_TEXT_ENTER, self.OnSend )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnSend( self, event ):
		event.Skip()
	

###########################################################################
## Class ThagWorldDialogBase
###########################################################################

class ThagWorldDialogBase ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"World Info:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer4.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.world_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.world_name, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Address:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.world_address = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.world_address, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.world_port = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.world_port, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Choose Font:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.world_font = wx.FontPickerCtrl( self, wx.ID_ANY, wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Lucida Console" ), wx.DefaultPosition, wx.DefaultSize, wx.FNTP_DEFAULT_STYLE )
		self.world_font.SetMaxPointSize( 100 ) 
		fgSizer1.Add( self.world_font, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer4.Add( fgSizer1, 0, wx.EXPAND, 2 )
		
		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Characters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer4.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.char_list = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer5.Add( self.char_list, 0, wx.ALL|wx.EXPAND, 5 )
		
		fgSizer2 = wx.FlexGridSizer( 0, 4, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		
		bSizer5.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"User:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer6.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.char_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.char_name, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"Pass:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		bSizer6.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.char_pass = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.char_pass, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button2 = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button2, 0, wx.ALL, 5 )
		
		self.m_button3 = wx.Button( self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button3, 0, wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button4, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		bSizer4.Add( bSizer5, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer4.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
		
		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();
		m_sdbSizer1.SetMinSize( wx.Size( -1,27 ) ) 
		
		bSizer4.Add( m_sdbSizer1, 0, wx.EXPAND|wx.FIXED_MINSIZE, 1 )
		
		
		bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		bSizer3.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

