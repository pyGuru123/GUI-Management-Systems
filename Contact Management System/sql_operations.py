import os
import sqlite3

if not os.path.exists('files/contacts.db'):
	with sqlite3.connect('files/contacts.db') as conn:
		conn.execute('''CREATE TABLE contacts (
					first_name text NOT NULL,
					last_name text,
					phone text NOT NULL,
					email text)
			''')
		print('database created successfully')

def insert_item(values):
	with sqlite3.connect('files/contacts.db') as conn:
		cursor = conn.cursor()
		try:
			cursor.execute("INSERT INTO contacts VALUES (?,?,?,?)",	
							values)
			return 'success'
		except:
			return 'error'

def delete_item(first_name, last_name):
	query =  "DELETE FROM contacts WHERE first_name = ? and last_name = ?"
	with sqlite3.connect('files/contacts.db') as conn:
		cursor = conn.cursor()
		try:
			cursor.execute(query, (first_name, last_name))
			return 'success'
		except:
			return 'error'

def fetch_single_result(first_name, last_name):
	query = "SELECT * FROM contacts WHERE first_name = ? and last_name = ?"
	with sqlite3.connect('files/contacts.db') as conn:
		cursor = conn.cursor()
		try:
			cursor.execute(query, (first_name, last_name))
			data = cursor.fetchone()
			return data
		except:
			return 'error'

def fetch_all_result():
	query = "SELECT * FROM contacts"
	with sqlite3.connect('files/contacts.db') as conn:
		cursor = conn.cursor()
		try:
			cursor.execute(query)
			data = cursor.fetchall()
			return sorted(data)
		except:
			return 'error'