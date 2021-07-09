from tweepy import TweepError
import speak
import wx
import globals
import sound
import utils
import platform
import twitter_text.parse_tweet

text_box_size=(800,600)
class TweetGui(wx.Dialog):
	def __init__(self,account,inittext="",type="tweet",status=None):
		self.ids=[]
		self.account=account
		self.inittext=inittext
		self.max_length=0
		self.status=status
		self.type=type
		wx.Dialog.__init__(self, None, title=type, size=(350,200))
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "Te&xt")
		if globals.prefs.wrap:
			self.text = wx.TextCtrl(self.panel, -1, "",style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER,size=text_box_size)
		else:
			self.text = wx.TextCtrl(self.panel, -1, "",style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_DONTWRAP,size=text_box_size)
		if platform.system()=="Darwin":
			self.text.MacCheckSpelling(True)
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.text.SetFocus()
		self.text.Bind(wx.EVT_TEXT_ENTER, self.Tweet)
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
				self.text2 = wx.TextCtrl(self.panel, -1, "",style=wx.TE_PROCESS_ENTER|wx.TE_DONTWRAP,size=text_box_size)
			else:
				self.text2 = wx.TextCtrl(self.panel, -1, "",style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_DONTWRAP|wx.TE_READONLY,size=text_box_size)
			self.main_box.Add(self.text2, 0, wx.ALL, 10)
			self.text2.Bind(wx.EVT_TEXT_ENTER, self.Tweet)
			if self.type=="message":
				self.text2.AppendText(inittext)
			else:
				self.text2.AppendText(status.user.screen_name+": "+status.text)
		if self.account.prefs.footer!="":
			self.text.AppendText(" "+self.account.prefs.footer)
		self.text.SetInsertionPoint(cursorpos)
		if platform.system()=="Darwin":
			self.autocomplete = wx.Button(self.panel, wx.ID_DEFAULT, "User A&utocomplete")
		else:
			self.autocomplete = wx.Button(self.panel, wx.ID_DEFAULT, "User &Autocomplete")
		self.autocomplete.Bind(wx.EVT_BUTTON, self.Autocomplete)
		self.main_box.Add(self.autocomplete, 0, wx.ALL, 10)
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
		self.tweet.SetDefault()
		self.tweet.Bind(wx.EVT_BUTTON, self.Tweet)
		self.main_box.Add(self.tweet, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.Chars(None)
		self.panel.Layout()

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
		results=twitter_text.parse_tweet.parse_tweet(self.text.GetValue())
		length=results.weightedLength
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
								if self.list.IsChecked(index)==False:
									self.ids.append(str(i.id))
								index+=1
						status=self.account.tweet(self.text.GetValue(),self.status.id,auto_populate_reply_metadata=True,exclude_reply_user_ids=",".join(self.ids))
					else:
						status=self.account.tweet(self.text.GetValue(),self.status.id)
			else:
				status=self.account.tweet(self.text.GetValue())
			globals.prefs.chars_sent+=len(self.text.GetValue())
		else:
			id=None
			user=utils.lookup_user_name(self.account, self.text2.GetValue())
			if user!=-1:
				id=user.id
			try:
				status=self.account.api.send_direct_message(id,self.text.GetValue())
			except TweepError as error:
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
			if hasattr(self,"thread")==True and self.thread.GetValue()==False or hasattr(self,"thread")==False:
				self.Destroy()
			else:
				self.status=status
				self.next_thread()
		else:
			sound.play(self.account,"error")
	def OnClose(self, event):
		self.Destroy()
