#! /usr/bin/env pyhton3

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

    return digit


def WaitForRfidInput():
    id, text = reader.read()
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
    bedrag = KeypadInputWithOk()
    card = WaitForRfidInput()
    code = KeypadInputWithOk()
    database.write(card, bedrag, code)


def storten():
    code = KeypadInputWithOk()
    if code == SUPERSECRETCODE:
        bedrag = KeypadInputWithOk()
        card = WaitForRfidInput()
        database.write(card, bedrag, "0000", False)
    else:
        print("foute code")


while True:
    function = WaitForKeypadInput()
    if function == "A":
        betalen()
    elif function == "B":
        storten()
    else:
        print("not correct function input")

