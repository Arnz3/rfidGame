#! /usr/bin/python2.7

import mysql.connector

config = {'user': 'root', 'password': 'ArnoSuckt', 'host' : '10.10.12.50', 'database': 'mysql'}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

def read(naam, code):
	cursor.execute("SELECT code FROM users WHERE naam = " + naam + ";")
	if (cursor.fetchall() == code):
		cursor.execute("SELECT totaal FROM users WHERE naam = " + naam + ";")
		huidigTotaal = cursor.fetchall()

		return "totaal van " + naam + " is: " + huidigTotaal

	else:
		return "Foute code!"

def write(naam, bedrag, code):
	cursor.execute("SELECT code FROM users WHERE naam = " + naam + ";")
	if (cursor.fetchall() == code):
		cursor.execute("SELECT totaal FROM users WHERE naam = " + naam + ";")
		huidigTotaal = cursor.fetchall()

		nieuwTotaal = huidigTotaal + bedrag
		cursor.execute("UPDATE users SET totaal = " + nieuwTotaal + " WHERE naam = " + naam + ";")
		cursor.commit()

		return "Nieuw totaal van " + naam + " is: " + nieuwTotaal
	
	else:
		return "Foute code!"