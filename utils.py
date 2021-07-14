import sys
import html
import platform
import json
import datetime
import time
import re
import globals
import speak
import wx
import requests
import webbrowser
import application
import sound
import os

url_re=re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?]))")
url_re2=re.compile("(?:\w+://|www\.)[^ ,.?!#%=+][^ ]*")
bad_chars="'\\.,[](){}:;\""

def process_tweet(s,return_only_text=False,template=""):
	if hasattr(s,"message_create"):
		print("We don't support this in this function, are you drunk?")
		return
	if hasattr(s,"extended_tweet") and "full_text" in s.extended_tweet:
		text=html.unescape(s.extended_tweet['full_text'])
	else:
		if hasattr(s,"full_text"):
			text=html.unescape(s.full_text)
		else:
			text=html.unescape(s.text)
	if hasattr(s,"entities")!=False:
		if "urls" in s.entities!=False:
			for url in s.entities['urls']:
				try:
					text=text.replace(url['url'],url['expanded_url'])
					if url['expanded_url'] not in text:
						text+=" "+url['expanded_url']
				except IndexError:
					pass

		if hasattr(s,"extended_tweet") and "urls" in s.extended_tweet['entities']:
			for url in s.extended_tweet['entities']['urls']:
				try:
					text=text.replace(url['url'],url['expanded_url'])
					if url['expanded_url'] not in text:
						text+=" "+url['expanded_url']
				except IndexError:
					pass

	if hasattr(s,"retweeted_status")!=False:
		qs=s.retweeted_status
		text=process_tweet(qs,False,globals.prefs.retweetTemplate)

	urls=find_urls_in_text(text)
	for url in range(0,len(urls)):
		if "twitter.com/i/web" in urls[url]:
			text=text.replace(urls[url],"")
	if hasattr(s,"quoted_status")!=False:
		qs=s.quoted_status
		urls=find_urls_in_text(text)
		for url in range(0,len(urls)):
			if "twitter.com" in urls[url]:
				text=text.replace(urls[url],"")
				text+=process_tweet(qs,False,globals.prefs.quoteTemplate)
		if not process_tweet(qs,False,globals.prefs.quoteTemplate) in text:
			text+=process_tweet(qs,False,globals.prefs.quoteTemplate)

	s.text=text
	if not return_only_text:
		return template_to_string(s,template)
	else:
		return text

def process_message(s, return_text=False):
	text=html.unescape(s.message_create['message_data']['text'])
	if "entities" in s.message_create['message_data']!=False:
		if "urls" in s.message_create["message_data"]["entities"]!=False:
			urls=find_urls_in_text(text)
			for url in range(0,len(urls)):
				try:
					text=text.replace(urls[url],s.message_create["message_data"]["entities"]['urls'][url]['expanded_url'])
				except IndexError:
					pass

	s.message_create["message_data"]["text"]=text
	if not return_text:
		return message_template_to_string(s)
	else:
		return s.message_create['message_data']['text']

def find_urls_in_text(text):
	return [s.strip(bad_chars) for s in url_re2.findall(text)]

def find_urls_in_tweet(s):
	urls=[]
	if hasattr(s,"entities"):
		if s.entities['urls']!=[]:
			for i in s.entities['urls']:
				urls.append(i['expanded_url'])
		if "media" in s.entities:
			for i in s.entities['media']:
				urls.append(i['expanded_url'])
	return urls

