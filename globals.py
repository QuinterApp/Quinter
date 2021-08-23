import sys
import shutil
import platform
from GUI import main, misc
import tweak
import os
import twitter as t
import pickle
import timeline
import utils
import threading
import sound
accounts=[]
prefs=None
users=[]
unknown_users=[]
confpath=""
errors=[]
currentAccount=None
timeline_settings=[]
def  load():
	global timeline_settings
	threading.Thread(target=utils.cfu).start()
	global confpath
	global prefs
	global users
	prefs=tweak.Config(name="Quinter",autosave=True)
	confpath=prefs.user_config_dir
	if platform.system()=="Darwin":
		try:
			f=open(confpath+"/errors.log","a")
			sys.stderr=f
		except:
			pass
	if os.path.exists(confpath+"/sounds/default"):
		shutil.rmtree(confpath+"/sounds/default")
	if not os.path.exists(confpath+"/sounds"):
		os.makedirs(confpath+"/sounds")
	if platform.system()=="Darwin":
		shutil.copytree("/applications/quinter.app/sounds/default",confpath+"/sounds/default")
	else:
		shutil.copytree("sounds/default",confpath+"/sounds/default")
	uaccounts = os.listdir(confpath+"/..")
	for i in uaccounts:
		if "Quinter_account" in i:
			shutil.move(confpath+"/../"+i,confpath+"/"+i.replace("Quinter_",""))
	prefs.timelinecache_version=prefs.get("timelinecache_version",1)
	if prefs.timelinecache_version==1:
		if os.path.exists(confpath+"/timelinecache"):
			os.remove(confpath+"/timelinecache")
		prefs.timelinecache_version=2
	prefs.user_reversed=prefs.get("user_reversed",False)
	prefs.user_limit=prefs.get("user_limit",4)
	prefs.tweetTemplate=prefs.get("tweetTemplate","$user.screen_name$: $text$ $created_at$")
	prefs.messageTemplate=prefs.get("messageTemplate","$sender.screen_name$ to $recipient.screen_name$: $text$ $created_at$")
	prefs.copyTemplate=prefs.get("copyTemplate","$user.name$ ($user.screen_name$): $text$")
	prefs.retweetTemplate=prefs.get("retweetTemplate","Retweeting $user.name$ ($user.screen_name$): $text$")
	prefs.quoteTemplate=prefs.get("quoteTemplate","Quoting $user.name$ ($user.screen_name$): $text$")
	prefs.userTemplate=prefs.get("userTemplate","$name$ ($screen_name$): $followers_count$ followers, $friends_count$ friends, $statuses_count$ tweets. Bio: $description$")
	prefs.accounts=prefs.get("accounts",1)
	prefs.errors=prefs.get("errors",True)
	prefs.streaming=prefs.get("streaming",False)
	prefs.invisible=prefs.get("invisible",False)
	prefs.invisible_sync=prefs.get("invisible_sync",True)
	prefs.update_time=prefs.get("update_time",2)
	prefs.volume=prefs.get("volume",1.0)
	prefs.count=prefs.get("count",200)
	prefs.repeat=prefs.get("repeat",False)
	prefs.demojify=prefs.get("demojify",False)
	prefs.demojify_tweet=prefs.get("demojify_tweet",False)
	prefs.position=prefs.get("position",True)
	prefs.chars_sent=prefs.get("chars_sent",0)
	prefs.tweets_sent=prefs.get("tweets_sent",0)
	prefs.replies_sent=prefs.get("replies_sent",0)
	prefs.quotes_sent=prefs.get("quotes_sent",0)
	prefs.retweets_sent=prefs.get("retweets_sent",0)
	prefs.likes_sent=prefs.get("likes_sent",0)
	prefs.statuses_received=prefs.get("statuses_received",0)
	prefs.ask_dismiss=prefs.get("ask_dismiss",True)
	prefs.reversed=prefs.get("reversed",False)
	prefs.window_shown=prefs.get("window_shown",True)
	prefs.autoOpenSingleURL=prefs.get("autoOpenSingleURL", False)
	prefs.use24HourTime=prefs.get("use24HourTime", False)
	if platform.system()!="Darwin":
		prefs.media_player=prefs.get("media_player","QPlay.exe")
	else:
		prefs.media_player=prefs.get("media_player","/applications/QPlay.app")
	prefs.earcon_audio=prefs.get("earcon_audio",True)
	prefs.earcon_top=prefs.get("earcon_top",False)
	prefs.wrap=prefs.get("wrap",False)
#	prefs.move_amount = prefs.get("move_amount", 20)
	if prefs.invisible:
		main.window.register_keys()
	try:
		f=open(confpath+"/usercache","rb")
		users=pickle.loads(f.read())
		f.close()
	except:
		pass
	if not prefs.user_reversed:
		users=[]
		prefs.user_reversed=True
	load_timeline_settings()
	for i in range(0,prefs.accounts):
		add_session()
	if platform.system()=="Windows" and not os.path.exists("QPlay.exe"):
		q=utils.question("QPlay","It appears you do not have QPlay. It is not needed unless you plan to play audio (such as twitter videos and youtube URL's) without using your browser. Would you like me to set up QPlay for you? Once you hit yes, you can use Quinter normally until QPlay is ready to go.")
		if q==1:
			threading.Thread(target=utils.download_QPlay).start()

def add_session():
	global accounts
	accounts.append(t.twitter(len(accounts)))

def save_users():
	global users
	f=open(confpath+"/usercache","wb")
	f.write(pickle.dumps(users))
	f.close()

def save_messages(account,messages):
	f=open(account.confpath+"/messagecache","wb")
	f.write(pickle.dumps(messages))
	f.close()

def load_messages(account):
	try:
		f=open(account.confpath+"/messagecache","rb")
		messages=pickle.loads(f.read())
		f.close()
		return messages
	except:
		return None

def save_timeline_settings():
	global confpath
	global timeline_settings
	f=open(confpath+"/timelinecache","wb")
	f.write(pickle.dumps(timeline_settings))
	f.close()

def load_timeline_settings():
	global confpath
	global timeline_settings
	try:
		f=open(confpath+"/timelinecache","rb")
		timeline_settings=pickle.loads(f.read())
		f.close()
	except:
		return False

def get_timeline_settings(account_id,name):
	global timeline_settings
	for i in timeline_settings:
		if i.tl==name and i.account_id==account_id:
			return i
	timeline_settings.append(timeline.TimelineSettings(account_id,name))
	return timeline_settings[len(timeline_settings)-1]

def clean_users():
	global users
	users=[]