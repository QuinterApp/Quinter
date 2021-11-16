import requests
from tweepy import TweepyException
import platform
import twishort
import globals
from . import misc
import wx
import utils
import sound
text_box_size=(800,600)
class ViewGui(wx.Dialog):

	def __init__(self,account,status):
		self.account=account
		if hasattr(status,"message_create"):
			self.status=status
			self.tweet_text=utils.process_message(self.status,True)
			self.type="message"
			wx.Dialog.__init__(self, None, title="View Tweet from "+utils.lookup_user(status.message_create['sender_id']).name+" ("+utils.lookup_user(status.message_create['sender_id']).screen_name+")", size=(350,200)) # initialize the wx frame
		else:
			try:
				self.status=account.api.get_status(id=status.id,include_ext_alt_text=True,tweet_mode="extended")
			except TweepyException as error:
				utils.handle_error(error)
				self.Destroy()
				return
			self.tweet_text=utils.process_tweet(self.status,True)
			self.type="tweet"
			wx.Dialog.__init__(self, None, title="View Tweet from "+status.user.name+" ("+status.user.screen_name+")", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		urls=utils.find_urls_in_text(self.tweet_text)
		for i in urls:
			if "twishort" in i:
				self.tweet_text=twishort.get_full_text(twishort.get_twishort_uri(i))
		self.text_label = wx.StaticText(self.panel, -1, "Te&xt")
		if globals.prefs.wrap:
			self.text = wx.TextCtrl(self.panel, style=wx.TE_READONLY|wx.TE_MULTILINE, size=text_box_size)
		else:
			self.text = wx.TextCtrl(self.panel, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_DONTWRAP, size=text_box_size)
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.text.SetFocus()
		if self.type=="tweet":
			self.text.SetValue(self.tweet_text)
		else:
			self.text.SetValue(status.message_create['message_data']['text'])
		if self.type=="tweet":
			self.text2_label = wx.StaticText(self.panel, -1, "Tweet &Details")
			self.text2 = wx.TextCtrl(self.panel, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_DONTWRAP, size=text_box_size)
			self.main_box.Add(self.text2, 0, wx.ALL, 10)
			extra=""
			if hasattr(self.status,"extended_entities"):
				if "media" in self.status.extended_entities:
					index=0
					for i in self.status.extended_entities['media']:
						index+=1
						extra+="Media "+str(index)+"\r\nType: "+i['type']+"\r\nRaw URL: "+i['media_url']+"\r\n"
						if i['ext_alt_text']!=None:
							extra+="Image description: "+i['ext_alt_text']+"\r\n"
			self.text2.SetValue(extra+"Posted: "+utils.parse_date(self.status.created_at)+"\r\nFrom: "+self.status.source+"\r\nLiked "+str(self.status.favorite_count)+" times\r\nRetweeted "+str(self.status.retweet_count)+" times.")
			if platform.system()=="Darwin":
				self.text2.SetValue(self.text2.GetValue().replace("\r",""))
			self.view_orig = wx.Button(self.panel, -1, "&Original tweet")
			self.view_orig.Bind(wx.EVT_BUTTON, self.OnViewOrig)
			self.main_box.Add(self.view_orig, 0, wx.ALL, 10)
			self.view_retweeters = wx.Button(self.panel, -1, "&View Retweeters")
			self.view_retweeters.Bind(wx.EVT_BUTTON, self.OnViewRetweeters)
			self.main_box.Add(self.view_retweeters, 0, wx.ALL, 10)
			if self.status.retweet_count==0:
				self.view_retweeters.Enable(False)
			if not hasattr(self.status,"retweeted_status") and not hasattr(self.status,"quoted_status"):
				self.view_orig.Enable(False)
			self.view_image = wx.Button(self.panel, -1, "&View Image")
			self.view_image.Bind(wx.EVT_BUTTON, self.OnViewImage)
			self.main_box.Add(self.view_image, 0, wx.ALL, 10)
			if not hasattr(self.status,"extended_entities") or hasattr(self.status,"extended_entities") and self.status.extended_entities['media'] == 0:
				self.view_image.Enable(False)
			self.reply = wx.Button(self.panel, -1, "&Reply")
			self.reply.Bind(wx.EVT_BUTTON, self.OnReply)
			self.main_box.Add(self.reply, 0, wx.ALL, 10)
			self.retweet = wx.Button(self.panel, -1, "R&etweet")
			self.retweet.Bind(wx.EVT_BUTTON, self.OnRetweet)
			self.main_box.Add(self.retweet, 0, wx.ALL, 10)
			self.like = wx.Button(self.panel, -1, "&Like")
			self.like.Bind(wx.EVT_BUTTON, self.OnLike)
			self.main_box.Add(self.like, 0, wx.ALL, 10)
			if len(utils.get_user_objects_in_tweet(self.account,self.status,True,True))>0:
				self.profile = wx.Button(self.panel, -1, "View &Profile of "+self.status.user.name+" and "+str(len(utils.get_user_objects_in_tweet(self.account,self.status,True,True)))+" more")
			else:
				self.profile = wx.Button(self.panel, -1, "View &Profile of "+self.status.user.name)

		if self.type=="tweet":
			self.message = wx.Button(self.panel, -1, "&Message "+self.status.user.name)
		else:
			self.profile = wx.Button(self.panel, -1, "View &Profile of "+utils.lookup_user(self.status.message_create['sender_id']).name)
			self.message = wx.Button(self.panel, -1, "&Message "+utils.lookup_user(self.status.message_create['sender_id']).name)
		self.message.Bind(wx.EVT_BUTTON, self.OnMessage)
		self.main_box.Add(self.message, 0, wx.ALL, 10)
		self.profile.Bind(wx.EVT_BUTTON, self.OnProfile)
		self.main_box.Add(self.profile, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Close")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()

	def OnViewOrig(self,event):
		if hasattr(self.status,"retweeted_status"):
			v=ViewGui(self.account,self.status.retweeted_status)
			v.Show()
		elif hasattr(self.status,"quoted_status"):
			v=ViewGui(self.account,self.status.quoted_status)
			v.Show()

	def OnViewImage(self,event):
		v=ViewImageGui(self.status)
		v.Show()

	def OnReply(self,event):
		misc.reply(self.account,self.status)

	def OnRetweet(self,event):
		misc.retweet(self.account,self.status)

	def OnViewRetweeters(self,event):
		users=[]
		if hasattr(self.status,"retweeted_status"):
			r=self.account.api.get_retweets(id=self.status.retweeted_status.id)
		else:
			r=self.account.api.get_retweets(id=self.status.id)
		for i in r:
			users.append(i.user)
		g=UserViewGui(self.account,users,"Retweeters")
		g.Show()

	def OnLike(self,event):
		misc.like(self.account,self.status)

	def OnProfile(self,event):
		if hasattr(self.status,"message_create"):
			u=[utils.lookup_user(self.account,self.status.message_create['sender_id'])]
		else:
			u=[self.status.user]
			u2=utils.get_user_objects_in_tweet(self.account,self.status,True,True)
			for i in u2:
				u.append(i)
		g=UserViewGui(self.account,u)
		g.Show()

	def OnMessage(self,event):
		misc.message(self.account,self.status)

	def OnClose(self, event):
		self.Destroy()

class UserViewGui(wx.Dialog):

	def __init__(self,account,users=[],title="User Viewer"):
		self.account=account
		self.index=0
		self.users=users
		wx.Dialog.__init__(self, None, title=title, size=(350,200))
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.list_label=wx.StaticText(self.panel, -1, label="&Users")
		self.list=wx.ListBox(self.panel, -1)
		self.main_box.Add(self.list, 0, wx.ALL, 10)
		self.list.Bind(wx.EVT_LISTBOX, self.on_list_change)
		for i in self.users:
			extra=""
			if i.protected:
				extra+=", Protected"
			if i.following:
				extra+=", You follow"
			if i.description!="" and i.description!=None:
				extra+=", "+i.description
			self.list.Insert(i.name+" (@"+i.screen_name+")"+extra,self.list.GetCount())
		self.index=0
		self.list.SetSelection(self.index)
		if len(self.users)==1:
			self.list.Show(False)
		else:
			self.list.SetFocus()
		self.text_label = wx.StaticText(self.panel, -1, "Info")
		self.text = wx.TextCtrl(self.panel, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_DONTWRAP, size=text_box_size)
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		if len(self.users)==1:
			self.text.SetFocus()
		self.follow = wx.Button(self.panel, -1, "&Follow")
		self.follow.Bind(wx.EVT_BUTTON, self.OnFollow)
		self.main_box.Add(self.follow, 0, wx.ALL, 10)
		self.unfollow = wx.Button(self.panel, -1, "&Unfollow")
		self.unfollow.Bind(wx.EVT_BUTTON, self.OnUnfollow)
		self.main_box.Add(self.unfollow, 0, wx.ALL, 10)
		self.message = wx.Button(self.panel, -1, "&Message")
		self.message.Bind(wx.EVT_BUTTON, self.OnMessage)
		self.main_box.Add(self.message, 0, wx.ALL, 10)
		self.timeline = wx.Button(self.panel, -1, "&Timeline")
		self.timeline.Bind(wx.EVT_BUTTON, self.OnTimeline)
		self.main_box.Add(self.timeline, 0, wx.ALL, 10)
		self.image = wx.Button(self.panel, -1, "View Profile Ima&ge")
		self.image.Bind(wx.EVT_BUTTON, self.OnImage)
		self.main_box.Add(self.image, 0, wx.ALL, 10)
		self.followers = wx.Button(self.panel, -1, "View Fo&llowers")
		self.followers.Bind(wx.EVT_BUTTON, self.OnFollowers)
		self.main_box.Add(self.followers, 0, wx.ALL, 10)
		self.friends = wx.Button(self.panel, -1, "View F&riends")
		self.friends.Bind(wx.EVT_BUTTON, self.OnFriends)
		self.main_box.Add(self.friends, 0, wx.ALL, 10)
		self.follow.Enable(False)
		self.unfollow.Enable(False)
		self.timeline.Enable(False)
		self.message.Enable(False)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Close")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.on_list_change(None)
		menu = wx.Menu()
		m_speak_user=menu.Append(-1, "Speak user", "speak")
		self.Bind(wx.EVT_MENU, self.OnSpeakUser, m_speak_user)
		accel=[]
		accel.append((wx.ACCEL_CTRL, ord(';'), m_speak_user.GetId()))
		accel_tbl=wx.AcceleratorTable(accel)
		self.SetAcceleratorTable(accel_tbl)
		self.panel.Layout()

	def OnSpeakUser(self,event):
		self.index=self.list.GetSelection()
		user=self.users[self.index].screen_name
		utils.speak_user(globals.currentAccount,[user])

	def on_list_change(self,event):
		self.index=self.list.GetSelection()
		user=self.users[self.index]
		if user.following:
			self.unfollow.Enable(True)
			self.follow.Enable(False)
		else:
			self.unfollow.Enable(False)
			self.follow.Enable(True)
		self.message.Enable(True)
		self.timeline.Enable(True)

		extra=""
		if hasattr(user,"entities") and "url" in user.entities and "urls" in user.entities['url']:
			for i in user.entities['url']['urls']:
				extra+="\r\nURL: "+i['expanded_url']
		if hasattr(user,"status"):
			extra+="\r\nLast tweeted: "+utils.parse_date(user.status.created_at)
		self.text.SetValue("Name: "+user.name+"\r\nScreen Name: "+user.screen_name+"\r\nLocation: "+user.location+"\r\nBio: "+str(user.description)+extra+"\r\nFollowers: "+str(user.followers_count)+"\r\nFriends: "+str(user.friends_count)+"\r\nTweets: "+str(user.statuses_count)+"\r\nLikes: "+str(user.favourites_count)+"\r\nCreated: "+utils.parse_date(user.created_at)+"\r\nProtected: "+str(user.protected)+"\r\nFollowing: "+str(user.following)+"\r\nNotifications enabled: "+str(user.notifications))
		if platform.system()=="Darwin":
			self.text.SetValue(self.text.GetValue().replace("\r",""))

	def OnFollow(self,event):
		user=self.users[self.index]
		misc.follow_user(self.account,user.screen_name)

	def OnUnfollow(self,event):
		user=self.users[self.index]
		misc.unfollow_user(self.account,user.screen_name)

	def OnFollowers(self,event):
		user=self.users[self.index]
		misc.followers(self.account,user.id)

	def OnFriends(self,event):
		user=self.users[self.index]
		misc.friends(self.account,user.id)

	def OnMessage(self,event):
		user=self.users[self.index]
		misc.message_user(self.account,user.screen_name)

	def OnTimeline(self,event):
		user=self.users[self.index]
		misc.user_timeline_user(self.account,user.screen_name)

	def OnImage(self,event):
		user=self.users[self.index]
		v=ViewImageGui(user)
		v.Show()

	def OnClose(self, event):
		"""App close event handler"""
		self.Destroy()

class ViewTextGui(wx.Dialog):

	def __init__(self,text):
		wx.Dialog.__init__(self, None, title="Text", size=(350,200)) # initialize the wx frame
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "Te&xt")
		self.text = wx.TextCtrl(self.panel, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_DONTWRAP)
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.text.SetValue(text)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Close")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()

	def OnClose(self, event):
		self.Destroy()

class ViewImageGui(wx.Dialog):

	def __init__(self,status):
		self.url=None
		if hasattr(status,"profile_image_url_https"):
			self.url=status.profile_image_url_https
		elif hasattr(status,"extended_entities"):
			if "media" in status.extended_entities:
				for i in status.extended_entities['media']:
					self.url=i['media_url']
					break
		image=requests.get(self.url)
		f=open(globals.confpath+"/temp_image","wb")
		f.write(image.content)
		f.close()
		self.image=wx.Image(globals.confpath+"/temp_image",wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		self.size=(self.image.GetWidth(), self.image.GetHeight())
		wx.Dialog.__init__(self, None, title="Image", size=self.size) # initialize the wx frame
		self.SetClientSize(self.size)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.text_label = wx.StaticText(self.panel, -1, "Image")
		self.text = wx.StaticBitmap(self.panel, -1, self.image, (10, 5), self.size)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Close")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.panel.Layout()

	def OnClose(self, event):
		self.Destroy()