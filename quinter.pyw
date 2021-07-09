import application
import platform
import sys
sys.dont_write_bytecode=True
if platform.system()!="Darwin":
	f=open("errors.log","a")
	sys.stderr=f
import shutil
import os
if os.path.exists(os.path.expandvars("%temp%\gen_py"))==True:
	shutil.rmtree(os.path.expandvars("%temp%\gen_py"))
# Bye foo!
os.chdir(".")
import wx
app = wx.App(redirect=False)

import speak
from GUI import main
import globals
globals.load()
if globals.prefs.window_shown==True:
	main.window.Show()
else:
	speak.speak("Welcome to Quinter! Main window hidden.")
app.MainLoop()