#! /usr/bin/python3

import mysql.connector

# config = {'user': 'vanhouckedre_bechiro', 'password': 'DreStinkt', 'host' : 'vanhouckedre.be.mysql', 'database': 'vanhouckedre_bechiro'}
config = {'user': 'arno', 'password': 'test1234', 'host' : '192.168.0.125', 'database': 'rfidgame'}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

def read(nummer, code):
	nummer = str(nummer)
	code = str(code)
	cursor.execute("SELECT code FROM rfid WHERE nummer = " + nummer + ";")
	if (cursor.fetchall() == code):
		cursor.execute("SELECT bedrag FROM rfid WHERE nummer = " + nummer + ";")
		huidigTotaal = cursor.fetchall()

		print("totaal van " + nummer + " is: " + huidigTotaal)

	else:
		print("Foute code!")

def write(nummer, bedrag, code, betalen=True):
	nummer = str(nummer)
	code = str(code)
	if betalen:
		cursor.execute("SELECT code FROM rfid WHERE nummer = " + nummer + ";")
		if (cursor.fetchall() == code):
			cursor.execute("SELECT bedrag FROM rfid WHERE nummer = " + nummer + ";")
			huidigTotaal = cursor.fetchall()

			nieuwTotaal = str(huidigTotaal - bedrag)
			cursor.execute("UPDATE rfid SET bedrag = " + nieuwTotaal + " WHERE nummer = " + nummer + ";")
			cursor.commit()

			print("Nieuw totaal van " + nummer + " is: " + nieuwTotaal)
			
		else:
			print("foute code!")


	elif not betalen:
		cursor.execute("SELECT bedrag FROM rfid WHERE nummer = " + nummer + ";")
		huidigTotaal = cursor.fetchall()

		nieuwTotaal = str(huidigTotaal + bedrag)
		cursor.execute("UPDATE rfid SET bedrag = " + nieuwTotaal + " WHERE nummer = " + nummer + ";")
		cursor.commit()

		print("Nieuw totaal van " + nummer + " is: " + nieuwTotaal)
	
	else:
		print("Er is iet fout gegaan!")
