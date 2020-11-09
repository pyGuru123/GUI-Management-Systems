#! python3
"""
@created: 07-11-2020 12:27:00 AM
@author: Prajjwal Pathak ( pyGuru )

Contact Management System

-------------------------------------------------------------------------------
Dependencies:

No external package is required

-------------------------------------------------------------------------------
Description : 
CMS is a advanced contact management system based on MVC architecture made using 
python and tkinter
"""

import re
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
from collections import namedtuple

import sql_operations
from customWidgets import CustomSearch, CustomEntry, CustomPhone

email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master=master
		self.pack()

		self._attributes()
		self.contacts = sql_operations.fetch_all_result()

		self.draw_header_frames()
		self.draw_all_contact_frame()

	def _attributes(self):
		self.search_term = tk.StringVar()
		self.search_term.set('')

		self.edit_contacts = False
		self.on_home = True
		self.is_new_contact = False

		self.data = None

	def draw_header_frames(self):
		self.header = tk.Frame(self, width=300, height=50, bg='dodgerblue')
		self.header.grid(row=0, column=0)
		self.header.grid_propagate(False)

		self.header_label = tk.Label(self.header, text='Contacts', font=('Algerian', 24),
						bg='dodgerblue', fg='white')
		self.header_label.grid(row=0, column=0, ipadx=2, pady=5) 

	def draw_all_contact_frame(self):
		# Frames
		self.contacts_frame = tk.Frame(self, width=300, height=400, bg='gray')
		self.search_bar = tk.Frame(self.contacts_frame, width=300, height=30)
		self.contact_box = tk.Frame(self.contacts_frame, width=300, height=320)
		self.bottom_menu = tk.Frame(self.contacts_frame, width=300, height=50, bg='dodgerblue3')

		self.contacts_frame.grid(row=1, column=0)
		self.search_bar.grid(row=0, column=0)
		self.contact_box.grid(row=1, column=0)
		self.bottom_menu.grid(row=2, column=0)

		self.contacts_frame.grid_propagate(False)
		self.search_bar.grid_propagate(False)
		self.contact_box.grid_propagate(False)
		self.bottom_menu.grid_propagate(False)

		# Widgets
		self.search_entry = CustomSearch(self.search_bar, width=32, textvariable=self.search_term)
		self.search_entry.grid(row=0, column=0, pady=5, padx=5)
		self.search_term.trace_add('write', self.enumerate_content)

		self.search_btn = tk.Button(self.search_bar, image=search_icon,
						relief=tk.FLAT)
		self.search_btn.grid(row=0, column=1, padx=60)

		self.contact_scroll = tk.Scrollbar(self.contact_box, orient=tk.VERTICAL)
		self.contact_scroll.grid(row=1, column=1, sticky='ns', pady=12)
		self.contact_list = tk.Listbox(self.contact_box, selectmode=tk.SINGLE,
				 selectbackground='sky blue', fg='black',
				 yscrollcommand=self.contact_scroll.set, font=('Times', 11))
		self.contact_list.configure(height=16, width=39)
		self.contact_list.bind('<Double-1>', self.show_contact)
		self.contact_list.bind('<Return>', self.show_contact)
		self.contact_list.grid(row=1, column=0, padx=2, sticky='W', pady=12)
		self.contact_scroll.config(command=self.contact_list.yview)

		self.num_contacts = tk.Label(self.bottom_menu, text=f'{len(self.contacts)} contacts saved',
							fg='white', bg='dodgerblue3', font=('Times', 11), width=16,
							anchor='w')
		self.num_contacts.grid(row=0, column=0, padx=5, pady=8)

		self.add_new_btn = tk.Button(self.bottom_menu, text=' New', fg='white', image=new_contact_icon,
							 relief=tk.FLAT, compound=tk.LEFT, font=('Times', 11), borderwidth=1,
							bg='dodgerblue3', command=self.create_new_contact)
		self.add_new_btn.grid(row=0, column=1, padx=80, pady=5)

		self.enumerate_content()

	def draw_display_contact_frame(self):
		self.search_term.set('')

		# frames
		self.new_contact_frame = tk.Frame(self, width=300, height=400, bg='gray')
		self.create_contact_frame = tk.Frame(self.new_contact_frame, width=300, height=350)
		self.bottom_menu = tk.Frame(self.new_contact_frame, width=300, height=50, bg='dodgerblue3')

		self.new_contact_frame.grid(row=1, column=0)
		self.create_contact_frame.grid(row=0, column=0)
		self.bottom_menu.grid(row=1, column=0)

		self.new_contact_frame.grid_propagate(False)
		self.create_contact_frame.grid_propagate(False)
		self.bottom_menu.grid_propagate(False)

		# widgets
		self.first = tk.LabelFrame(self.create_contact_frame, text='*First Name', bg='dodgerblue3',
						width=250, height=40, fg='white')
		self.last = tk.LabelFrame(self.create_contact_frame, text='Last Name', bg='dodgerblue3',
						width=250, height=40, fg='white')
		self.phone = tk.LabelFrame(self.create_contact_frame, text='*Phone', bg='dodgerblue3',
						width=250, height=40, fg='white')
		self.email = tk.LabelFrame(self.create_contact_frame, text='Email', bg='dodgerblue3',
						width=250, height=40, fg='white')

		self.first.grid(row=0, column=0, padx=25, pady=(30,0))
		self.last.grid(row=1, column=0, padx=25, pady=(30,0))
		self.phone.grid(row=2, column=0, padx=25, pady=(30,0))
		self.email.grid(row=3, column=0, padx=25, pady=(30,0))

		self.first.grid_propagate()
		self.last.grid_propagate()
		self.phone.grid_propagate()
		self.email.grid_propagate()

		if not self.edit_contacts:
			self.first_name = tk.Label(self.first, width=33, anchor='w')
			self.last_name = tk.Label(self.last, width=33, anchor='w')
			self.phone_number = tk.Label(self.phone, width=33, anchor='w')
			self.email_id = tk.Label(self.email, width=33, anchor='w')

			self.first_name.grid(row=0, column=0)
			self.last_name.grid(row=0, column=0)
			self.phone_number.grid(row=0, column=0)
			self.email_id.grid(row=0, column=0)

			self.back = tk.Button(self.bottom_menu, image=back_icon, bg='dodgerblue3',
								relief=tk.FLAT, command=self.go_back)
			self.copy = tk.Button(self.bottom_menu, image=copy_icon, bg='dodgerblue3',
								relief=tk.FLAT, command=self.copy_contact)
			self.edit = tk.Button(self.bottom_menu, image=edit_icon, bg='dodgerblue3',
								relief=tk.FLAT, command=self.edit_contact)
			self.delete = tk.Button(self.bottom_menu, image=delete_icon, bg='dodgerblue3',
								relief=tk.FLAT, command=self.delete_contact)

			self.back.grid(row=0, column=0, padx=(10,0), pady=4)
			self.copy.grid(row=0, column=1, padx=(40,0), pady=4)
			self.edit.grid(row=0, column=2, padx=(40,0), pady=4)
			self.delete.grid(row=0, column=3, padx=(40,0), pady=4)
		else:
			self.first_name = CustomEntry(self.first, width=39)
			self.last_name = tk.Entry(self.last, width=39)
			self.phone_number = CustomPhone(self.phone, width=39)
			self.email_id = tk.Entry(self.email, width=39)

			self.first_name.focus_set()

			self.first_name.grid(row=0, column=0)
			self.last_name.grid(row=0, column=0)
			self.phone_number.grid(row=0, column=0)
			self.email_id.grid(row=0, column=0)

			self.cancel = tk.Button(self.bottom_menu, image=cancel_icon, bg='dodgerblue3',
								relief=tk.FLAT, command=self.go_back)
			self.save_contact = tk.Button(self.bottom_menu, image=save_icon, bg='dodgerblue3',
								relief=tk.FLAT, activebackground='dodgerblue3',
								command=self.save_contact_in_db)

			self.cancel.grid(row=0, column=0, padx=5)
			self.save_contact.grid(row=0, column=1, padx=180)


	# Custom Functions

	def enumerate_content(self, var=None,indx=None, mode=None):
		self.contact_list.delete(0, tk.END)
		term = self.search_term.get()
		if term == '' or term == 'Search Contact':
			for index, contact in enumerate(self.contacts):
				self.contact_list.insert(index, (' ' + contact[0] + ' ' + contact[1]))
			self.num_contacts['text'] = f'{len(self.contacts)} contacts saved'
		else:
			temp_contact = [contact for contact in self.contacts if
							 (term.lower() in (contact[0].lower() + ' ' + contact[1].lower()))]
			for index, contact in enumerate(temp_contact):
				self.contact_list.insert(index, (' ' + contact[0] + ' ' + contact[1]))
			self.num_contacts['text'] = f'{len(temp_contact)} contacts found'

	def show_contact(self, event=None):
		if event:
			widget = event.widget
			selection=widget.curselection()
			if selection:
				self.data = self.contacts[selection[0]]

		if self.data:
			self.on_home = True
			self.edit_contacts = False
			self.draw_display_contact_frame()

			self.first_name['text'] = self.data[0]
			self.last_name['text'] = self.data[1]
			self.phone_number['text'] = self.data[2]
			self.email_id['text'] = self.data[3]

			self.prev = self.data
			self.update()

	def copy_contact(self):
		self.clipboard_clear()
		self.clipboard_append(self.data[2])
		messagebox.showinfo('CMS', 'Phone number copied to clipboard')

	def edit_contact(self):
		self.on_home = False
		self.is_new_contact = False
		self.edit_contacts = True
		self.new_contact_frame.destroy()
		self.draw_display_contact_frame()

		self.first_name.delete(0, tk.END)
		self.first_name.insert(0, self.data[0])
		self.last_name.delete(0, tk.END)
		self.last_name.insert(0, self.data[1])
		self.phone_number.delete(0, tk.END)
		self.phone_number.insert(0, self.data[2])
		self.email_id.delete(0, tk.END)
		self.email_id.insert(0, self.data[3])

	def create_new_contact(self):
		self.on_home = True
		self.is_new_contact = True
		self.edit_contacts = True
		self.draw_display_contact_frame()

	def save_contact_in_db(self):
		first_name = self.first_name.get().strip().lower().capitalize()
		last_name = self.last_name.get().strip().lower().capitalize()
		phone = self.phone_number.get().strip()
		email = self.email_id.get().strip()

		temp_contact = [(contact[0] + ' ' + contact[1]) for contact in self.contacts]
		
		if (first_name == '' or first_name == 'This field is required' or phone == ''
				or phone == 'This field is required'):
			messagebox.showerror('CMS', 'Fill in the Mandatory Fields')
		elif len(phone) != 10:
			messagebox.showerror('CMS', 'Enter 10 digit phone number')
		elif email and not valid_email(email):
			messagebox.showerror('CMS', 'Invalid email')
		else:
			if self.is_new_contact:
				if (first_name + ' ' + last_name) in temp_contact:
					messagebox.showerror('CMS', 'Contact with this name already\nexist, edit & try again')
				else:
					status = sql_operations.insert_item([first_name ,last_name, phone, email])
					if status == 'success':
						messagebox.showinfo('CMS', 'Contact Saved')
					else:
						messagebox.showerror('CMS', 'An error Occured')

					self.contacts = sql_operations.fetch_all_result()
					self.data = (first_name ,last_name, phone, email)
					self.show_contact()
			else:
				status = sql_operations.delete_item(self.prev[0], self.prev[1])
				if status == 'success':
					status = sql_operations.insert_item([first_name ,last_name, phone, email])
					if status == 'success':
						messagebox.showinfo('CMS', 'Contact Saved')
					else:
						messagebox.showerror('CMS', 'An error Occured')

					self.contacts = sql_operations.fetch_all_result()
					self.data = (first_name ,last_name, phone, email)
					self.prev = self.data
					self.show_contact()

	def delete_contact(self):
		status = sql_operations.delete_item(self.data[0], self.data[1])
		if status == 'success':
			messagebox.showinfo('CMS', 'Contact deleted')
		else:
			messagebox.showerror('CMS', 'An error Occured')

		self.contacts = sql_operations.fetch_all_result()
		self.data = None
		self.on_home = True
		self.go_back()

	def go_back(self):
		if self.on_home:
			self.new_contact_frame.destroy()
			self.draw_all_contact_frame()
			self.update()
		else:
			self.new_contact_frame.destroy()
			self.show_contact()

def valid_email(email):
	if re.fullmatch(email_regex, email):
		return True
	return False

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('300x450')
	root.title('CMS')
	root.iconbitmap('icons/phone.ico')
	root.wm_resizable(0,0)

	search_icon = PhotoImage(file='icons/search.png')
	new_contact_icon = PhotoImage(file='icons/new.png')
	save_icon = PhotoImage(file='icons/save.png')
	back_icon = PhotoImage(file='icons/back.png')
	copy_icon = PhotoImage(file='icons/copy.png')
	delete_icon = PhotoImage(file='icons/delete.png')
	edit_icon = PhotoImage(file='icons/edit.png')
	cancel_icon = PhotoImage(file='icons/cancel.png')

	app = Application(master=root)
	app.mainloop()