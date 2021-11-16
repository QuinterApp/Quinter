import globals
from . import main
import speak
import utils
import sound
def register_key(key,name,reg=True):
	if hasattr(main.window,name):
		try:
			if reg:
				main.window.handler.register_key(key,getattr(main.window,name))
			else:
				main.window.handler.unregister_key(key,getattr(main.window,name))
			return True
		except:
			return False
	if hasattr(main.window,"on"+name):
		try:
			if reg:
				main.window.handler.register_key(key,getattr(main.window,"on"+name))
			else:
				main.window.handler.unregister_key(key,getattr(main.window,"on"+name))
			return True
		except:
			return False
	if hasattr(main.window,"On"+name):
		try:
			if reg:
				main.window.handler.register_key(key,getattr(main.window,"On"+name))
			else:
				main.window.handler.unregister_key(key,getattr(main.window,"On"+name))
			return True
		except:
			return False
	if hasattr(inv,name):
		try:
			if reg:
				main.window.handler.register_key(key,getattr(inv,name))
			else:
				main.window.handler.unregister_key(key,getattr(inv,name))
			return True
		except:
			return False

class invisible_interface(object):
	def focus_tl(self,sync=False):
		globals.currentAccount.currentTimeline=globals.currentAccount.list_timelines()[globals.currentAccount.currentIndex]
		if not sync and globals.prefs.invisible_sync or sync:
			main.window.list.SetSelection(globals.currentAccount.currentIndex)
			main.window.on_list_change(None)
		extratext=""
		if globals.prefs.position:
			if len(globals.currentAccount.currentTimeline.statuses)==0:
				extratext+="Empty"
			else:
				extratext+=str(globals.currentAccount.currentTimeline.index+1)+" of "+str(len(globals.currentAccount.currentTimeline.statuses))
		if globals.currentAccount.currentTimeline.read:
			extratext+=", Autoread"
		if globals.currentAccount.currentTimeline.mute:
			extratext+=", muted"
		speak.speak(globals.currentAccount.currentTimeline.name+". "+extratext,True)
		if not globals.prefs.invisible_sync and not sync:
			main.window.play_earcon()

	def focus_tl_item(self):
		if globals.prefs.invisible_sync:
			main.window.list2.SetSelection(globals.currentAccount.currentTimeline.index)
			main.window.on_list2_change(None)
		else:
			if globals.prefs.earcon_audio and len(sound.get_media_urls(utils.find_urls_in_tweet(globals.currentAccount.currentTimeline.statuses[globals.currentAccount.currentTimeline.index]))) > 0:
				sound.play(globals.currentAccount,"media")
		self.speak_item()

	def speak_item(self):
		if globals.currentAccount.currentTimeline.type!="messages":
			speak.speak(utils.process_tweet(globals.currentAccount.currentTimeline.statuses[globals.currentAccount.currentTimeline.index]),True)
		else:
			speak.speak(utils.process_message(globals.currentAccount.currentTimeline.statuses[globals.currentAccount.currentTimeline.index]),True)

	def prev_tl(self,sync=False):
		globals.currentAccount.currentIndex-=1
		if globals.currentAccount.currentIndex<0:
			globals.currentAccount.currentIndex=len(globals.currentAccount.list_timelines())-1
		self.focus_tl(sync)

	def next_tl(self,sync=False):
		globals.currentAccount.currentIndex+=1
		if globals.currentAccount.currentIndex>=len(globals.currentAccount.list_timelines()):
			globals.currentAccount.currentIndex=0
		self.focus_tl(sync)

	def prev_item(self):
		if globals.currentAccount.currentTimeline.index==0 or len(globals.currentAccount.currentTimeline.statuses)==0:
			sound.play(globals.currentAccount,"boundary")
			if globals.prefs.repeat:
				self.speak_item()
			return
		globals.currentAccount.currentTimeline.index-=1
		self.focus_tl_item()

	def prev_item_jump(self):
		if globals.currentAccount.currentTimeline.index < 20:
			sound.play(globals.currentAccount,"boundary")
			if globals.prefs.repeat:
				self.speak_item()
			return
		globals.currentAccount.currentTimeline.index -= 20
		self.focus_tl_item()
	
	def top_item(self):
		globals.currentAccount.currentTimeline.index=0
		self.focus_tl_item()
	
	def next_item(self):
		if globals.currentAccount.currentTimeline.index==len(globals.currentAccount.currentTimeline.statuses)-1 or len(globals.currentAccount.currentTimeline.statuses)==0:
			sound.play(globals.currentAccount,"boundary")
			if globals.prefs.repeat:
				self.speak_item()
			return
		globals.currentAccount.currentTimeline.index+=1
		self.focus_tl_item()
	
	def next_item_jump(self):
		if globals.currentAccount.currentTimeline.index >= len(globals.currentAccount.currentTimeline.statuses) - 20:
			sound.play(globals.currentAccount,"boundary")
			if globals.prefs.repeat:
				self.speak_item()
			return
		globals.currentAccount.currentTimeline.index += 20
		self.focus_tl_item()
	
	def bottom_item(self):
		globals.currentAccount.currentTimeline.index=len(globals.currentAccount.currentTimeline.statuses)-1
		self.focus_tl_item()
	
	def previous_from_user(self):
		main.window.OnPreviousFromUser()
		self.speak_item()
	
	def next_from_user(self):
		main.window.OnNextFromUser()
		self.speak_item()

	def previous_in_thread(self):
		main.window.OnPreviousInThread()
		self.speak_item()

	def next_in_thread(self):
		main.window.OnNextInThread()
		self.speak_item()

	def refresh(self,event=None):
		globals.currentAccount.currentTimeline.load(speech=True)

	def speak_account(self):
		speak.speak(globals.currentAccount.me.screen_name)

inv=invisible_interface()