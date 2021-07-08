import platform
if platform.system()=="Darwin":
	from accessible_output2 import outputs
	speaker = outputs.auto.Auto()
else:
	import Tolk as speaker
	speaker.load()
	speaker.try_sapi=True

def speak(text,interrupt=False):
	if platform.system()=="Darwin":
		speaker.speak(text,interrupt)
	else:
		speaker.output(text,interrupt)