def template_to_string(s,template=""):
	if template=="":
		template=globals.prefs.tweetTemplate
	temp=template.split(" ")
	for i in range(len(temp)):
		if "$" in temp[i]:
			t=temp[i].split("$")
			r=t[1]
			if "." in r:
				q=r.split(".")
				o=q[0]
				p=q[1]

				if hasattr(s,o) and hasattr(getattr(s,o),p):
					try:
						if (o=="name" or p=="name") and globals.prefs.demojify:
							deEmojify=True
						else:
							deEmojify=False
						f1=getattr(s,o)
						if deEmojify:
							demojied=demojify(getattr(f1,p))
							if demojied=="":
								template=template.replace("$"+t[1]+"$",getattr(f1,"screen_name"))
							else:
								template=template.replace("$"+t[1]+"$",demojied)
						else:
							template=template.replace("$"+t[1]+"$",getattr(f1,p))
					except:
						try:
							f1=getattr(s,o)
							template=template.replace("$"+t[1]+"$",str(getattr(f1,p)))
						except Exception as e:
							print(e)

			else:
				if hasattr(s,t[1]):
					try:
						if t[1]=="name" and globals.prefs.demojify or t[1]=="text" and globals.prefs.demojify_tweet:
							deEmojify=True
						else:
							deEmojify=False
						if deEmojify:
							demojied=demojify(getattr(s,t[1]))
							if demojied=="" and t[1]=="name":
								template=template.replace("$"+t[1]+"$",getattr(s,"screen_name"))
							else:
								template=template.replace("$"+t[1]+"$",demojied)
						else:
							if t[1]=="created_at":
								template=template.replace("$"+t[1]+"$",parse_date(getattr(s,t[1])))
							else:
								template=template.replace("$"+t[1]+"$",getattr(s,t[1]))
					except:
						try:
							template=template.replace("$"+t[1]+"$",str(getattr(s,t[1])))
						except Exception as e:
							print(e)
	return template

def message_template_to_string(s):
	s2={}
	template=globals.prefs.messageTemplate
	if "sender" not in s2:
		s2["sender"]=lookup_user(s.message_create['sender_id'])
	if "recipient" not in s2:
		s2["recipient"]=lookup_user(s.message_create['target']['recipient_id'])
	if globals.prefs.demojify:
		if s2['sender']!=None:
			s2['sender'].name=demojify(s2['sender'].name)
			if s2['sender'].name=="":
				s2['sender'].name=s2['sender'].screen_name
		if s2['recipient']!=None:
			s2['recipient.name']=demojify(s2['recipient'].name)
			if s2['recipient'].name=="":
				s2['recipient'].name=s2['recipient'].screen_name
	if "created_at" not in s2:
		s2['created_at']=parse_date(datetime.datetime.fromtimestamp(int(s.created_timestamp)/1000),False)
	temp=template.split(" ")
	for i in range(len(temp)):
		if "$" in temp[i]:
			t=temp[i].split("$")
			r=t[1]
			if "." in r:
				q=r.split(".")
				o=q[0]
				p=q[1]

				if o in s2 and type(s2[o])==dict and p in s2[o]:
					try:
						template=template.replace("$"+t[1]+"$",s2[o][p])
					except Exception as e:
						print(e)

				elif o in s2 and hasattr(s2[o],p):
					try:
						attribute=getattr(s2[o],p)
						template=template.replace("$"+t[1]+"$",attribute)
					except Exception as e:
						print(e)

				elif o in s.message_create and p in s.message_create[o]:
					try:
						template=template.replace("$"+t[1]+"$",s.message_create[o][p])
					except Exception as e:
						print(e)

				elif o in s.message_create['message_data'] and p in s.message_create['message_data'][o]:
					try:
						if t[1]=="text" and globals.prefs.demojify_tweet:
							demojified=demojify(s.message_create["message_data"][o][p])
							template=template.replace("$"+t[1]+"$",demojified)
						else:
							template=template.replace("$"+t[1]+"$",s.message_create['message_data'][o][p])
					except Exception as e:
						print(e)

			else:
				if t[1] in s2:
					try:
						template=template.replace("$"+t[1]+"$",s2[t[1]])
					except Exception as e:
						print(e)
				elif t[1] in s.message_create:
					try:
						template=template.replace("$"+t[1]+"$",s.message_create[t[1]])
					except Exception as e:
						print(e)
				elif t[1] in s.message_create['message_data']:
					try:
						if t[1]=="text" and globals.prefs.demojify_tweet:
							demojified=demojify(s.message_create["message_data"][t[1]])
							template=template.replace("$"+t[1]+"$",demojified)
						else:
							template=template.replace("$"+t[1]+"$",s.message_create["message_data"][t[1]])
					except Exception as e:
						print(e)
	return template

