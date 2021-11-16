import wx
import globals
from . import misc
from . import view

class ListsGui(wx.Dialog):
	def __init__(self,account,user=None,add=True):
		self.account=account
		self.add=add
		self.user=user
		self.lists=self.account.api.get_lists()
		wx.Dialog.__init__(self, None, title="Lists", size=(350,200))
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.list_label=wx.StaticText(self.panel, -1, label="&Lists")
		self.list=wx.ListBox(self.panel, -1)
		self.main_box.Add(self.list, 0, wx.ALL, 10)
		self.list.SetFocus()
		self.list.Bind(wx.EVT_LISTBOX, self.on_list_change)
		self.add_items()
		if self.user!=None:
			if self.add:
				self.load = wx.Button(self.panel, wx.ID_DEFAULT, "&Add")
			else:
				self.load = wx.Button(self.panel, wx.ID_DEFAULT, "&Remove")
		else:
			self.load = wx.Button(self.panel, wx.ID_DEFAULT, "&Load list")
		self.load.SetDefault()
		self.load.Bind(wx.EVT_BUTTON, self.Load)
		self.load.Enable(False)
		self.main_box.Add(self.load, 0, wx.ALL, 10)
		if len(self.lists)>0:
			self.list.SetSelection(0)
			self.on_list_change(None)
		if self.user==None:
			self.new = wx.Button(self.panel, wx.ID_DEFAULT, "&New list")
			self.new.Bind(wx.EVT_BUTTON, self.New)
			self.main_box.Add(self.new, 0, wx.ALL, 10)
			self.edit = wx.Button(self.panel, wx.ID_DEFAULT, "&Edit list")
			self.edit.Bind(wx.EVT_BUTTON, self.Edit)
			self.main_box.Add(self.edit, 0, wx.ALL, 10)
			if len(self.lists)==0:
				self.edit.Enable(False)
			self.view_members = wx.Button(self.panel, wx.ID_DEFAULT, "&View list members")
			self.view_members.Bind(wx.EVT_BUTTON, self.ViewMembers)
			self.main_box.Add(self.view_members, 0, wx.ALL, 10)
			if len(self.lists)==0 or self.lists[self.list.GetSelection()].member_count==0:
				self.view_members.Enable(False)
			self.view_subscribers = wx.Button(self.panel, wx.ID_DEFAULT, "&View list subscribers")
			self.view_subscribers.Bind(wx.EVT_BUTTON, self.ViewSubscribers)
			self.main_box.Add(self.view_subscribers, 0, wx.ALL, 10)
			if len(self.lists)==0 or self.lists[self.list.GetSelection()].subscriber_count==0:
				self.view_subscribers.Enable(False)
			self.remove = wx.Button(self.panel, wx.ID_DEFAULT, "&Remove list")
			self.remove.Bind(wx.EVT_BUTTON, self.Remove)
			self.main_box.Add(self.remove, 0, wx.ALL, 10)
			if len(self.lists)==0:
				self.remove.Enable(False)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()

	def add_items(self):
		for i in self.lists:
			self.list.Insert(i.name+", "+i.description+", "+str(i.member_count)+" members, "+str(i.subscriber_count)+" subscribers.",self.list.GetCount())
		if len(self.lists)>0:
			self.list.SetSelection(0)
		else:
			if hasattr(self,"load"):
				self.load.Enable(False)
			if hasattr(self,"edit"):
				self.edit.Enable(False)
			if hasattr(self,"remove"):
				self.remove.Enable(False)

	def on_list_change(self,event):
		self.load.Enable(True)
		if hasattr(self,"edit"):
			self.edit.Enable(True)
		if hasattr(self,"remove"):
			self.remove.Enable(True)
		if hasattr(self,"view_members"):
				if len(self.lists)==0 or self.lists[self.list.GetSelection()].member_count==0:
					self.view_members.Enable(False)
				else:
					self.view_members.Enable(True)
		if hasattr(self,"view_subscribers"):
				if len(self.lists)==0 or self.lists[self.list.GetSelection()].subscriber_count==0:
					self.view_subscribers.Enable(False)
				else:
					self.view_subscribers.Enable(True)

	def New(self, event):
		l=NewListGui(self.account)
		l.Show()

	def Edit(self, event):
		l=NewListGui(self.account,self.lists[self.list.GetSelection()])
		l.Show()

	def Remove(self, event):
		self.account.api.destroy_list(list_id=self.lists[self.list.GetSelection()].id)
		self.lists.remove(self.lists[self.list.GetSelection()])
		self.list.Clear()
		self.add_items()

	def ViewSubscribers(self, event):
		list=self.lists[self.list.GetSelection()]
		v=view.UserViewGui(self.account,self.account.api.list_subscribers(count=200, list_id=list.id),"List subscribers")
		v.Show()

	def ViewMembers(self, event):
		list=self.lists[self.list.GetSelection()]
		v=view.UserViewGui(self.account,self.account.api.list_members(count=200, list_id=list.id),"List members")
		v.Show()

	def Load(self, event):
		if self.user==None:
			misc.list_timeline(self.account,self.lists[self.list.GetSelection()].name, self.lists[self.list.GetSelection()].id)
		else:
			if self.add:
				self.account.api.add_list_member(user_id=self.user.id, list_id=self.lists[self.list.GetSelection()].id)
			else:
				self.account.api.remove_list_member(user_id=self.user.id, list_id=self.lists[self.list.GetSelection()].id)
		self.Destroy()

	def OnClose(self, event):
		self.Destroy()

