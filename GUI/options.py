import timeline
import platform
import os, sys
import globals
import wx
from . import main

class general(wx.Panel, wx.Dialog):
	def __init__(self, parent):
		super(general, self).__init__(parent)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.ask_dismiss=wx.CheckBox(self, -1, "Ask before dismissing timelines")
		self.main_box.Add(self.ask_dismiss, 0, wx.ALL, 10)
		self.ask_dismiss.SetValue(globals.prefs.ask_dismiss)
		self.earcon_audio=wx.CheckBox(self, -1, "Play a sound when a tweet contains media")
		self.main_box.Add(self.earcon_audio, 0, wx.ALL, 10)
		self.earcon_audio.SetValue(globals.prefs.earcon_audio)
		self.earcon_top=wx.CheckBox(self, -1, "Play a sound when you navigate to a timeline that may have new items")
		self.main_box.Add(self.earcon_top, 0, wx.ALL, 10)
		self.earcon_top.SetValue(globals.prefs.earcon_top)
		self.demojify=wx.CheckBox(self, -1, "Remove emojis and other unicode characters from display names")
		self.main_box.Add(self.demojify, 0, wx.ALL, 10)
		self.demojify.SetValue(globals.prefs.demojify)
		self.demojify_tweet=wx.CheckBox(self, -1, "Remove emojis and other unicode characters from tweet text")
		self.main_box.Add(self.demojify_tweet, 0, wx.ALL, 10)
		self.demojify_tweet.SetValue(globals.prefs.demojify_tweet)
		self.reversed=wx.CheckBox(self, -1, "Reverse timelines (newest on bottom)")
		self.main_box.Add(self.reversed, 0, wx.ALL, 10)
		self.reversed.SetValue(globals.prefs.reversed)
		self.wrap=wx.CheckBox(self, -1, "Word wrap in text fields")
		self.main_box.Add(self.wrap, 0, wx.ALL, 10)
		self.wrap.SetValue(globals.prefs.wrap)
		self.autoOpenSingleURL=wx.CheckBox(self, -1, "when getting URLs from a tweet, automatically open the first URL if it is the only one")
		self.main_box.Add(self.autoOpenSingleURL, 0, wx.ALL, 10)
		self.autoOpenSingleURL.SetValue(globals.prefs.autoOpenSingleURL)
		self.use24HourTime=wx.CheckBox(self, -1, "Use 24-hour time for tweet timestamps")
		self.main_box.Add(self.use24HourTime, 0, wx.ALL, 10)
		self.use24HourTime.SetValue(globals.prefs.use24HourTime)


class templates(wx.Panel, wx.Dialog):
	def __init__(self, parent):
		super(templates, self).__init__(parent)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.tweetTemplate_label = wx.StaticText(self, -1, "Tweet template")
		self.tweetTemplate = wx.TextCtrl(self, -1, "")
		self.main_box.Add(self.tweetTemplate, 0, wx.ALL, 10)
		self.tweetTemplate.AppendText(globals.prefs.tweetTemplate)
		self.quoteTemplate_label = wx.StaticText(self, -1, "Quote template")
		self.quoteTemplate = wx.TextCtrl(self, -1, "")
		self.main_box.Add(self.quoteTemplate, 0, wx.ALL, 10)
		self.quoteTemplate.AppendText(globals.prefs.quoteTemplate)
		self.retweetTemplate_label = wx.StaticText(self, -1, "Retweet template")
		self.retweetTemplate = wx.TextCtrl(self, -1, "")
		self.main_box.Add(self.retweetTemplate, 0, wx.ALL, 10)
		self.retweetTemplate.AppendText(globals.prefs.retweetTemplate)
		self.copyTemplate_label = wx.StaticText(self, -1, "Copy template")
		self.copyTemplate = wx.TextCtrl(self, -1, "")
		self.main_box.Add(self.copyTemplate, 0, wx.ALL, 10)
		self.copyTemplate.AppendText(globals.prefs.copyTemplate)
		self.messageTemplate_label = wx.StaticText(self, -1, "Direct Message template")
		self.messageTemplate = wx.TextCtrl(self, -1, "")
		self.main_box.Add(self.messageTemplate, 0, wx.ALL, 10)
		self.messageTemplate.AppendText(globals.prefs.messageTemplate)
		self.userTemplate_label = wx.StaticText(self, -1, "User template")
		self.userTemplate = wx.TextCtrl(self, -1, "")
		self.main_box.Add(self.userTemplate, 0, wx.ALL, 10)
		self.userTemplate.AppendText(globals.prefs.userTemplate)

