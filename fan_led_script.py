import RPi.GPIO as GPIO
import time

# -----------initial setting ---------------
GPIO.setmode(GPIO.BCM)
yellow = 23
red = 12
green = 21
GPIO.setup(yellow, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

pwm_pin = 13
in1 = 5
in2 = 6
GPIO.setup(pwm_pin, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
freq = 60
pwm = GPIO.PWM(pwm_pin, freq)

#----------- start faning, red----------------
GPIO.output(red, True)
time.sleep(3)
GPIO.output(red, False)
pwm.start(50)

#----------- right, green ---------------------
GPIO.output(in1, True)
GPIO.output(in2, False)
GPIO.output(green, True)
time.sleep(5)
GPIO.output(green, False)

#---------- left, yellow ---------------------
GPIO.output(in1, False)
GPIO.output(in2, True)
GPIO.output(yellow, True)
time.sleep(5)
GPIO.output(yellow, False)


GPIO.cleanup()



