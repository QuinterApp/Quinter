import application
import wx
import globals
from . import main, misc

class AccountsGui(wx.Dialog):
	def __init__(self):
		wx.Dialog.__init__(self, None, title="Accounts", size=(350,200))
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.list_label=wx.StaticText(self.panel, -1, label="&Accounts")
		self.list=wx.ListBox(self.panel, -1)
		self.main_box.Add(self.list, 0, wx.ALL, 10)
		self.list.SetFocus()
		self.list.Bind(wx.EVT_LISTBOX, self.on_list_change)
		self.add_items()
		self.load = wx.Button(self.panel, wx.ID_DEFAULT, "&Switch")
		self.load.SetDefault()
		self.load.Bind(wx.EVT_BUTTON, self.Load)
#		self.load.Enable(False)
		self.main_box.Add(self.load, 0, wx.ALL, 10)
		self.new = wx.Button(self.panel, wx.ID_DEFAULT, "&Add account")
		self.new.Bind(wx.EVT_BUTTON, self.New)
		self.main_box.Add(self.new, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()

	def add_items(self):
		index=0
		for i in globals.accounts:
			self.list.Insert(i.me.screen_name,self.list.GetCount())
			if i==globals.currentAccount:
				self.list.SetSelection(index)
			index+=1

	def on_list_change(self,event):
		pass

	def New(self, event):
		globals.add_session()
		globals.prefs.accounts+=1
		globals.currentAccount=globals.accounts[len(globals.accounts)-1]
		main.window.refreshTimelines()
		main.window.on_list_change(None)
		main.window.SetLabel(globals.currentAccount.me.screen_name+" - "+application.name+" "+application.version)
		self.Destroy()

	def Load(self, event):
		globals.currentAccount=globals.accounts[self.list.GetSelection()]
		main.window.refreshTimelines()
		main.window.list.SetSelection(globals.currentAccount.currentIndex)
		main.window.on_list_change(None)
		main.window.SetLabel(globals.currentAccount.me.screen_name+" - "+application.name+" "+application.version)
		self.Destroy()

	def OnClose(self, event):
		self.Destroy()
