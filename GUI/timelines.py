import application
import wx
import globals
from . import main, misc

class HiddenTimelinesGui(wx.Dialog):
	def __init__(self,account):
		self.account=account
		wx.Dialog.__init__(self, None, title="Hidden timelines", size=(350,200))
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.list_label=wx.StaticText(self.panel, -1, label="&Timelines")
		self.list=wx.ListBox(self.panel, -1)
		self.main_box.Add(self.list, 0, wx.ALL, 10)
		self.list.SetFocus()
		self.list.Bind(wx.EVT_LISTBOX, self.on_list_change)
		self.add_items()
		self.load = wx.Button(self.panel, wx.ID_DEFAULT, "&Unhide")
		self.load.SetDefault()
		self.load.Bind(wx.EVT_BUTTON, self.Load)
#		self.load.Enable(False)
		self.main_box.Add(self.load, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()

	def add_items(self):
		index=0
		for i in self.account.list_timelines(True):
			self.list.Insert(i.name,self.list.GetCount())
		self.list.SetSelection(0)

	def on_list_change(self,event):
		self.load.Enable(True)

	def Load(self, event):
		self.account.list_timelines(True)[self.list.GetSelection()].unhide_tl()
		self.list.Delete(self.list.GetSelection())

	def OnClose(self, event):
		self.Destroy()
