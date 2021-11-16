import globals
import wx
class ProfileGui(wx.Dialog):

	def __init__(self, account):
		self.account=account
		s=account.api.verify_credentials()
		wx.Dialog.__init__(self, None, title="Profile Editor", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.name_label = wx.StaticText(self.panel, -1, "Full Name")
		self.name = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.name, 0, wx.ALL, 10)
		self.name.SetFocus()
		if s.name!=None:
			self.name.SetValue(s.name)
		self.url_label = wx.StaticText(self.panel, -1, "URL")
		self.url = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.url, 0, wx.ALL, 10)
		if s.url!=None:
			self.url.SetValue(s.url)
		self.location_label = wx.StaticText(self.panel, -1, "Location")
		self.location = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.location, 0, wx.ALL, 10)
		if s.location!=None:
			self.location.SetValue(s.location)
		self.description_label = wx.StaticText(self.panel, -1, "Description")
		self.description = wx.TextCtrl(self.panel, -1, "")
		self.main_box.Add(self.description, 0, wx.ALL, 10)
		if s.description!=None:
			self.description.SetValue(s.description)
		self.update = wx.Button(self.panel, wx.ID_DEFAULT, "&Update")
		self.update.SetDefault()
		self.update.Bind(wx.EVT_BUTTON, self.Update)
		self.main_box.Add(self.update, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()
	def Update(self, event):
		self.account.UpdateProfile(self.name.GetValue(),self.url.GetValue(),self.location.GetValue(),self.description.GetValue())
		self.Destroy()
	def OnClose(self, event):
		self.Destroy()