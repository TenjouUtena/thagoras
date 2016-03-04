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
		
		self.m_menu3.AppendSeparator()
		
		self.m_menuItem5 = wx.MenuItem( self.m_menu3, wx.ID_ANY, u"E&xit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu3.AppendItem( self.m_menuItem5 )
		
		self.thag_main_frame_menubar.Append( self.m_menu3, u"File" ) 
		
		self.connect_menu = wx.Menu()
		self.thag_main_frame_menubar.Append( self.connect_menu, u"Connect" ) 
		
		self.edit_menu = wx.Menu()
		self.m_menuItem2 = wx.MenuItem( self.edit_menu, wx.ID_ANY, u"Add World...", wx.EmptyString, wx.ITEM_NORMAL )
		self.edit_menu.AppendItem( self.m_menuItem2 )
		
		self.edit_menu.AppendSeparator()
		
		self.thag_main_frame_menubar.Append( self.edit_menu, u"Worlds" ) 
		
		self.m_menu4 = wx.Menu()
		self.m_menuItem41 = wx.MenuItem( self.m_menu4, wx.ID_ANY, u"Settings...", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu4.AppendItem( self.m_menuItem41 )
		
		self.thag_main_frame_menubar.Append( self.m_menu4, u"Options" ) 
		
		self.SetMenuBar( self.thag_main_frame_menubar )
		
		gSizer1 = wx.GridSizer( 1, 4, 1, 1 )
		
		
		self.SetSizer( gSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.Bind( wx.EVT_MENU, self.DoLoad, id = self.m_menuItem3.GetId() )
		self.Bind( wx.EVT_MENU, self.DoSave, id = self.m_menuItem4.GetId() )
		self.Bind( wx.EVT_MENU, self.OnExitCommand, id = self.m_menuItem5.GetId() )
		self.Bind( wx.EVT_MENU, self.OnNewWorld, id = self.m_menuItem2.GetId() )
		self.Bind( wx.EVT_MENU, self.OnSettings, id = self.m_menuItem41.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()
	
	def DoLoad( self, event ):
		event.Skip()
	
	def DoSave( self, event ):
		event.Skip()
	
	def OnExitCommand( self, event ):
		event.Skip()
	
	def OnNewWorld( self, event ):
		event.Skip()
	
	def OnSettings( self, event ):
		event.Skip()
	

###########################################################################
## Class ThagMainDialogBase
###########################################################################

class ThagMainDialogBase ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer13 = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Save on Close?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		fgSizer4.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.save_on_close = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.save_on_close, 0, wx.ALL, 5 )
		
		
		bSizer13.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		m_sdbSizer3 = wx.StdDialogButtonSizer()
		self.m_sdbSizer3OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer3.AddButton( self.m_sdbSizer3OK )
		self.m_sdbSizer3Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer3.AddButton( self.m_sdbSizer3Cancel )
		m_sdbSizer3.Realize();
		
		bSizer13.Add( m_sdbSizer3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer13 )
		self.Layout()
		bSizer13.Fit( self )
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

###########################################################################
## Class ThagWorldFrameBase
###########################################################################

class ThagWorldFrameBase ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 977,549 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.thag_world_frame_menubar = wx.MenuBar( 0 )
		self.SetMenuBar( self.thag_world_frame_menubar )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.text_output = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.HSCROLL|wx.NO_BORDER|wx.VSCROLL )
		self.text_output.SetForegroundColour( wx.Colour( 192, 192, 192 ) )
		self.text_output.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
		
		bSizer1.Add( self.text_output, 1, wx.EXPAND |wx.ALL, 1 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.output = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.output.SetMaxLength( 0 ) 
		self.output.SetForegroundColour( wx.Colour( 192, 192, 192 ) )
		self.output.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
		self.output.SetMinSize( wx.Size( -1,20 ) )
		self.output.SetMaxSize( wx.Size( -1,27 ) )
		
		bSizer2.Add( self.output, 8, wx.EXPAND, 0 )
		
		self.button_1 = wx.Button( self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.button_1.SetDefault() 
		bSizer2.Add( self.button_1, 1, 0, 0 )
		
		
		bSizer1.Add( bSizer2, 0, wx.ALIGN_BOTTOM|wx.EXPAND|wx.FIXED_MINSIZE|wx.TOP, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.Bind( wx.EVT_MOUSEWHEEL, self.OnScroll )
		self.text_output.Bind( wx.EVT_SET_FOCUS, self.OnOutFocus )
		self.text_output.Bind( wx.EVT_SIZE, self.OnSize )
		self.text_output.Bind( wx.EVT_TEXT_URL, self.OnURL )
		self.output.Bind( wx.EVT_KEY_DOWN, self.OnKeyDown )
		self.output.Bind( wx.EVT_TEXT_ENTER, self.OnSend )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()
	
	def OnScroll( self, event ):
		event.Skip()
	
	def OnOutFocus( self, event ):
		event.Skip()
	
	def OnSize( self, event ):
		event.Skip()
	
	def OnURL( self, event ):
		event.Skip()
	
	def OnKeyDown( self, event ):
		event.Skip()
	
	def OnSend( self, event ):
		event.Skip()
	

###########################################################################
## Class ThagWorldChannelFrameBase
###########################################################################

class ThagWorldChannelFrameBase ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 977,549 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.thag_world_frame_menubar = wx.MenuBar( 0 )
		self.SetMenuBar( self.thag_world_frame_menubar )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.chan_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		bSizer1.Add( self.chan_notebook, 1, wx.EXPAND |wx.ALL, 0 )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		char_choiceChoices = []
		self.char_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, char_choiceChoices, 0 )
		self.char_choice.SetSelection( 0 )
		bSizer2.Add( self.char_choice, 0, wx.ALL, 0 )
		
		self.output = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.output.SetMaxLength( 0 ) 
		self.output.SetForegroundColour( wx.Colour( 192, 192, 192 ) )
		self.output.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
		self.output.SetMinSize( wx.Size( -1,20 ) )
		self.output.SetMaxSize( wx.Size( -1,27 ) )
		
		bSizer2.Add( self.output, 8, wx.EXPAND, 0 )
		
		self.button_1 = wx.Button( self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.button_1.SetDefault() 
		bSizer2.Add( self.button_1, 1, 0, 0 )
		
		
		bSizer1.Add( bSizer2, 0, wx.ALIGN_BOTTOM|wx.EXPAND|wx.FIXED_MINSIZE|wx.TOP, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.Bind( wx.EVT_MOUSEWHEEL, self.OnScroll )
		self.output.Bind( wx.EVT_KEY_DOWN, self.OnKeyDown )
		self.output.Bind( wx.EVT_TEXT_ENTER, self.OnSend )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()
	
	def OnScroll( self, event ):
		event.Skip()
	
	def OnKeyDown( self, event ):
		event.Skip()
	
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
		bSizer4.Add( self.m_staticText8, 0, wx.ALL, 2 )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Name:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 1 )
		
		self.world_name = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.world_name, 0, wx.ALL|wx.EXPAND, 1 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Address:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer1.Add( self.m_staticText2, 0, wx.ALL, 1 )
		
		self.world_address = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.world_address, 0, wx.ALL|wx.EXPAND, 1 )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Port:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		fgSizer1.Add( self.m_staticText3, 0, wx.ALL, 1 )
		
		self.world_port = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.world_port, 0, wx.ALL|wx.EXPAND, 1 )
		
		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"SSL?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		fgSizer1.Add( self.m_staticText9, 0, wx.ALL, 1 )
		
		self.world_ssl = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.world_ssl, 0, wx.ALL, 1 )
		
		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Scrollback Lines", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		fgSizer1.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.lines_scrollback = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.lines_scrollback, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Choose Font:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		fgSizer1.Add( self.m_staticText4, 0, wx.ALL, 1 )
		
		self.world_font = wx.FontPickerCtrl( self, wx.ID_ANY, wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, "Lucida Console" ), wx.DefaultPosition, wx.DefaultSize, wx.FNTP_DEFAULT_STYLE )
		self.world_font.SetMaxPointSize( 100 ) 
		self.world_font.Enable( False )
		
		fgSizer1.Add( self.world_font, 0, wx.ALL|wx.EXPAND, 1 )
		
		
		bSizer4.Add( fgSizer1, 0, wx.EXPAND, 2 )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.STATIC_BORDER|wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText7 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Characters:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer5.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.char_list = wx.ListCtrl( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SINGLE_SEL )
		bSizer5.Add( self.char_list, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText5 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"User:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer6.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.char_name = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.char_name, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"Pass:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		bSizer6.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.char_pass = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.char_pass, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button2 = wx.Button( self.m_panel1, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button2, 0, wx.ALL, 5 )
		
		self.m_button3 = wx.Button( self.m_panel1, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button3, 0, wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self.m_panel1, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_button4, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer5 )
		self.m_panel1.Layout()
		bSizer5.Fit( self.m_panel1 )
		bSizer4.Add( self.m_panel1, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.delete_button = wx.Button( self, wx.ID_ANY, u"Delete World", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.delete_button, 0, wx.ALL, 5 )
		
		
		bSizer4.Add( bSizer18, 0, wx.EXPAND, 5 )
		
		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		self.m_sdbSizer1Cancel = wx.Button( self, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();
		m_sdbSizer1.SetMinSize( wx.Size( -1,27 ) ) 
		
		bSizer4.Add( m_sdbSizer1, 0, wx.EXPAND|wx.FIXED_MINSIZE, 1 )
		
		
		bSizer3.Add( bSizer4, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		bSizer3.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_INIT_DIALOG, self.OnInit )
		self.char_list.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnCharSelect )
		self.m_button2.Bind( wx.EVT_BUTTON, self.OnCharAdd )
		self.m_button3.Bind( wx.EVT_BUTTON, self.OnCharSave )
		self.m_button4.Bind( wx.EVT_BUTTON, self.OnCharRemove )
		self.delete_button.Bind( wx.EVT_BUTTON, self.OnDeleteWorld )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnInit( self, event ):
		event.Skip()
	
	def OnCharSelect( self, event ):
		event.Skip()
	
	def OnCharAdd( self, event ):
		event.Skip()
	
	def OnCharSave( self, event ):
		event.Skip()
	
	def OnCharRemove( self, event ):
		event.Skip()
	
	def OnDeleteWorld( self, event ):
		event.Skip()
	

###########################################################################
## Class ThagPersonInfoBase
###########################################################################

class ThagPersonInfoBase ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 959,662 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		person_selectorChoices = []
		self.person_selector = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, person_selectorChoices, wx.CB_DROPDOWN|wx.CB_SORT )
		bSizer8.Add( self.person_selector, 0, wx.ALL, 5 )
		
		self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		bSizer8.Add( self.notebook, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer8 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.person_selector.Bind( wx.EVT_COMBOBOX, self.OnSelectPerson )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()
	
	def OnSelectPerson( self, event ):
		event.Skip()
	

###########################################################################
## Class ThagPersonInfoPaneBase
###########################################################################

class ThagPersonInfoPaneBase ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.general_info = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_MULTILINE|wx.TE_WORDWRAP )
		self.general_info.SetMinSize( wx.Size( 250,-1 ) )
		
		bSizer11.Add( self.general_info, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		picSizer = wx.BoxSizer( wx.VERTICAL )
		
		self.person_picture = wx.StaticBitmap( self.m_scrolledWindow1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		picSizer.Add( self.person_picture, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_scrolledWindow1.SetSizer( picSizer )
		self.m_scrolledWindow1.Layout()
		picSizer.Fit( self.m_scrolledWindow1 )
		bSizer11.Add( self.m_scrolledWindow1, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer10.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		self.info_list = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT )
		bSizer10.Add( self.info_list, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer10 )
		self.Layout()
	
	def __del__( self ):
		pass
	

###########################################################################
## Class ThagOutputPanelBase
###########################################################################

class ThagOutputPanelBase ( wx.Panel ):
	
	def __init__( self, parent ):
		wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		
		bSizer23 = wx.BoxSizer( wx.VERTICAL )
		
		self.text_output = wx.richtext.RichTextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER|wx.WANTS_CHARS )
		self.text_output.SetForegroundColour( wx.Colour( 192, 192, 192 ) )
		self.text_output.SetBackgroundColour( wx.Colour( 0, 0, 0 ) )
		
		bSizer23.Add( self.text_output, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer23 )
		self.Layout()
		
		# Connect Events
		self.text_output.Bind( wx.EVT_SET_FOCUS, self.OnOutFocus )
		self.text_output.Bind( wx.EVT_TEXT_URL, self.OnURL )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnOutFocus( self, event ):
		event.Skip()
	
	def OnURL( self, event ):
		event.Skip()
	

