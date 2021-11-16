from tweepy import TweepyException
import speak
import wx
import globals
import sound
import utils
import platform
if platform.system()!="Darwin":
	import twitter_text.parse_tweet
from . import poll

text_box_size=(800,600)
class TweetGui(wx.Dialog):
	def __init__(self,account,inittext="",type="tweet",status=None):
		self.ids=[]
		self.account=account
		self.inittext=inittext
		self.max_length=0
		self.status=status
		self.type=type
		self.poll_runfor=None
		self.poll_opt1=None
		self.poll_opt2=None
		self.poll_opt3=None
		self.poll_opt4=None
		wx.Dialog.__init__(self, None, title=type, size=(350,200))
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "Te&xt")
		if globals.prefs.wrap:
			self.text = wx.TextCtrl(self.panel, -1, "",style=wx.TE_MULTILINE,size=text_box_size)
		else:
			self.text = wx.TextCtrl(self.panel, -1, "",style=wx.TE_MULTILINE|wx.TE_DONTWRAP,size=text_box_size)
		if platform.system()=="Darwin":
			self.text.MacCheckSpelling(True)
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.text.SetFocus()
		self.text.Bind(wx.EVT_TEXT, self.Chars)
		if self.type!="message":
			self.text.AppendText(inittext)
			cursorpos=len(inittext)
		else:
			cursorpos=0
		if self.type=="message":
			self.max_length=10000
		else:
			self.max_length=280
		if self.type=="message":
			self.text2_label = wx.StaticText(self.panel, -1, "Recipient")
		if self.type=="reply" or self.type=="quote" or self.type=="message":
			if self.type=="message":
				self.text2 = wx.TextCtrl(self.panel, -1, "",style=wx.TE_DONTWRAP,size=text_box_size)
			else:
				self.text2 = wx.TextCtrl(self.panel, -1, "",style=wx.TE_MULTILINE|wx.TE_DONTWRAP|wx.TE_READONLY,size=text_box_size)
			self.main_box.Add(self.text2, 0, wx.ALL, 10)
			if self.type=="message":
				self.text2.AppendText(inittext)
			else:
				self.text2.AppendText(status.user.screen_name+": "+status.text)
		if self.account.prefs.footer!="":
			self.text.AppendText(" "+self.account.prefs.footer)
		self.text.SetInsertionPoint(cursorpos)
		if self.type!="message":
			self.reply_settings_label=wx.StaticText(self.panel, -1, "Who can reply?")
			self.reply_settings=wx.Choice(self.panel,-1,size=(800,600))
			self.reply_settings.Insert("Everyone",self.reply_settings.GetCount())
			self.reply_settings.Insert("Mentioned Users Only",self.reply_settings.GetCount())
			self.reply_settings.Insert("Following Only",self.reply_settings.GetCount())
			self.reply_settings.SetSelection(0)
			self.main_box.Add(self.reply_settings, 0, wx.ALL, 10)
		if platform.system()=="Darwin":
			self.autocomplete = wx.Button(self.panel, wx.ID_DEFAULT, "User A&utocomplete")
		else:
			self.autocomplete = wx.Button(self.panel, wx.ID_DEFAULT, "User &Autocomplete")
		self.autocomplete.Bind(wx.EVT_BUTTON, self.Autocomplete)
		self.main_box.Add(self.autocomplete, 0, wx.ALL, 10)
		if self.type!="reply" and self.type!="message":
			self.poll = wx.Button(self.panel, wx.ID_DEFAULT, "Poll")
			self.poll.Bind(wx.EVT_BUTTON, self.Poll)
			self.main_box.Add(self.poll, 0, wx.ALL, 10)
		if self.type=="reply" and self.status!=None and "user_mentions" in self.status.entities and len(self.status.entities['user_mentions'])>0:
			self.users=utils.get_user_objects_in_tweet(self.account,self.status,True,True)
			self.list_label=wx.StaticText(self.panel, -1, label="&Users to include in reply")
			self.list=wx.CheckListBox(self.panel, -1)
			self.main_box.Add(self.list, 0, wx.ALL, 10)
			for i in self.users:
				self.list.Append(i.name+" ("+i.screen_name+")")
				self.list.Check(self.list.GetCount()-1,True)
				self.list.SetSelection(0)
				self.list.Bind(wx.EVT_CHECKLISTBOX,self.OnToggle)
		if self.type=="tweet" or self.type=="reply":
			self.thread=wx.CheckBox(self.panel, -1, "&Thread mode")
			self.main_box.Add(self.thread, 0, wx.ALL, 10)
		self.tweet = wx.Button(self.panel, wx.ID_DEFAULT, "&Send")
