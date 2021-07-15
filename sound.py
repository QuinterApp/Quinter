import os
import sound_lib
from sound_lib import stream
from sound_lib import output as o
import globals
import speak

out = o.Output()
handle = None

import re

def return_url(url):
	return url

media_matchlist = [{"match": r"https://sndup.net/[a-zA-Z0-9]+/[ad]$", "func":return_url},
	{"match": r"^http:\/\/\S+(\/\S+)*(\/)?\.(mp3|m4a|ogg|opus|flac)$", "func":return_url},
	{"match": r"^https:\/\/\S+(\/\S+)*(\/)?\.(mp3|m4a|ogg|opus|flac)$", "func":return_url},
	{"match": r"^http:\/\/\S+:[+-]?[1-9]\d*|0(\/\S+)*(\/)?$", "func":return_url},
	{"match": r"^https:\/\/\S+:[+-]?[1-9]\d*|0(\/\S+)*(\/)?$", "func":return_url},
	{"match": r"https?://twitter.com/.+/status/.+/video/.+", "func":return_url},
	{"match": r"https?://twitch.tv/.", "func":return_url},
	{"match": r"http?://twitch.tv/.", "func":return_url},
	{"match": r"https?://vm.tiktok.com/.+", "func":return_url},
	{"match": r"https?://soundcloud.com/.+", "func":return_url},
	{"match": r"https?://t.co/.", "func":return_url},
	{"match": r"^(?:https?:\/\/)?(?:m\.|www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$", "func":return_url}
	]

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
