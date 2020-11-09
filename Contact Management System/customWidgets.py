import tkinter as tk

class CustomSearch(tk.Entry):
	def __init__(self, parent, *args, **kwargs):
		tk.Entry.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.bind('<FocusOut>', self.add_placeholder)
		self.bind('<FocusIn>', self.clear_placeholder)

		self.configure(fg="gray70")
		self.insert(0, 'Search Contact')

	def add_placeholder(self, event=None):
		if not self.get():
			self.configure(fg="gray70")
			self.insert(0, 'Search Contact')

	def clear_placeholder(self, event):
		if event and self.get() == 'Search Contact':
			self.delete('0', 'end')
			self.configure(fg="black")

class CustomEntry(tk.Entry):
	def __init__(self, parent, *args, **kwargs):
		tk.Entry.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.bind('<FocusOut>', self.add_placeholder)
		self.bind('<FocusIn>', self.clear_placeholder)

	def add_placeholder(self, event=None):
		if not self.get():
			self.configure(fg="red")
			self.insert(0, 'This field is required')

	def clear_placeholder(self, event):
		if event and self.get() == 'This field is required':
			self.delete('0', 'end')
			self.configure(fg="black")

class CustomPhone(CustomEntry):
	def __init__(self, parent, *args, **kwargs):
		CustomEntry.__init__(self, parent, *args, **kwargs)
		self.var = tk.StringVar(parent)
		self.var.trace('w', self.validate)
		self.configure(textvariable=self.var)
		self.get, self.set = self.var.get, self.var.set
	
	def validate(self, *args):
		value = self.get()
		if len(value) <= 10:
			if not value.isdigit():
				self.set(''.join(x for x in value if x.isdigit()))
		else:
			if value != 'This field is required':
				value = value[:10]
				self.set(value[:10])