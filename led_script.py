import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
yellow = 23
red = 12
green = 21

GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

for i in range(2):
	GPIO.output(yellow, True)
	time.sleep(1)
	GPIO.output(green, True)
	time.sleep(1)
	GPIO.output(red, True)
	time.sleep(1)
	GPIO.output(yellow, False)
	time.sleep(1)
	GPIO.output(green, False)
	time.sleep(1)
	GPIO.output(red, False)
GPIO.cleanup()
print("Bye Bye~~")
