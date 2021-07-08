import wx
import globals
from . import misc

class SearchGui(wx.Dialog):
	def __init__(self,account, type="search"):
		self.account=account
		self.type=type
		wx.Dialog.__init__(self, None, title="Search", size=(350,200))
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "Search text")
		self.text = wx.TextCtrl(self.panel, -1, "",style=wx.TE_PROCESS_ENTER|wx.TE_DONTWRAP)
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.text.SetFocus()
		self.text.Bind(wx.EVT_TEXT_ENTER, self.Search)
		self.search = wx.Button(self.panel, wx.ID_DEFAULT, "&Search")
		self.search.SetDefault()
		self.search.Bind(wx.EVT_BUTTON, self.Search)
		self.main_box.Add(self.search, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()

	def Search(self, event):
		if self.type=="search":
			misc.search(self.account,self.text.GetValue())
		else:
			misc.user_search(self.account,self.text.GetValue())
		self.Destroy()

	def OnClose(self, event):
		self.Destroy()
