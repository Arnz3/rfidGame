#! /usr/bin/python2.7

import mysql.connector

config = {'user': 'root', 'password': 'ArnoSuckt', 'host' : '10.10.12.50', 'database': 'mysql'}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

def write(data, table):
	sql = "INSERT INTO " + table + " VALUES (" + data + ");"
	cursor.execute(sql)
	conn.commit()

def read(table):
	sql = "SELECT * FROM "+ table + ";"
	cursor.execute(sql)
	return cursor.fetchall()

write('420', 'arno')
print(read('arno'))
