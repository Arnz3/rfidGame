#! /usr/bin/python3

import time
import RPi.GPIO as GPIO
from keypad import keypad
from mfrc522 import SimpleMFRC522
import database as database

SUPERSECRETCODE = "6969"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

redLed = 11
yellowLed = 13
greenLed = 15

GPIO.setup(redLed, GPIO.OUT)
GPIO.setup(yellowLed, GPIO.OUT)
GPIO.setup(greenLed, GPIO.OUT)
GPIO.output(greenLed, GPIO.LOW)
GPIO.output(redLed, GPIO.LOW)
GPIO.output(yellowLed, GPIO.LOW)

reader = SimpleMFRC522()
kp = keypad(columnCount=4)


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
    GPIO.setup(redLed, GPIO.OUT)
    GPIO.setup(yellowLed, GPIO.OUT)
    GPIO.setup(greenLed, GPIO.OUT)
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
    # groen lampje aan
    GPIO.output(greenLed, GPIO.HIGH)
    bedrag = KeypadInputWithOk()
    print("scan kaart")
    GPIO.output(greenLed, GPIO.LOW)

    # geel lampje aan
    GPIO.output(yellowLed, GPIO.HIGH) 
    card = WaitForRfidInput()
    print("fix code")
    # groen en geel lampje aan
    GPIO.output(greenLed, GPIO.HIGH)
    code = KeypadInputWithOk()
    if(database.write(card, bedrag, code)):
        print("done")
        # alle lampjes aan
        GPIO.output(redLed, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(greenLed, GPIO.LOW)
        GPIO.output(redLed, GPIO.LOW)
        GPIO.output(yellowLed, GPIO.LOW)
    else:
        GPIO.output(greenLed, GPIO.LOW)
        GPIO.output(yellowLed, GPIO.LOW)
        GPIO.output(redLed, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(redLed, GPIO.LOW)


def storten():
    print("fix code")
    GPIO.output(greenLed, GPIO.HIGH)
    GPIO.output(yellowLed, GPIO.HIGH)
    code = KeypadInputWithOk()
    # groen en geel lampje aan 
    if code == SUPERSECRETCODE:
        time.sleep(0.5)
        print("ait bedrag")
        GPIO.output(yellowLed, GPIO.LOW)
        # groen lampje aan 
        bedrag = KeypadInputWithOk()
        print("cardje pls")
        # geel lampje aan
        GPIO.output(greenLed, GPIO.LOW)
        GPIO.output(yellowLed, GPIO.HIGH)
        card = WaitForRfidInput()
        if(database.write(card, bedrag, "0000", False)):
            print("goeidd")
            GPIO.output(redLed, GPIO.HIGH)
            GPIO.output(greenLed, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(greenLed, GPIO.LOW)
            GPIO.output(redLed, GPIO.LOW)
            GPIO.output(yellowLed, GPIO.LOW)
            # alle lampjes aan 
    else:
        # rood lampje aan
        GPIO.output(greenLed, GPIO.LOW)
        GPIO.output(yellowLed, GPIO.LOW)
        GPIO.output(redLed, GPIO.HIGH)
        print("foute code")
        time.sleep(3)
        GPIO.output(redLed, GPIO.LOW)

while True:
    print("fix input")
    # groen lampje aan 
    GPIO.output(greenLed, GPIO.HIGH)
    function = WaitForKeypadInput()
    print(f"function is {function}")
    GPIO.output(greenLed, GPIO.LOW)
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

