from sound_lib import stream
import platform
import os, sys
import globals
import wx
from . import main

class general(wx.Panel, wx.Dialog):
	def __init__(self, account, parent):
		self.snd = stream.FileStream(file=globals.confpath+"/sounds/default/boundary.ogg")
		self.account=account
		super(general, self).__init__(parent)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.soundpack_box = wx.BoxSizer(wx.VERTICAL)
		self.soundpacklist_label=wx.StaticText(self, -1, "Soundpacks")
		self.soundpackslist = wx.ListBox(self, -1)
		self.soundpack_box.Add(self.soundpackslist, 0, wx.ALL, 10)
		self.soundpackslist.Bind(wx.EVT_LISTBOX, self.on_soundpacks_list_change)
		dirs = os.listdir(globals.confpath+"/sounds")
		for i in range(0,len(dirs)):
			if not dirs[i].startswith("_") and not dirs[i].startswith(".DS"):
				self.soundpackslist.Insert(dirs[i],self.soundpackslist.GetCount())
				if account.prefs.soundpack==dirs[i]:
					self.soundpackslist.SetSelection(self.soundpackslist.GetCount()-1)
					self.sp=dirs[i]
		try:
			dirs2 = os.listdir("sounds")
			for i in range(0,len(dirs2)):
				if not dirs2[i].startswith("_") and not dirs2[i].startswith(".DS") and dirs2[i] not in dirs:
					self.soundpackslist.Insert(dirs2[i],self.soundpackslist.GetCount())
					if account.prefs.soundpack==dirs2[i]:
						self.soundpackslist.SetSelection(self.soundpackslist.GetCount()-1)
						self.sp=dirs2[i]
		except:
			pass
		if not hasattr(self,"sp"):
			self.sp="default"
		self.text_label = wx.StaticText(self, -1, "Sound pan")
		self.soundpan = wx.Slider(self, -1, self.account.prefs.soundpan*50,-50,50,name="Soundpack Pan")
		self.soundpan.Bind(wx.EVT_SLIDER,self.OnPan)
		self.main_box.Add(self.soundpan, 0, wx.ALL, 10)
		self.text_label = wx.StaticText(self, -1, "Tweet Footer (Optional)")
		self.footer = wx.TextCtrl(self, -1, "",style=wx.TE_MULTILINE)
		self.main_box.Add(self.footer, 0, wx.ALL, 10)
		self.footer.AppendText(account.prefs.footer)
		if platform.system() != "Linux":
			self.footer.SetMaxLength(280)

	def OnPan(self,event):
		pan=self.soundpan.GetValue()/50
		self.snd.pan=pan
		self.snd.play()

	def on_soundpacks_list_change(self, event):
		self.sp=event.GetString()

class OptionsGui(wx.Dialog):
	def __init__(self,account):
		self.account=account
		wx.Dialog.__init__(self, None, title="Account Options for "+self.account.me.screen_name, size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.notebook = wx.Notebook(self.panel)
		self.general=general(self.account, self.notebook)
		self.notebook.AddPage(self.general, "General")
		self.general.SetFocus()
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
		self.account.prefs.soundpack=self.general.sp
		self.account.prefs.soundpan=self.general.soundpan.GetValue()/50
		self.account.prefs.footer=self.general.footer.GetValue()
		self.general.snd.free()
		self.Destroy()

	def OnClose(self, event):
		self.general.snd.free()
		self.Destroy()
