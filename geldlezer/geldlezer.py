#! /usr/bin/pyhton3

import time
import threading
import os
import sys
import RPi.GPIO as GPIO
from keypad import keypad
from mfrc522 import SimpleMFRC522
import database as database

SUPERSECRETCODE = "9512"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

reader = SimpleMFRC522()
kp = keypad(columnCount=4)

def resetInterrupt():
    digit = None
    while digit == None:
        digit = kp.getKey()
    
    if(digit == "*"):
        os.execv(sys.argv[0], sys.argv)
    else:
        resetInterrupt()


def WaitForKeypadInput():
    digit = None
    while digit == None:
        digit = kp.getKey()

    print(digit)
    return digit


def WaitForRfidInput():
    id, text = reader.read()
    print(id)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    return id


def KeypadInputWithOk():
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


def betalen():
    print("bedrag")
    bedrag = KeypadInputWithOk()
    print("scan kaart")
    card = WaitForRfidInput()
    print("fix code")
    code = KeypadInputWithOk()
    database.write(card, bedrag, code)
    print("done")


def storten():
    print("fix code")
    code = KeypadInputWithOk()
    if code == SUPERSECRETCODE:
        time.sleep(0.5)
        print("ait bedrag")
        bedrag = KeypadInputWithOk()
        print("cardje pls")
        card = WaitForRfidInput()
        database.write(card, bedrag, "0000", False)
        print("goeidd")
    else:
        print("foute code")


resetThread = threading.Thread(target=resetInterrupt)
resetThread.start()

print("fix input")
function = WaitForKeypadInput()
print(f"function is {function}")
if function == "A":
    print("we gaan betalen")
    time.sleep(0.5)
    betalen()
elif function == "B":
    print("storten")
    time.sleep(0.5)
    storten()
else:
    print("not correct function input")