class advanced(wx.Panel, wx.Dialog):
	def __init__(self, parent):
		super(advanced, self).__init__(parent)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		if platform.system()!="Darwin":
			self.invisible=wx.CheckBox(self, -1, "Enable invisible interface")
			self.main_box.Add(self.invisible, 0, wx.ALL, 10)
			self.invisible.SetValue(globals.prefs.invisible)
			self.invisible_sync=wx.CheckBox(self, -1, "Sync invisible interface with UI (uncheck for reduced lag in invisible interface)")
			self.main_box.Add(self.invisible_sync, 0, wx.ALL, 10)
			self.invisible_sync.SetValue(globals.prefs.invisible_sync)
			self.repeat=wx.CheckBox(self, -1, "Repeat items at edges of invisible interface")
			self.main_box.Add(self.repeat, 0, wx.ALL, 10)
			self.repeat.SetValue(globals.prefs.repeat)
		self.position=wx.CheckBox(self, -1, "Speak position information when navigating between timelines of invisible interface and switching timelines")
		self.main_box.Add(self.position, 0, wx.ALL, 10)
		self.position.SetValue(globals.prefs.position)
		self.update_time_label = wx.StaticText(self, -1, "Update time, in minutes")
		self.update_time = wx.TextCtrl(self, -1, "")
		self.main_box.Add(self.update_time, 0, wx.ALL, 10)
		self.update_time.AppendText(str(globals.prefs.update_time))
		self.user_limit_label = wx.StaticText(self, -1, "Max API calls when fetching users in user viewer")
		self.user_limit = wx.TextCtrl(self, -1, "")
		self.main_box.Add(self.user_limit, 0, wx.ALL, 10)
		self.user_limit.AppendText(str(globals.prefs.user_limit))
		self.count_label = wx.StaticText(self, -1, "Number of tweets to fetch per call (Maximum is 200)")
		self.count = wx.TextCtrl(self, -1, "")
		self.main_box.Add(self.count, 0, wx.ALL, 10)
		self.count.AppendText(str(globals.prefs.count))
		self.streaming=wx.CheckBox(self, -1, "Enable streaming for home, mentions, and list timelines (Requires restart to disable)")
		self.main_box.Add(self.streaming, 0, wx.ALL, 10)
		self.streaming.SetValue(globals.prefs.streaming)
		self.media_player_box=wx.StaticBox(self, -1,"Media Player path")
		self.media_player=wx.FilePickerCtrl(self.media_player_box, -1, "", "Path to external Media Player")
		self.main_box.Add(self.media_player, 0, wx.ALL, 10)
		self.media_player.SetPath(globals.prefs.media_player)
		self.main_box.Add(self.media_player_box, 0, wx.ALL, 10)

class OptionsGui(wx.Dialog):
	def __init__(self):
		wx.Dialog.__init__(self, None, title="Options", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.notebook = wx.Notebook(self.panel)
		self.general=general(self.notebook)
		self.notebook.AddPage(self.general, "General")
		self.general.SetFocus()
		self.templates=templates(self.notebook)
		self.notebook.AddPage(self.templates, "Templates")
		self.advanced=advanced(self.notebook)
		self.notebook.AddPage(self.advanced, "Advanced")
		self.main_box.Add(self.notebook, 0, wx.ALL, 10)
		self.ok = wx.Button(self.panel, wx.ID_OK, "&OK")
		self.ok.SetDefault()
		self.ok.Bind(wx.EVT_BUTTON, self.OnOK)
		self.main_box.Add(self.ok, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()

	def OnOK(self, event):
		refresh=False
		globals.prefs.use24HourTime = self.general.use24HourTime.GetValue()
		globals.prefs.ask_dismiss=self.general.ask_dismiss.GetValue()
		if platform.system()!="Darwin":
			globals.prefs.invisible=self.advanced.invisible.GetValue()
			globals.prefs.invisible_sync=self.advanced.invisible_sync.GetValue()
			globals.prefs.repeat=self.advanced.repeat.GetValue()
			globals.prefs.invisible_sync=self.advanced.invisible_sync.GetValue()
			if globals.prefs.invisible==True and main.window.invisible==False:
				main.window.register_keys()
			if globals.prefs.invisible==False and main.window.invisible==True:
				main.window.unregister_keys()
		globals.prefs.streaming=self.advanced.streaming.GetValue()
		globals.prefs.position=self.advanced.position.GetValue()
		globals.prefs.media_player=self.advanced.media_player.GetPath()
		globals.prefs.earcon_audio=self.general.earcon_audio.GetValue()
		globals.prefs.earcon_top=self.general.earcon_top.GetValue()
		globals.prefs.wrap=self.general.wrap.GetValue()
		globals.prefs.update_time=int(self.advanced.update_time.GetValue())
		if globals.prefs.update_time<1:
			globals.prefs.update_time=1
		globals.prefs.user_limit=int(self.advanced.user_limit.GetValue())
		if globals.prefs.user_limit<1:
			globals.prefs.user_limit=1
		if globals.prefs.user_limit>15:
			globals.prefs.user_limit=15
		globals.prefs.count=int(self.advanced.count.GetValue())
		if globals.prefs.count>200:
			globals.prefs.count=200
		if globals.prefs.reversed!=self.general.reversed.GetValue():
			reverse=True
		else:
			reverse=False
		globals.prefs.reversed=self.general.reversed.GetValue()
		if globals.prefs.demojify_tweet!=self.general.demojify_tweet.GetValue() or globals.prefs.demojify!=self.general.demojify.GetValue() or globals.prefs.tweetTemplate!=self.templates.tweetTemplate.GetValue() or globals.prefs.retweetTemplate!=self.templates.retweetTemplate.GetValue or globals.prefs.quoteTemplate!=self.templates.quoteTemplate.GetValue or globals.prefs.messageTemplate!=self.templates.messageTemplate.GetValue():
			refresh=True
		globals.prefs.demojify=self.general.demojify.GetValue()
		globals.prefs.demojify_tweet=self.general.demojify_tweet.GetValue()
		globals.prefs.tweetTemplate=self.templates.tweetTemplate.GetValue()
		globals.prefs.quoteTemplate=self.templates.quoteTemplate.GetValue()
		globals.prefs.retweetTemplate=self.templates.retweetTemplate.GetValue()
		globals.prefs.messageTemplate=self.templates.messageTemplate.GetValue()
		globals.prefs.copyTemplate=self.templates.copyTemplate.GetValue()
		globals.prefs.userTemplate=self.templates.userTemplate.GetValue()
		globals.prefs.autoOpenSingleURL=self.general.autoOpenSingleURL.GetValue()
		self.Destroy()
		if reverse==True:
			timeline.reverse()
		if refresh==True:
			main.window.refreshList()

	def OnClose(self, event):
		self.Destroy()
