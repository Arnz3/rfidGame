#! /usr/bin/pyhton3

import threading
import os
import sys
import time
from unicodedata import digit
import RPi.GPIO as GPIO
from keypad import keypad
from mfrc522 import SimpleMFRC522
import database

SUPERSECRETCODE = "9512"

GPIO.setwarnings(False)

reader = SimpleMFRC522()
kp = keypad(columnCount=4)

def starInterrupt():
    digit = None
    while digit == None:
        digit = kp.getKey()
    
    if(digit == "*"):
        print("reset shit")
        os.execv(sys.argv[0], sys.argv)
    else:
        starInterrupt()


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

        print(digit)
        if digit == "D":
            pass
        else:
            bedrag += str(digit)
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


resetThread = threading.Thread(target=starInterrupt)
resetThread.start()

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

