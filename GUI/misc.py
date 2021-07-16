import math
import os
import platform
import subprocess
import speak
import sound
import utils
from . import chooser, main, tweet, view
import timeline
import globals
from tweepy import TweepError
def reply(account,status):
	NewTweet=tweet.TweetGui(account,"",type="reply",status=status)
	NewTweet.Show()

def quote(account,status):
	NewTweet=tweet.TweetGui(account,type="quote",status=status)
	NewTweet.Show()

def user_timeline(account,status):
	u=utils.get_user_objects_in_tweet(account,status)
	u2=[]
	for i in u:
		u2.append(i.screen_name)
	chooser.chooser(account,"User Timeline","Choose user timeline",u2,"usertimeline")

def user_profile(account,status):
	u=utils.get_user_objects_in_tweet(account,status)
	u2=[]
	for i in u:
		u2.append(i.screen_name)
	chooser.chooser(account,"User Profile","Choose user profile",u2,"profile")

def url_chooser(account,status):
	title="Open URL"
	prompt="Select a URL?"
	type=chooser.ChooseGui.TYPE_URL
	if hasattr(status,"message_create"):
		urlList=utils.find_urls_in_text(status.message_create['message_data']['text'])
	else:
		urlList = utils.find_urls_in_text(status.text)
	if len(urlList) == 1 and globals.prefs.autoOpenSingleURL:
		utils.openURL(urlList[0])
	else:
		chooser.chooser(account,title,prompt,urlList,type)

def follow(account,status):
	u=utils.get_user_objects_in_tweet(account,status)
	u2=[]
	for i in u:
		u2.append(i.screen_name)
	chooser.chooser(account,"Follow User","Follow who?",u2,"follow")

def follow_user(account,username):
	try:
		user=account.follow(username)
		sound.play(globals.currentAccount,"follow")
	except TweepError as error:
		utils.handle_error(error,"Follow "+username)

def unfollow(account,status):
	u=utils.get_user_objects_in_tweet(account,status)
	u2=[]
	for i in u:
		u2.append(i.screen_name)
	chooser.chooser(account,"Unfollow User","Unfollow who?",u2,"unfollow")

def unfollow_user(account,username):
	try:
		user=account.unfollow(username)
		sound.play(globals.currentAccount,"unfollow")
	except TweepError as error:
		utils.handle_error(error,"Unfollow "+username)

def block(account,status):
	u=utils.get_user_objects_in_tweet(account,status)
	u2=[]
	for i in u:
		u2.append(i.screen_name)
	chooser.chooser(account,"Block User","Block who?",u2,"block")

def unblock(account,status):
	u=utils.get_user_objects_in_tweet(account,status)
	u2=[]
	for i in u:
		u2.append(i.screen_name)
	chooser.chooser(account,"Unblock User","Unblock who?",u2,"block")

def mute(account,status):
	u=utils.get_user_objects_in_tweet(account,status)
	u2=[]
	for i in u:
		u2.append(i.screen_name)
	chooser.chooser(account,"Mute User","Mute who?",u2,"mute")

def unmute(account,status):
	u=utils.get_user_objects_in_tweet(account,status)
	u2=[]
	for i in u:
		u2.append(i.screen_name)
	chooser.chooser(account,"Unmute User","Unmute who?",u2,"unmute")

def add_to_list(account,status):
	u=utils.get_user_objects_in_tweet(account,status)
	u2=[]
	for i in u:
		u2.append(i.screen_name)
	chooser.chooser(account,"Add user to list","Add who?",u2,"list")

def remove_from_list(account,status):
	u=utils.get_user_objects_in_tweet(account,status)
	u2=[]
	for i in u:
		u2.append(i.screen_name)
	chooser.chooser(account,"Remove user from list","Remove who?",u2,"listr")

def message(account,status):
	if hasattr(status,"message_create"):
		if status.message_create['sender_id']!=account.me.id:
			user=utils.lookup_user(status.message_create['sender_id']).screen_name
		else:
			user=utils.lookup_user(account,status.message_create['target']['recipient_id']).screen_name
	else:
		user=status.user.screen_name
	message_user(account,user)

def message_user(account,user):
	NewTweet=tweet.TweetGui(account,user,"message")
	NewTweet.Show()

