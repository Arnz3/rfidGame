#! /usr/bin/pyhton3

import time
import json
import RPi.GPIO as GPIO
from keypad import keypad
from mfrc522 import SimpleMFRC522
import database

GPIO.setwarnings(False)

reader = SimpleMFRC522()
kp = keypad(columnCount=4)

def writehtml(message, bedrag):
    f = open('../atm/index.html', 'w')
    html =  f'''<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="stylesheet" href="style.css">
                    <title>ATM</title>
                </head>
                <body onLoad="timeRefresh(2000);">
                    <div class="content">
                        <h3 id="message">{message}</h3>
                        <h1 id="bedrag">{bedrag}</h1>
                    </div>
                    <script src="script.js"></script>
                </body>
                </html>'''
    f.write(html)
    f.close


def WaitForKeypadInput():
    GPIO.setmode(GPIO.BOARD)
    digit = None
    while digit == None:
        digit = kp.getKey()

    print(digit)
    return digit


def WaitForRfidInput():
    id, text = reader.read()
    print(id)
    GPIO.cleanup()
    return id


def KeypadInputWithOk():
    GPIO.setmode(GPIO.BOARD)
    bedrag = ""
    digit = None
    while digit != "#":
        digit = None
        while digit == None:
            digit = kp.getKey()

        if digit == "D":
            bedrag = bedrag[:-1]
        else:
            bedrag += str(digit)
        print(bedrag)
        time.sleep(0.4)
    
    bedrag = bedrag.replace('#', '')
    print(f"bedrag is {bedrag}")
    return bedrag


def getTotaal():
    print("fix kaart")
    card = WaitForRfidInput()
    bedrag = database.read(card)
    writehtml("Dit is uw totaal bedrag:", bedrag)


def schulden():
    print("schulden")
    schulden = database.readall()
    totaalBedragen = 0
    for schuld in schulden:
        totaalBedragen += int(schuld)
    totaalschulden = 1000000 - totaalBedragen
    writehtml("De totale schulden zijn", totaalschulden)


print("fix input")
function = WaitForKeypadInput()
if function == "A":
    print("ait totaal ja")
    getTotaal()
if function == "B":
    schulden()
if function == "C":
    pass
