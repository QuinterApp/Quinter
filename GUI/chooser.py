from tweepy import TweepError
import globals, sound, timeline, utils
import time
import wx
import webbrowser
import os
import platform
from . import lists, main, misc, view

class ChooseGui(wx.Dialog):
	def __init__(self,account,title="Choose",text="Choose a thing",list=[],type=""):
		self.account=account
		self.type=type
		self.returnvalue=""
		wx.Dialog.__init__(self, None, title=title, size=(350,200))
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.chooser_label=wx.StaticText(self.panel, -1, title)
		self.chooser=wx.ComboBox(self.panel,-1,size=(800,600))
		self.main_box.Add(self.chooser, 0, wx.ALL, 10)
		self.chooser.SetFocus()
		for i in list:
			self.chooser.Insert(i,self.chooser.GetCount())
		self.chooser.SetSelection(0)
		self.ok = wx.Button(self.panel, wx.ID_DEFAULT, "OK")
		self.ok.SetDefault()
		self.ok.Bind(wx.EVT_BUTTON, self.OK)
		self.main_box.Add(self.ok, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()

	def OK(self, event):
		self.returnvalue=self.chooser.GetValue().strip("@")
		self.Destroy()
		if self.type=="profile":
			user=view.UserViewGui(self.account,[utils.lookup_user_name(self.account,self.returnvalue)],self.returnvalue+"'s profile")
			user.Show()
		if self.type=="url":
			if platform.system()!="Darwin":
				webbrowser.open(self.returnvalue)
			else:
				os.system("open "+self.returnvalue)
		if self.type=="list":
			l=lists.ListsGui(self.account,utils.lookup_user_name(self.account,self.returnvalue))
			l.Show()
		if self.type=="listr":
			l=lists.ListsGui(self.account,utils.lookup_user_name(self.account,self.returnvalue),False)
			l.Show()
		if self.type=="follow":
			misc.follow_user(self.account,self.returnvalue)
		if self.type=="unfollow":
			misc.unfollow_user(self.account,self.returnvalue)
		if self.type=="block":
			user=self.account.block(self.returnvalue)
		if self.type=="unblock":
			user=self.account.unblock(self.returnvalue)
		if self.type=="mute":
			try:
				user=self.account.api.create_mute(self.returnvalue)
			except TweepError as e:
				utils.handle_error(e,"Mute")
		if self.type=="unmute":
			try:
				user=self.account.api.destroy_mute(self.returnvalue)
			except TweepError as e:
				utils.handle_error(e,"Unmute")
		if self.type=="usertimeline":
			misc.user_timeline_user(self.account,self.returnvalue)

	def OnClose(self, event):
		self.Destroy()

def chooser(account,title="choose",text="Choose some stuff",list=[],type=""):
	chooser=ChooseGui(account,title,text,list,type)
	chooser.Show()
	return chooser.returnvalue