def retweet(account,status):
	try:
		account.retweet(status.id)
		globals.prefs.retweets_sent+=1
		sound.play(globals.currentAccount,"send_retweet")
	except TweepError as error:
		utils.handle_error(error,"retweet")

def like(account,status):
	try:
		if status.favorited:
			account.unlike(status.id)
			status.favorited=False
			sound.play(globals.currentAccount,"unlike")
		else:
			account.like(status.id)
			globals.prefs.likes_sent+=1
			status.favorited=True
			sound.play(globals.currentAccount,"like")
	except TweepError as error:
		utils.handle_error(error,"like tweet")

def followers(account,id=-1):
	if id==-1:
		id=account.me.id
	flw=view.UserViewGui(account,account.followers(id=id),"Followers")
	flw.Show()

def friends(account,id=-1):
	if id==-1:
		id=account.me.id
	flw=view.UserViewGui(account,account.friends(id=id),"Friends")
	flw.Show()

def mutual_following(account):
	if account.me.friends_count>globals.prefs.user_limit*200 or account.me.followers_count>globals.prefs.user_limit*200:
		if account.me.friends_count>account.me.followers_count:
			calls=math.ceil(account.me.friends_count/200)
		else:
			calls=math.ceil(account.me.followers_count/200,0)
		utils.alert("Your set number of user API calls don't allow for this analysis. This means that you have more followers or friends than the API calls would return, thus making this analysis impossible. You would need to perform "+str(calls)+" calls for this analysis to work.","Error")
		return
	flw=view.UserViewGui(account,account.mutual_following(),"Mutual followers")
	flw.Show()

def not_following_me(account):
	if account.me.friends_count>globals.prefs.user_limit*200 or account.me.followers_count>globals.prefs.user_limit*200:
		if account.me.friends_count>account.me.followers_count:
			calls=math.ceil(account.me.friends_count/200)
		else:
			calls=math.ceil(account.me.followers_count/200)
		utils.alert("Your set number of user API calls doesn't allow for this analysis. This means that you have more followers or friends than the API calls would return, thus making this analysis impossible. You would need to perform "+str(calls)+" calls for this analysis to work.","Error")
		return
	flw=view.UserViewGui(account,account.not_following_me(),"Users not following me")
	flw.Show()

def not_following(account):
	flw=view.UserViewGui(account,account.not_following(),"users I don't follow")
	flw.Show()

def havent_tweeted(account):
	flw=view.UserViewGui(account,account.havent_tweeted(),"users who haven't tweeted recently")
	flw.Show()

def user_timeline_user(account,username,focus=True):
	if username in account.prefs.user_timelines and focus==True:
		utils.alert("You already have a timeline for this user open.","Error")
		return False
	if len(account.prefs.user_timelines)>=8:
		utils.alert("You cannot have this many user timelines open! Please consider using a list instead.","Error")
		return False
	user=utils.lookup_user_name(account,username)
	if user!=-1:
		if focus==False:
			account.timelines.append(timeline.timeline(account,name=username+"'s Timeline",type="user",data=username,user=user,silent=True))
		else:
			account.timelines.append(timeline.timeline(account,name=username+"'s Timeline",type="user",data=username,user=user))
		if username not in account.prefs.user_timelines:
			account.prefs.user_timelines.append(username)
		main.window.refreshTimelines()
		if focus==True:
			account.currentIndex=len(account.timelines)-1
			main.window.list.SetSelection(len(account.timelines)-1)
			main.window.on_list_change(None)
		return True

def search(account,q,focus=True):
	if focus==False:
		account.timelines.append(timeline.timeline(account,name=q+" Search",type="search",data=q,silent=True))
	else:
		account.timelines.append(timeline.timeline(account,name=q+" Search",type="search",data=q))
	if q not in account.prefs.search_timelines:
		account.prefs.search_timelines.append(q)
	main.window.refreshTimelines()
	if focus==True:
		account.currentIndex=len(account.timelines)-1
		main.window.list.SetSelection(len(account.timelines)-1)
		main.window.on_list_change(None)

def user_search(account,q):
	users=account.api.search_users(q,page=1)
	u=view.UserViewGui(account,users,"User search for "+q)
	u.Show()

