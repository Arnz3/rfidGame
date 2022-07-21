#! /usr/bin/python3

import mysql.connector

config = {'user': 'vanhouckedre_bechiro', 'password': 'ArnoSuckt', 'host' : 'vanhouckedre.be.mysql:69', 'database': 'vanhouckedre_bechiro'}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

def read(nummer, code):
	cursor.execute("SELECT code FROM rfid WHERE naam = " + nummer + ";")
	if (cursor.fetchall() == code):
		cursor.execute("SELECT bedrag FROM rfid WHERE naam = " + nummer + ";")
		huidigTotaal = cursor.fetchall()

		return "totaal van " + nummer + " is: " + huidigTotaal

	else:
		return "Foute code!"

def write(nummer, bedrag, code, betalen=True):
	if betalen:
		cursor.execute("SELECT code FROM rfid WHERE nummer = " + nummer + ";")
		if (cursor.fetchall() == code):
			cursor.execute("SELECT bedrag FROM rfid WHERE nummer = " + nummer + ";")
			huidigTotaal = cursor.fetchall()

			nieuwTotaal = huidigTotaal - bedrag
			cursor.execute("UPDATE rfid SET bedrag = " + nieuwTotaal + " WHERE nummer = " + nummer + ";")
			cursor.commit()

			return "Nieuw totaal van " + nummer + " is: " + nieuwTotaal
			
		else:
			return "foute code!"


	elif not betalen:
		cursor.execute("SELECT bedrag FROM rfid WHERE nummer = " + nummer + ";")
		huidigTotaal = cursor.fetchall()

		nieuwTotaal = huidigTotaal + bedrag
		cursor.execute("UPDATE rfid SET bedrag = " + nieuwTotaal + " WHERE nummer = " + nummer + ";")
		cursor.commit()

		return "Nieuw totaal van " + nummer + " is: " + nieuwTotaal
	
	else:
		return "Er is iet fout gegaan!"
