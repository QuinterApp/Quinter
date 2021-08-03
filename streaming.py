# -*- coding: utf-8 -*-
from tweepy.models import Status
import tweepy
from GUI import main
import globals

import time
import speak

import sys
import six
import requests
import urllib3
import ssl
import utils

from tweepy  import TweepError
class StreamListener(tweepy.StreamListener):

	def __init__(self, account, *args, **kwargs):
		super(StreamListener, self).__init__(*args, **kwargs)
		self.account = account
		try:
			self.users = [str(id) for id in self.account.api.friends_ids()]
		except TweepError as e:
			utils.handle_error(e)
			self.users=[]
		muted=self.account.api.mutes()
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
		print("Streaming started for "+self.account.me.screen_name)

	def on_exception(self, ex):
		speak.speak("Exception in stream for "+self.account.me.screen_name)
		print(str(ex))

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

class Stream(tweepy.Stream):

    def _run(self):
        # Authenticate
        url = "https://%s%s" % (self.host, self.url)

        # Connect and process the stream
        error_counter = 0
        resp = None
        exc_info = None
        while self.running:
            if self.retry_count is not None:
                if error_counter > self.retry_count:
                    # quit if error count greater than retry count
                    break
            try:
                auth = self.auth.apply_auth()
                resp = self.session.request('POST',
                                            url,
                                            data=self.body,
                                            timeout=self.timeout,
                                            stream=True,
                                            auth=auth,
                                            verify=self.verify,
                                            proxies = self.proxies)
                if resp.status_code != 200:
                    if self.listener.on_error(resp.status_code) is False:
                        break
                    error_counter += 1
                    if resp.status_code == 420:
                        self.retry_time = max(self.retry_420_start,
                                              self.retry_time)
                    time.sleep(self.retry_time)
                    self.retry_time = min(self.retry_time * 2,
                                          self.retry_time_cap)
                else:
                    error_counter = 0
                    self.retry_time = self.retry_time_start
                    self.snooze_time = self.snooze_time_step
                    self.listener.on_connect()
                    self._read_loop(resp)
            except (requests.ConnectionError, requests.Timeout, ssl.SSLError, urllib3.exceptions.ReadTimeoutError, urllib3.exceptions.ProtocolError) as exc:
                # This is still necessary, as a SSLError can actually be
                # thrown when using Requests
                # If it's not time out treat it like any other exception
                if isinstance(exc, ssl.SSLError):
                    if not (exc.args and 'timed out' in str(exc.args[0])):
                        exc_info = sys.exc_info()
                        break
                if self.listener.on_timeout() is False:
                    break
                if self.running is False:
                    break
                time.sleep(self.snooze_time)
                self.snooze_time = min(self.snooze_time + self.snooze_time_step,
                                       self.snooze_time_cap)
            except Exception as exc:
                exc_info = sys.exc_info()
                # any other exception is fatal, so kill loop
                break

        # cleanup
        self.running = False
        if resp:
            resp.close()

        self.new_session()

        if exc_info:
            # call a handler first so that the exception can be logged.
            self.listener.on_exception(exc_info[1])
            six.reraise(*exc_info)