def list_timeline(account,n, q,focus=True):
	if q in account.prefs.list_timelines and focus==True:
		utils.alert("You already have a timeline for this list open!","Error")
		return
	if len(account.prefs.list_timelines)>=8:
		utils.alert("You cannot have this many list timelines open!","Error")
		return
	if focus==False:
		account.timelines.append(timeline.timeline(account,name=n+" List",type="list",data=q,silent=True))
	else:
		account.timelines.append(timeline.timeline(account,name=n+" List",type="list",data=q))
	if q not in account.prefs.list_timelines:
		account.prefs.list_timelines.append(q)
	main.window.refreshTimelines()
	if focus==True:
		account.currentIndex=len(account.timelines)-1
		main.window.list.SetSelection(len(account.timelines)-1)
		main.window.on_list_change(None)

def next_in_thread(account):
	status=account.currentTimeline.statuses[account.currentTimeline.index]
	if hasattr(status,"in_reply_to_status_id") and status.in_reply_to_status_id!=None:
		newindex=utils.find_status(account.currentTimeline,status.in_reply_to_status_id)
		if newindex>-1:
			account.currentTimeline.index=newindex
			main.window.list2.SetSelection(newindex)

def previous_in_thread(account):
	newindex=-1
	newindex=utils.find_reply(account.currentTimeline,account.currentTimeline.statuses[account.currentTimeline.index].id)
	if newindex>-1:
		account.currentTimeline.index=newindex
		main.window.list2.SetSelection(newindex)

def previous_from_user(account):
	newindex=-1
	oldindex=account.currentTimeline.index
	user=account.currentTimeline.statuses[account.currentTimeline.index].user
	newindex2=0
	for i in account.currentTimeline.statuses:
		if i.user.id==user.id:
			newindex=newindex2
		newindex2+=1
		if newindex2>=oldindex:
			break

	if newindex>-1:
		account.currentTimeline.index=newindex
		main.window.list2.SetSelection(newindex)

def next_from_user(account):
	newindex=-1
	oldindex=account.currentTimeline.index
	status=account.currentTimeline.statuses[account.currentTimeline.index]
	user=account.currentTimeline.statuses[account.currentTimeline.index].user
	newindex2=0
	for i in account.currentTimeline.statuses:
		if i!=status and i.user.id==user.id and newindex2>=oldindex:
			newindex=newindex2
			break
		newindex2+=1

	if newindex>-1:
		account.currentTimeline.index=newindex
		main.window.list2.SetSelection(newindex)

def delete(account,status):
	try:
		account.api.destroy_status(status.id)
		account.currentTimeline.statuses.remove(status)
		main.window.list2.Delete(account.currentTimeline.index)
		sound.play(globals.currentAccount,"delete")
		main.window.list2.SetSelection(account.currentTimeline.index)
	except TweepError as error:
		utils.handle_error(error,"Delete tweet")

def load_conversation(account,status):
	account.timelines.append(timeline.timeline(account,name="Conversation with "+status.user.screen_name,type="conversation",data=status.user.screen_name,status=status))
	main.window.refreshTimelines()
	main.window.list.SetSelection(len(account.timelines)-1)
	account.currentIndex=len(account.timelines)-1
	main.window.on_list_change(None)

def play(status):
	if sound.player!=None and sound.player.is_playing==True:
		speak.speak("Stopped")
		sound.stop()
		return
	if hasattr(status,"message_create"):
		urls=utils.find_urls_in_text(status.message_create['message_data']['text'])
	else:
		urls=utils.find_urls_in_tweet(status)
	try:
		speak.speak("Retrieving URL...")
		audio=sound.get_audio_urls(urls)[0]
		a=audio['func'](audio['url'])
		sound.play_url(a)
	except:
		speak.speak("No audio.")

def play_external(status):
	if hasattr(status,"message_create"):
		urls=utils.find_urls_in_text(status.message_create['message_data']['text'])
	else:
		urls=utils.find_urls_in_tweet(status)
	if globals.prefs.media_player!="":
		if len(urls)>0:
			speak.speak("Opening media...")
			audio=sound.get_media_urls(urls)[0]
			if platform.system()!="Darwin":
				subprocess.run([globals.prefs.media_player, audio['url']])
			else:
				os.system("open -a "+globals.prefs.media_player+" --args "+audio['url'])
		else:
			speak.speak("No audio")
	else:
		speak.speak("No external media player setup.")