def get_users_in_tweet(account,s):
	new=""

	if hasattr(s,"quoted_status")!=False and s.quoted_status.user.id!=account.me.id:
		s.text+=" "+s.quoted_status.user.screen_name
	if hasattr(s,"retweeted_status")!=False and s.retweeted_status.user.id!=account.me.id:
		s.text+=" "+s.retweeted_status.user.screen_name

	if s.user.screen_name!=account.me.screen_name:
		new=s.user.screen_name
	if hasattr(s,"entities") and "user_mentions" in s.entities:
		weew=s.entities['user_mentions']
		for i in range(0,len(weew)):
			if account.me.screen_name!=weew[i]['screen_name']:
				new+=" "+weew[i]['screen_name']
	return new

def user(s):
	if s.has_key('user'):
		return s['user']['screen_name']
	else:
		return s['sender']['screen_name']

def dict_match(d1, d2):
	for i in d2:
		if not i in d1:
			d1[i]=d2[i]
	return d1

def class_match(d1, d2):
	names1=[p for p in dir(d1) if isinstance(getattr(d1,p),property)]
	names2=[p for p in dir(d2) if isinstance(getattr(d2,p),property)]
	for i in names2:
		if not i in names1:
			setattr(d1,i,getattr(d2,i,None))
	return d1

def parse_date(date,convert=True):
	ti=datetime.datetime.now()
	dst=time.localtime().tm_isdst
	if dst==1:
		tz=time.altzone
	else:
		tz=time.timezone
	if convert:
		try:
			date+=datetime.timedelta(seconds=0-tz)
		except:
			pass
	returnstring=""

	try:
		if date.year==ti.year:
			if date.day==ti.day and date.month==ti.month:
				returnstring=""
			else:
				returnstring=date.strftime("%m/%d/%Y, ")
		else:
			returnstring=date.strftime("%m/%d/%Y, ")

		if returnstring!="":
			returnstring+=date.strftime("%I:%M:%S %p")
		else:
			returnstring=date.strftime("%I:%M:%S %p")
	except:
		pass
	return returnstring

def isDuplicate(status,statuses):
	for i in statuses:
		if i.id==status.id:
			return True
	return False


class dict_obj:
	def __init__(self, dict1):
		self.__dict__.update(dict1)

def dict2obj(dict1):
	return json.loads(json.dumps(dict1), object_hook=dict_obj)

def add_users(status):
	if status.user in globals.users:
		try:
			globals.users.remove(status.user)
		except:
			pass
	globals.users.insert(0,status.user)
	if hasattr(status,"quoted_status")!=False:
		if status.quoted_status.user in globals.users:
			try:
				globals.users.remove(status.quoted_status.user)
			except:
				pass
		globals.users.insert(0,status.quoted_status.user)
	if hasattr(status,"retweeted_status")!=False:
		if status.retweeted_status.user in globals.users:
			try:
				globals.users.remove(status.retweeted_status.user)
			except:
				pass
		globals.users.insert(0,status.retweeted_status.user)

def lookup_user(id):
	for i in globals.users:
		if int(i.id)==int(id):
			return i
	globals.unknown_users.append(id)
	print(id+" not found. Added to cue of "+str(len(globals.unknown_users))+" users.")
	return None

def lookup_user_name(account,name,use_api=True):
	for i in globals.users:
		if i.screen_name.lower()==name.lower():
			return i
	if not use_api:
		return -1
	try:
		user=account.api.lookup_users(screen_names=[name])[0]
		if user in globals.users:
			try:
				globals.users.remove(user)
			except:
				pass
		globals.users.insert(0,user)
		return user
	except:
		return -1

def get_user_objects_in_tweet(account,status,exclude_self=False,exclude_orig=False):
	users=[]
	if hasattr(status,"message_create"):
		users.append(lookup_user(status.message_create['sender_id']))
		users.append(lookup_user(status.message_create['target']['recipient_id']))
		return users
	if status.user not in users and not exclude_orig:
		users.append(status.user)
	if hasattr(status,"quoted_status")!=False and status.quoted_status.user not in users:
		users.append(status.quoted_status.user)
	if hasattr(status,"retweeted_status")!=False and status.retweeted_status.user not in users:
		users.append(status.retweeted_status.user)
	if hasattr(status,"entities") and "user_mentions" in status.entities:
		weew=status.entities['user_mentions']
		for i in range(0,len(weew)):
			if (account.me.screen_name!=weew[i]['screen_name'] and exclude_self or not exclude_self):
				username=weew[i]['screen_name']
				un=lookup_user_name(account,username)
				if un!=-1:
					users.append(un)
	for i in users:
		if i.id==account.me.id and exclude_self:
			users.remove(i)

	return users

