import wx

def ask(parent=None, message="", caption="", default_value=""):
	dlg = wx.TextEntryDialog(parent, caption, message, value=default_value)
	dlg.ShowModal()
	result = dlg.GetValue()
	dlg.Destroy()
	return result

app = wx.App()
