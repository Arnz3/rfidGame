#! /usr/bin/python3

import mysql.connector

# config = {'user': 'vanhouckedre_bechiro', 'password': 'DreStinkt', 'host' : 'vanhouckedre.be.mysql', 'database': 'vanhouckedre_bechiro'}
config = {'user': 'arno', 'password': 'test1234', 'host' : '192.168.0.125', 'database': 'rfidgame'}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

def read(nummer):
	nummer = str(nummer)
	
	cursor.execute("SELECT bedrag FROM rfid WHERE nummer = " + nummer + ";")
	huidigTotaal = cursor.fetchall()[0][0]

	print("totaal van " + nummer + " is: " + huidigTotaal)
	return huidigTotaal


def readall():
	cursor.execure("SELECT bedrag FROM rfid")
	bedragen = cursor.fetchall()

	return bedragen


def write(nummer, bedrag, code, betalen=True):
	nummer = str(nummer)
	code = str(code)
	if betalen:
		cursor.execute("SELECT code FROM rfid WHERE nummer = " + nummer + ";")
		if (cursor.fetchall()[0][0] == code):
			cursor.execute("SELECT bedrag FROM rfid WHERE nummer = " + nummer + ";")
			huidigTotaal = cursor.fetchall()[0][0]

			nieuwTotaal = str(int(huidigTotaal) - int(bedrag))
			cursor.execute("UPDATE rfid SET bedrag = " + nieuwTotaal + " WHERE nummer = " + nummer + ";")
			conn.commit()

			print("Nieuw totaal van " + nummer + " is: " + nieuwTotaal)
			
		else:
			print("foute code!")


	elif not betalen:
		cursor.execute("SELECT bedrag FROM rfid WHERE nummer = " + nummer + ";")
		huidigTotaal = cursor.fetchall()[0][0]

		nieuwTotaal = str(int(huidigTotaal) + int(bedrag))
		cursor.execute("UPDATE rfid SET bedrag = " + nieuwTotaal + " WHERE nummer = " + nummer + ";")
		conn.commit()

		print("Nieuw totaal van " + nummer + " is: " + nieuwTotaal)
	
	else:
		print("Er is iet fout gegaan!")
