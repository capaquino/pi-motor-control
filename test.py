import RPi.GPIO as gpio
from time import sleep


step_pin = 16
dir_pin = 18
SLEEP_TIME = 0.0001

gpio.setmode(gpio.BOARD)
gpio.setup(step_pin, gpio.OUT)
gpio.setup(dir_pin, gpio.OUT)

gpio.output(dir_pin, False)
distance = 0

while distance < 3200:
	gpio.output(step_pin, True)
	sleep(SLEEP_TIME)
	gpio.output(step_pin, False)
	sleep(SLEEP_TIME)
	distance = distance + 1

gpio.cleanup()