class NewListGui(wx.Dialog):
	def __init__(self,account,list=None):
		self.account=account
		self.list=list
		title="New list"
		if list!=None:
			title="Edit list "+list.name
		wx.Dialog.__init__(self, None, title=title, size=(350,200))
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.panel = wx.Panel(self)
		self.main_box = wx.BoxSizer(wx.VERTICAL)
		self.text_label = wx.StaticText(self.panel, -1, "Name of list")
		self.text = wx.TextCtrl(self.panel, -1, "",style=wx.TE_PROCESS_ENTER|wx.TE_DONTWRAP)
		self.main_box.Add(self.text, 0, wx.ALL, 10)
		self.text.SetFocus()
		if list!=None:
			self.text.SetValue(self.list.name)
		self.text2_label = wx.StaticText(self.panel, -1, "Description of list")
		self.text2 = wx.TextCtrl(self.panel, -1, "",style=wx.TE_PROCESS_ENTER|wx.TE_DONTWRAP)
		self.main_box.Add(self.text2, 0, wx.ALL, 10)
		if list!=None:
			self.text2.SetValue(self.list.description)
		self.type_label = wx.StaticText(self.panel, -1, "Mode")
		self.type = wx.ComboBox(self.panel, -1, "",style=wx.CB_READONLY)
		self.type.Insert("private",0)
		self.type.Insert("public",1)
		self.type.SetSelection(0)
		if self.list!=None:
			if self.list.mode=="public":
				self.type.SetSelection(1)

		self.main_box.Add(self.type, 0, wx.ALL, 10)
		if self.list!=None:
			self.create = wx.Button(self.panel, wx.ID_DEFAULT, "&Edit list")
		else:
			self.create = wx.Button(self.panel, wx.ID_DEFAULT, "&Create list")
		self.create.SetDefault()
		self.create.Bind(wx.EVT_BUTTON, self.Create)
		self.main_box.Add(self.create, 0, wx.ALL, 10)
		self.close = wx.Button(self.panel, wx.ID_CANCEL, "&Cancel")
		self.close.Bind(wx.EVT_BUTTON, self.OnClose)
		self.main_box.Add(self.close, 0, wx.ALL, 10)
		self.panel.Layout()

	def Create(self, event):
		if self.list==None:
			self.account.api.create_list(name=self.text.GetValue(),mode=self.type.GetString(self.type.GetSelection()),description=self.text2.GetValue())
		else:
			self.account.api.update_list(list_id=self.list.id, name=self.text.GetValue(),mode=self.type.GetString(self.type.GetSelection()),description=self.text2.GetValue())
		self.Destroy()

	def OnClose(self, event):
		self.Destroy()