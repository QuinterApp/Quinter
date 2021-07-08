import tweepy
from tweepy import TweepError
import streaming
import application
import utils
import threading
from GUI import main, misc
import tweak
import timeline
import speak
from GUI.ask import *
import webbrowser
import platform
import os

import globals
import sound
if platform.system() == "Windows":
	API_KEY = "xyTlkymHxgbfjasI2OL0O2ssG"
	API_SECRET = "sLKYWCCZw5zX6xR2K04enB0TAQLTwCsCHuQIEhZT4KHhkCM6zW"
elif platform.system() == "Darwin":
	API_KEY = "pCQOjY5bd1ifqve7WeTEhcm2Z"
	API_SECRET = "aKRqASlPQyWTigLmy1x4n16Kg5LCnidZK1eVRSVMIqPB56XtU7"

class twitter(object):
	def __init__(self,index):
		self.stream_thread=None
		self.ready=False
		self.timelines=[]
		self.currentTimeline=None
		self.currentIndex=0
		self.currentStatus=None
		self.confpath=""
		self.prefs=tweak.Config(name="Quinter/account"+str(index),autosave=True)
		self.confpath=self.prefs.user_config_dir
		self.prefs.key=self.prefs.get("key","")
		self.prefs.secret=self.prefs.get("secret","")
		self.prefs.user_timelines=self.prefs.get("user_timelines",[])
		self.prefs.list_timelines=self.prefs.get("list_timelines",[])
		self.prefs.search_timelines=self.prefs.get("search_timelines",[])
		self.prefs.follow_prompt=self.prefs.get("follow_prompt",False)
		self.prefs.footer=self.prefs.get("footer","")
		self.prefs.soundpack=self.prefs.get("soundpack","default")
		self.prefs.soundpan=self.prefs.get("soundpan",0)
		self.auth=tweepy.OAuthHandler(API_KEY, API_SECRET)
		if self.prefs.key==None or self.prefs.secret==None or self.prefs.key=="" or self.prefs.secret=="":
			if platform.system()!="Darwin":
				webbrowser.open(self.auth.get_authorization_url())
			else:
				os.system("open "+self.auth.get_authorization_url())
			verifier = ask(caption="Pin",message='Enter pin:')
			if verifier==None:
				sys.exit()
			self.auth.get_access_token(verifier)
			self.prefs.key=self.auth.access_token
			self.prefs.secret=self.auth.access_token_secret
		else:
			self.auth.set_access_token(self.prefs.key,self.prefs.secret)
		self.api = tweepy.API(self.auth)
		self.me=self.api.me()
		if globals.currentAccount==None:
			globals.currentAccount=self
			main.window.SetLabel(self.me.screen_name+" - "+application.name+" "+application.version)
		timeline.add(self,"Home","home")
		timeline.add(self,"Mentions","mentions")
		timeline.add(self,"Messages","messages")
		timeline.add(self,"Likes","likes")
		timeline.add(self,"Sent","user",self.me.screen_name,self.me)
		for i in self.prefs.user_timelines:
			misc.user_timeline_user(self,i,False)
		for i in self.prefs.list_timelines:
			misc.list_timeline(self,self.api.get_list(list_id=i).name,i,False)
		for i in self.prefs.search_timelines:
			misc.search(self,i,False)
		self.stream_listener=None
		self.stream=None
		if globals.prefs.streaming==True:
			self.start_stream()

		if globals.currentAccount==self:
			main.window.list.SetSelection(0)
			main.window.on_list_change(None)
		threading.Thread(target=timeline.timelineThread,args=[self,],daemon=True).start()
		if self.prefs.follow_prompt==False:
			q=utils.question("Follow for app updates and support","Would you like to follow @QuinterApp to get app updates and support?")
			if q==1:
				misc.follow_user(self,"@QuinterApp")
			self.prefs.follow_prompt=True

	def start_stream(self):
		if self.stream_listener==None:
			self.stream_listener = streaming.StreamListener(self)
		if self.stream==None or self.stream!=None and self.stream.running==False:
			self.stream = streaming.Stream(auth = self.auth, listener=self.stream_listener,stall_warnings=True)
			self.stream_thread=threading.Thread(target=self.stream.filter, kwargs={"follow":self.stream_listener.users},daemon=True)
			self.stream_thread.start()

	def followers(self,id):
		count=0
		cursor=-1
		followers=[]
		try:
			f=self.api.followers(id=id,cursor=cursor,count=200)
		except TweepError as err:
			utils.handle_error(err,"followers")
			return []
		for i in f[0]:
			followers.append(i)
		cursor=f[1][1]
		count+=1
		while len(f)>0:
			if count>=globals.prefs.user_limit:
				return followers
			try:
				f=self.api.followers(id=id,cursor=cursor,count=200)
				count+=1
			except TweepError as err:
				utils.handle_error(err,"followers")
				return followers
			if len(f[0])==0:
				return followers
			for i in f[0]:
				followers.append(i)
			cursor=f[1][1]
		if cursor<1000:
			return followers
		return followers

	def friends(self,id):
		count=0
		cursor=-1
		followers=[]
		try:
			f=self.api.friends(id=id,cursor=cursor,count=200)
		except TweepError as err:
			utils.handle_error(err,"friends")
			return []
		for i in f[0]:
			followers.append(i)
		count+=1
		cursor=f[1][1]
		while len(f)>0:
			if count>=globals.prefs.user_limit:
				return followers
			try:
				f=self.api.friends(id=id,cursor=cursor,count=200)
				count+=1
			except TweepError as err:
				utils.handle_error(err,"friends")
				return followers
			if len(f[0])==0:
				return followers
			for i in f[0]:
				followers.append(i)
			cursor=f[1][1]
		if cursor<1000:
			return followers
		return followers

	def mutual_following(self):
		followers=self.followers(self.me.id)
		friends=self.friends(self.me.id)
		users=[]
		for i in friends:
			if i in followers:
				users.append(i)
		return users

	def not_following(self):
		followers=self.followers(self.me.id)
		users=[]
		for i in followers:
			if not i.following:
				users.append(i)
		return users

	def not_following_me(self):
		followers=self.followers(self.me.id)
		friends=self.friends(self.me.id)
		users=[]
		for i in friends:
			if not i in followers:
				users.append(i)
		return users

	def tweet(self,text,id=None,**kwargs):
		try:
			if id!=None:
				return self.api.update_status(text,id,**kwargs)
			else:
				return self.api.update_status(text)
			return True
		except Exception as e:
			speak.speak(str(e))
			return False

	def retweet(self,id):
		self.api.retweet(id)

	def quote(self,status,text):
		return self.api.update_status(text, attachment_url = "https://twitter.com/"+status.user.screen_name+"/status/"+str(status.id))

	def like(self,id):
		self.api.create_favorite(id)

	def unlike(self,id):
		self.api.destroy_favorite(id)

	def follow(self,status):
		self.api.create_friendship(status)

	def unfollow(self,status):
		self.api.destroy_friendship(status)

	def block(self,status):
		self.api.create_block(status)

	def unblock(self,status):
		self.api.destroy_block(status)

	def UpdateProfile(self,name,url,location,description):
		self.api.update_profile(name,url,location,description)
