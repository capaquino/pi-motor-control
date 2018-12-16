import RPi.GPIO as gpio
from time import sleep

test_pin = 18

gpio.setmode(gpio.BOARD)
gpio.setup(test_pin, gpio.OUT)

gpio.output(test_pin, True)
sleep(5)
gpio.output(test_pin, False)

gpio.cleanup()
