#! /usr/bin/pyhton3

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

def WaitForKeypadInput():
    digit = None
    while digit == None:
        digit = kp.getKey()

    print("digit")
    return digit


def WaitForRfidInput():
    id, text = reader.read()
    print(id)
    GPIO.cleanup()
    return id

    
def KeypadInputWithOk():
    digit = None
    bedrag = ""
    while digit != "#":
        digit = kp.getKey()
        if digit == "D":
            pass
        else:
            bedrag += digit

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
    code = KeypadInputWithOk()
    if code == SUPERSECRETCODE:
        bedrag = KeypadInputWithOk()
        card = WaitForRfidInput()
        database.write(card, bedrag, "0000", False)
    else:
        print("foute code")



function = WaitForKeypadInput()
print(f"function is {function}")
if function == "A":
    print("we gaan betalen")
    betalen()
elif function == "B":
    print("storten")
    storten()
else:
    print("not correct function input")

