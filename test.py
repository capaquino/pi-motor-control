import RPi.GPIO as gpio
from time import sleep, time


step_pin = 16
dir_pin = 18
SLEEP_TIME = 0.001 #0.0001 for microstepping, how is this determined to not torque out.
direction = False # clockwise?
rotations = 2

gpio.setmode(gpio.BOARD)
gpio.setup(step_pin, gpio.OUT)
gpio.setup(dir_pin, gpio.OUT)

gpio.output(dir_pin, direction)
steps = 0

start = time()

#  NEMA-17 Stepper Motor
#  200  full stepping
#  3200 1/16 microstepping

while steps < 3200*rotations:
	gpio.output(step_pin, True)
	sleep(SLEEP_TIME)
	gpio.output(step_pin, False)
	sleep(SLEEP_TIME)
	steps = steps + 1

end = time()
print("{0} rotations took {1}s".format(rotations, end-start))

gpio.cleanup()

