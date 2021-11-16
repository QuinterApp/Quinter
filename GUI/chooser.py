from tweepy import TweepyException
import globals, sound, timeline, utils
import time
import wx
import webbrowser
import os
import platform
from . import lists, main, misc, view

class ChooseGui(wx.Dialog):
	
	#constants for the types we might need to handle
	TYPE_BLOCK="block"
	TYPE_FOLLOW="follow"
	TYPE_LIST = "list"
	TYPE_LIST_R="listr"
	TYPE_MUTE="mute"
	TYPE_PROFILE = "profile"
	TYPE_UNBLOCK="unblock"
	TYPE_UNFOLLOW="unfollow"
	TYPE_UNMUTE="unmute"
	TYPE_URL="url"
	TYPE_USER_TIMELINE="userTimeline"

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
		if self.type==self.TYPE_PROFILE:
			user=view.UserViewGui(self.account,[utils.lookup_user_name(self.account,self.returnvalue)],self.returnvalue+"'s profile")
			user.Show()
		elif self.type==self.TYPE_URL:
			utils.openURL(self.returnvalue)
		elif self.type==self.TYPE_LIST:
			l=lists.ListsGui(self.account,utils.lookup_user_name(self.account,self.returnvalue))
			l.Show()
		elif self.type==self.TYPE_LIST_R:
			l=lists.ListsGui(self.account,utils.lookup_user_name(self.account,self.returnvalue),False)
			l.Show()
		elif self.type==self.TYPE_FOLLOW:
			misc.follow_user(self.account,self.returnvalue)
		elif self.type==self.TYPE_UNFOLLOW:
			misc.unfollow_user(self.account,self.returnvalue)
		elif self.type==self.TYPE_BLOCK:
			user=self.account.block(self.returnvalue)
		elif self.type==self.TYPE_UNBLOCK:
			user=self.account.unblock(self.returnvalue)
		elif self.type==self.TYPE_MUTE:
			try:
				user=self.account.api.create_mute(screen_name=self.returnvalue)
			except TweepyException as e:
				utils.handle_error(e,"Mute")
		elif self.type==self.TYPE_UNMUTE:
			try:
				user=self.account.api.destroy_mute(screen_name=self.returnvalue)
			except TweepyException as e:
				utils.handle_error(e,"Unmute")
		elif self.type==self.TYPE_USER_TIMELINE:
			misc.user_timeline_user(self.account,self.returnvalue)

	def OnClose(self, event):
		self.Destroy()

def chooser(account,title="choose",text="Choose some stuff",list=[],type=""):
	chooser=ChooseGui(account,title,text,list,type)
	chooser.Show()
	return chooser.returnvalue