#		self.tweet.SetDefault()
		self.tweet.Bind(wx.EVT_BUTTON, self.Tweet)
		self.main_box.Add(self.tweet, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.Chars(None)
		self.text.Bind(wx.EVT_CHAR, self.onKeyPress)
		self.panel.Layout()

	def Poll(self,event):
		p=poll.PollGui()
		result=p.ShowModal()
		if result==wx.ID_CANCEL: return False
		self.poll_runfor=p.runfor.GetValue()*60*24
		self.poll_opt1=p.opt1.GetValue()
		self.poll_opt2=p.opt2.GetValue()
		self.poll_opt3=p.opt3.GetValue()
		self.poll_opt4=p.opt4.GetValue()
		self.poll.Enable(False)

	def onKeyPress(self,event):
		mods = event.HasAnyModifiers()
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_RETURN:
			if not mods:
				self.Tweet(None)
		event.Skip()

	def OnToggle(self,event):
		index=event.GetInt()
		if self.list.IsChecked(index):
			speak.speak("Checked")
		else:
			speak.speak("Unchecked.")

	def Autocomplete(self,event):
		if self.type=="message":
			txt=self.text2.GetValue().split(" ")
		else:
			txt=self.text.GetValue().split(" ")
		text=""
		for i in txt:
			if (self.type!="message" and i.startswith("@") or self.type=="message") and utils.lookup_user_name(self.account,i.strip("@"),False)==-1:
				text=i.strip("@")

		if text=="":
			speak.speak("No user to autocomplete")
			return
		self.menu = wx.Menu()
		for i in globals.users:
			if i.screen_name.lower().startswith(text.lower()) or i.name.lower().startswith(text.lower()):
				self.create_menu_item(self.menu, i.name+" (@"+i.screen_name+")", lambda event, orig=text, text=i.screen_name: self.OnUser(event,orig, text))
		self.PopupMenu(self.menu)

	def Newline(self,event):
		if platform.system()=="Darwin":
			nl="\n"
		else:
			nl="\r\n"
		self.text.WriteText(nl)

	def create_menu_item(self,menu, label, func):
		item = wx.MenuItem(menu, -1, label)
		menu.Bind(wx.EVT_MENU, func, id=item.GetId())
		menu.Append(item)
		return item

	def OnUser(self,event, orig, text):
		if self.type!="message":
			v=self.text.GetValue().replace(orig,text)
			self.text.SetValue(v)
			self.text.SetInsertionPoint(len(v))
		else:
			v=self.text2.GetValue().replace(orig,text)
			self.text2.SetValue(v)

	def next_thread(self):
		self.text.SetValue("")
		self.text.AppendText(self.inittext)
		cursorpos=len(self.inittext)
		if self.account.prefs.footer!="":
			self.text.AppendText(" "+self.account.prefs.footer)
		self.text.SetInsertionPoint(cursorpos)

	def maximum(self):
		sound.play(self.account,"max_length")

	def Chars(self, event):
		if platform.system()!="Darwin":
			results=twitter_text.parse_tweet(self.text.GetValue())
			length=results.weightedLength
		else:
			length=len(self.text.GetValue())
		if length>0 and self.max_length>0:
			percent=str(int((length/self.max_length)*100))
		else:
			percent="0"
		if self.max_length>0 and length>self.max_length:
			self.maximum()
		self.SetLabel(self.type+" - "+str(length).split(".")[0]+" of "+str(self.max_length)+" characters ("+percent+" Percent)")

	def Tweet(self, event):
		snd=""
		if self.type!="message":
			if self.reply_settings.GetSelection()==0: ReplySettings=None
			elif self.reply_settings.GetSelection()==1: ReplySettings="mentionedUsers"
			elif self.reply_settings.GetSelection()==2: ReplySettings="following"
			globals.prefs.tweets_sent+=1
			if self.status!=None:
				if self.type=="quote":
					globals.prefs.quotes_sent+=1
					status=self.account.quote(self.status, self.text.GetValue())
				else:
					globals.prefs.replies_sent+=1
					if self.type=="reply":
						index=0
						if hasattr(self,"list"):
							for i in self.users:
								if not self.list.IsChecked(index):
									self.ids.append(str(i.id))
								index+=1
						status=self.account.tweet(self.text.GetValue(),self.status.id,exclude_reply_user_ids=",".join(self.ids),reply_settings=ReplySettings)
					else:
						status=self.account.tweet(self.text.GetValue(),self.status.id,reply_settings=ReplySettings)
			else:
				if self.poll_opt1!=None and self.poll_opt1!="":
					opts=[]
					if self.poll_opt1!="" and self.poll_opt1!=None: opts.append(self.poll_opt1)
					if self.poll_opt2!="" and self.poll_opt2!=None: opts.append(self.poll_opt2)
					if self.poll_opt3!="" and self.poll_opt3!=None: opts.append(self.poll_opt3)
					if self.poll_opt4!="" and self.poll_opt4!=None: opts.append(self.poll_opt4)
					status=self.account.tweet(self.text.GetValue(),id=None, reply_settings=ReplySettings, poll_duration_minutes=self.poll_runfor, poll_options=opts)
				else:
					status=self.account.tweet(self.text.GetValue(),reply_settings=ReplySettings)
			globals.prefs.chars_sent+=len(self.text.GetValue())
		else:
			id=None
			user=utils.lookup_user_name(self.account, self.text2.GetValue())
			if user!=-1:
				id=user.id
			try:
				status=self.account.api.send_direct_message(recipient_id=id,text=self.text.GetValue())
			except TweepyException as error:
				sound.play(self.account,"error")
				if hasattr(error,"response") and error.response!=None:
					speak.speak(error.response.text)
				else:
					speak.speak(error.reason)

		if self.type=="reply" or self.type=="quote":
			snd="send_reply"
		elif self.type=="tweet":
			snd="send_tweet"
		elif self.type=="message":
			snd="send_message"
		if status!=False:
			sound.play(self.account,snd)
			if hasattr(self,"thread") and not self.thread.GetValue() or not hasattr(self, "thread"):
				self.Destroy()
			else:
				self.status=status
				self.next_thread()
		else:
			sound.play(self.account,"error")
	def OnClose(self, event):
		self.Destroy()
