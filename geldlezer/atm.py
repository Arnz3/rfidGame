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

def writeJson(message, bedrag):
    f = open('../atm/data.json', 'rw')
    data = json.load(f)
    data[message] = message
    data[bedrag] = bedrag
    json.dump(data, f)
    f.close()


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
    writeJson("Dit is uw totaal bedrag:", bedrag)


def schulden():
    print("schulden")
    schulden = database.readall()
    totaalBedragen = 0
    for schuld in schulden:
        totaalBedragen += int(schuld)
    totaalschulden = 1000000 - totaalBedragen
    writeJson("De totale schulden zijn", totaalschulden)


print("fix input")
function = WaitForKeypadInput()
if function == "A":
    print("ait totaal ja")
    getTotaal()
if function == "B":
    schulden()
if function == "C":
    pass