def speak_user(account,users):
	text=""
	for i in users:
		user=lookup_user_name(account,i)
		if user!=None and user!=-1:
			text+=". "+template_to_string(user,globals.prefs.userTemplate)
		text=text.rstrip(".")
	text=text.lstrip(".")
	speak.speak(str(len(users))+" users: "+text)

def lookup_status(account,id):
	for i in account.timelines:
		for i2 in i.statuses:
			if i2.id==id:
				return i2
	s=account.api.get_status(id,tweet_mode="extended")
	return s

def find_status(tl,id):
	index=0
	for i in tl.statuses:
		if i.id==id:
			return index
		index+=1

	return -1

def find_reply(tl, id):
	index=0
	for i in tl.statuses:
		if hasattr(i,"in_reply_to_status_id") and i.in_reply_to_status_id==id:
			return index
		index+=1

	return -1

def speak_reply(account,status):
	if hasattr(status,"in_reply_to_status_id") and status.in_reply_to_status_id!=None:
		status=lookup_status(account,status.in_reply_to_status_id)
		status=process_tweet(status)
		speak.speak(status)
	else:
		speak.speak("Not a reply.")

def question(title,text, parent=None):
	dlg=wx.MessageDialog(parent,text,title,wx.YES_NO | wx.ICON_QUESTION)
	result=dlg.ShowModal()
	dlg.Destroy()
	if result== wx.ID_YES:
		return 1
	else:
		return 2

def warn(message, caption = 'Warning!', parent=None):
	dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
	dlg.ShowModal()
	dlg.Destroy()

def alert(message, caption = "", parent=None):
	dlg = wx.MessageDialog(parent, message, caption, wx.OK)
	dlg.ShowModal()
	dlg.Destroy()

def cfu(silent=True):
	try:
		latest=requests.get("http://masonasons.me/projects/"+application.shortname+"version.txt",timeout=5).text
		if application.version<latest:
			ud=question("Update available: "+latest,"There is an update available. Your version: "+application.version+". Latest version: "+latest+". Do you want to open the direct download link?")
			if ud==1:
				if platform.system()=="Darwin":
					webbrowser.open("http://masonasons.me/softs/QuinterMac.zip")
					sys.exit()
				else:
					webbrowser.open("http://masonasons.me/softs/Quinter.zip")
		else:
			if not silent:
				alert("No updates available! The latest version of the program is "+latest,"No update available")
	except:
		pass

def demojify(text):
#    regrex_pattern = re.compile(pattern = "["
#        u"\U0001F600-\U0001F64F"  # emoticons
#        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#        u"\U0001F680-\U0001F6FF"  # transport & map symbols
#        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                           "]+", flags = re.UNICODE)
#    return regrex_pattern.sub(r'',text)
	text=text.encode("ascii","ignore")
	text=text.decode()
	return text

def handle_error(error,name="Unknown"):
	if hasattr(error,"response") and error.response!=None and error.response!="":
		if "429" in str(error):
			globals.errors.append("Error in "+name+": "+error.response.text)
			return
		speak.speak("Error in "+name+": "+error.response.text)
		globals.errors.append("Error in "+name+": "+error.response.text)
		sound.play(globals.currentAccount,"error")
	else:
		if error.reason!="" and error.reason!=None:
			speak.speak("Error in "+name+": "+error.reason)
			globals.errors.append("Error in "+name+": "+error.reason)
			sound.play(globals.currentAccount,"error")

def get_account(id):
	for i in globals.accounts:
		if i.me.id==id:
			return i
	return -1

def openURL(url):
	if platform.system()!="Darwin":
		webbrowser.open(url)
	else:
		os.system(f"open {url}")
