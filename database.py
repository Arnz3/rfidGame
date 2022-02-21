#! /usr/bin/python2.7

import mysql.connector

config = {'user': 'root', 'password': 'ArnoSuckt', 'host' : '10.10.12.50', 'database': 'mysql'}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

def read(table):
	sql = "SELECT * FROM "+ table + ";"
	cursor.execute(sql)
	return cursor.fetchall()

def write(naam, bedrag, code):
	cursor.execute("SELECT code FROM users WHERE naam = " + naam + ";")
	if (cursor.fetchall() == code):
		cursor.execute("SELECT totaal FROM users WHERE naam = " + naam + ";")
		huidigTotaal = cursor.fetchall()

		nieuwTotaal = huidigTotaal + bedrag
		cursor.execute("UPDATE users SET totaal = " + nieuwTotaal + " WHERE naam = " + naam + ";")
		cursor.commit()

		return "Niet totaal van " + naam + " is: " + nieuwTotaal
	
	else:
		return "Foute code!"