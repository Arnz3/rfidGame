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
	cursor.execute("SELECT bedrag FROM rfid")
	bedragen = cursor.fetchall()

	return bedragen[0]


def write(nummer, bedrag, code, betalen=True):
	nummer = str(nummer)
	code = str(code)
	if betalen:
		cursor.execute("SELECT code FROM rfid WHERE nummer = " + nummer + ";")
		results = cursor.fetchall()
		if (results == None):
			return False

		if (results[0][0] == code):
			cursor.execute("SELECT bedrag FROM rfid WHERE nummer = " + nummer + ";")
			huidigTotaal = cursor.fetchall()[0][0]
			
			if (int(huidigTotaal) < int(bedrag)):
				print("niet genoeg cash")
				return False
			else:
				nieuwTotaal = str(int(huidigTotaal) - int(bedrag))
				cursor.execute("UPDATE rfid SET bedrag = " + nieuwTotaal + " WHERE nummer = " + nummer + ";")
				conn.commit()

				print("Nieuw totaal van " + nummer + " is: " + nieuwTotaal)
				return True
			
		else:
			# rood lampje aan 
			print("foute code!")
			return False


	elif not betalen:
		cursor.execute("SELECT bedrag FROM rfid WHERE nummer = " + nummer + ";")
		huidigTotaal = cursor.fetchall()[0][0]

		nieuwTotaal = str(int(huidigTotaal) + int(bedrag))
		cursor.execute("UPDATE rfid SET bedrag = " + nieuwTotaal + " WHERE nummer = " + nummer + ";")
		conn.commit()

		print("Nieuw totaal van " + nummer + " is: " + nieuwTotaal)
		return True
	
	else:
		print("Er is iet fout gegaan!")
		return False
