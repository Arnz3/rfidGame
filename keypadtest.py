import time
import RPi.GPIO as GPIO
from keypad import keypad

GPIO.setwarnings(False)
while True:
	if __name__ == "__main__":
		kp = keypad(columnCount=4)

		digit = None
		while digit == None:
			digit = kp.getKey()
		print(digit)
		time.sleep(0.5)
