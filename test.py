import RPi.GPIO as gpio
from time import sleep, time

step_pin = 16
dir_pin = 18

SLEEP_TIME = 0.0001
direction = False # T:clockwise&close, F:counter-clockwise&open
gpio.setmode(gpio.BOARD)
gpio.setup(step_pin, gpio.OUT)
gpio.setup(dir_pin, gpio.OUT)

for x in range(6):
	gpio.output(dir_pin, direction)
	steps = 0
	# start = time()
	#  NEMA-17 Stepper Motor
	#  200  full stepping
	#  3200 1/16 microstepping

	while steps < 3200*3:
		gpio.output(step_pin, True)
		sleep(SLEEP_TIME)
		gpio.output(step_pin, False)
		sleep(SLEEP_TIME)
		steps = steps + 1
	direction = not direction

	# end = time()
	# print("{0} steps took {1}s".format(steps, end-start))

gpio.cleanup()

