# -*- coding: utf-8 -*-
from tweepy.models import Status
import tweepy
from GUI import main
import globals

import time
import speak

import sys
import utils

from tweepy  import TweepyException
class StreamListener(tweepy.Stream):

	def __init__(self, account, *args, **kwargs):
		super(StreamListener, self).__init__(*args, **kwargs)
		self.account = account
		try:
			self.users = [str(id) for id in self.account.api.get_friend_ids()]
		except TweepyException as e:
			utils.handle_error(e)
			self.users=[]
		muted=self.account.api.get_mutes()
		for i in muted:
			if i.id_str in self.users:
				self.users.remove(i.id_str)
		self.users.append(str(self.account.me.id))
		self.home_users=[]
		for i in self.users:
			self.home_users.append(i)
		for i in self.account.timelines:
			if i.type=="user" and not i.user.protected and i.user.id_str not in self.users:
				self.users.append(i.user.id_str)

	def on_connect(self):
		speak.speak("Streaming started for "+self.account.me.screen_name)

	def on_exception(self, ex):
		speak.speak("Exception in stream for "+self.account.me.screen_name)

	def on_status(self, status):
		""" Checks data arriving as a tweet. """
		send_home=True
		if status.in_reply_to_user_id_str != None and status.in_reply_to_user_id_str not in self.users:
			send_home=False
		if status.user.id_str not in self.home_users:
			send_home=False
		if hasattr(status, "retweeted_status"):
			if hasattr(status.retweeted_status, "extended_tweet"):
				status.retweeted_status._json = {**status.retweeted_status._json, **status.retweeted_status._json["extended_tweet"]}
			status.retweeted_status=Status().parse(None,status.retweeted_status._json)
		if hasattr(status, "quoted_status"):
			if hasattr(status.quoted_status, "extended_tweet"):
				status.quoted_status._json = {**status.quoted_status._json, **status.quoted_status._json["extended_tweet"]}
			status.quoted_status=Status().parse(None,status.quoted_status._json)
		if status.truncated:
			status._json = {**status._json, **status._json["extended_tweet"]}
		status=Status().parse(None,status._json)
		if status.user.id_str in self.users:
			if send_home:
				self.account.timelines[0].load(items=[status])
			if status.user.screen_name!=self.account.me.screen_name:
				users=utils.get_user_objects_in_tweet(self.account,status)
				for i in users:
					if i.screen_name==self.account.me.screen_name:
						self.account.timelines[1].load(items=[status])
			if status.user.id==self.account.me.id:
				self.account.timelines[4].load(items=[status])
			for i in self.account.timelines:
				if i.type=="list" and status.user.id in i.members:
					i.load(items=[status])
				if i.type=="user" and status.user.screen_name==i.data:
					i.load(items=[status])