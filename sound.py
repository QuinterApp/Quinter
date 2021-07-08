import os
import sound_lib
from sound_lib import stream
from sound_lib import output as o
import globals
import speak

out = o.Output()
handle = None

import re
import youtube_dl
ydl=None
player=None
def ydl_url(url):
	global ydl
	if ydl is None:
		ydl = youtube_dl.YoutubeDL(params=dict(outtmpl = u"%(title)s [%(extractor)s '%(id)s].%(ext)s", quiet=True, ))
		ydl.add_default_info_extractors()

	info = ydl.extract_info(url, download=False, process=False)
	print(info['formats'][-1]['url'])
	return info['formats'][-1]['url']

def return_url(url):
	return url

audio_matchlist = [{"match": r"https://sndup.net/[a-zA-Z0-9]+/[ad]$", "func":return_url},
	{"match": r"^http:\/\/\S+(\/\S+)*(\/)?\.(mp3|m4a|ogg|opus|flac)$", "func":return_url},
	{"match": r"^https:\/\/\S+(\/\S+)*(\/)?\.(mp3|m4a|ogg|opus|flac)$", "func":return_url},
	{"match": r"^http:\/\/\S+:[+-]?[1-9]\d*|0(\/\S+)*(\/)?$", "func":return_url},
	{"match": r"^https:\/\/\S+:[+-]?[1-9]\d*|0(\/\S+)*(\/)?$", "func":return_url},
	{"match": r"https?://twitter.com/.+/status/.+/video/.+", "func":ydl_url},
#	{"match": r"https?://vm.tiktok.com/.+", "func":ydl_url},
	{"match": r"https?://soundcloud.com/.+", "func":ydl_url},
	{"match": r"https?://t.co/.", "func":ydl_url},
	{"match": r"^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$", "func":ydl_url}
	]

media_matchlist = [{"match": r"https://sndup.net/[a-zA-Z0-9]+/[ad]$", "func":return_url},
	{"match": r"^http:\/\/\S+(\/\S+)*(\/)?\.(mp3|m4a|ogg|opus|flac)$", "func":return_url},
	{"match": r"^https:\/\/\S+(\/\S+)*(\/)?\.(mp3|m4a|ogg|opus|flac)$", "func":return_url},
	{"match": r"^http:\/\/\S+:[+-]?[1-9]\d*|0(\/\S+)*(\/)?$", "func":return_url},
	{"match": r"^https:\/\/\S+:[+-]?[1-9]\d*|0(\/\S+)*(\/)?$", "func":return_url},
	{"match": r"https?://twitter.com/.+/status/.+/video/.+", "func":ydl_url},
	{"match": r"https?://twitch.tv/.", "func":ydl_url},
	{"match": r"http?://twitch.tv/.", "func":ydl_url},
	{"match": r"https?://vm.tiktok.com/.+", "func":ydl_url},
	{"match": r"https?://soundcloud.com/.+", "func":ydl_url},
	{"match": r"https?://t.co/.", "func":ydl_url},
	{"match": r"^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$", "func":ydl_url}
	]

def get_audio_urls(urls):
	result = []
	for u in urls:
		for service in audio_matchlist:
			if re.match(service['match'], u.lower()) != None:
				result.append({"url":u, "func":service['func']})
	return result

def get_media_urls(urls):
	result = []
	for u in urls:
		for service in media_matchlist:
			if re.match(service['match'], u.lower()) != None:
				result.append({"url":u, "func":service['func']})
	return result

def play(account, filename, pack="", wait=False):
	global handle
	if handle != None:
		try:
			handle.stop()
		except sound_lib.main.BassError:
			pass
		try:
			handle.free()
		except sound_lib.main.BassError:
			pass
	if os.path.exists(globals.confpath+"/sounds/" + account.prefs.soundpack + "/" + filename + ".ogg"):
		path=globals.confpath+"/sounds/" + account.prefs.soundpack + "/" + filename + ".ogg"
	elif os.path.exists("sounds/"+account.prefs.soundpack+"/"+filename + ".ogg"):
		path="sounds/" + account.prefs.soundpack + "/" + filename + ".ogg"
	elif os.path.exists(globals.confpath+"/sounds/default/" + filename + ".ogg"):
		path=globals.confpath+"/sounds/default/" + filename + ".ogg"
	elif os.path.exists("sounds/default/"+filename + ".ogg"):
		path="sounds/default/" + filename + ".ogg"
	else:
		return
	try:
		handle = stream.FileStream(file=path)
		handle.pan=account.prefs.soundpan
		handle.volume = globals.prefs.volume
		handle.looping = False
		if wait:
			handle.play_blocking()
		else:
			handle.play()
	except sound_lib.main.BassError:
		pass

def play_url(url):
	global player
	if player!=None and player.is_playing==True:
		speak.speak("Stopped")
		stop()
		return
	try:
		speak.speak("Playing")
		player = stream.URLStream(url)
		player.volume = globals.prefs.volume
		player.play()
		return True
	except:
		speak.speak("Error while playing "+url)
		return False

def stop():
	global player
	if player == None: return False
	player.stop()
	player.free()
	player = None
	return True