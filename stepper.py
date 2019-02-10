import gpiozero
from time import sleep
# from enum import Enum # for init types?


class Stepper(object):
	def __init__(self, stepPin_pin, dirPin_pin, frequency_hz):
		self.stepPin = stepPin_pin
		self.dirPin = dirPin_pin
		self.SetFrequency(frequency_hz)
		self.homePosition = 0
		self.currentPosition = 0
		pass

	def Home(self, initializationType):
		if initializationType == 0:
			self.homePosition = 0
			self.currentPosition = 0
			pass
		else:
			raise Value("Invalid initialization type.")
		pass

	def SetFrequency(self, frequency_hz):
		if frequency_hz < 0:
			raise ValueError("Frequency cannot be negative.")
		self.frequency = frequency_hz
		pass

	def MoveRel(self, moveDist_steps):
		# Set up move
		distMoved_steps = 0

		try:
			# Assign pin that pulse train will be on
			pulse = gpiozero.DigitalOutputDevice(self.stepPin)
			# Assign pin based on direction of move (positive/clockwise, negative/counterclockwise)
			if moveDist_steps > 0:
				dir = gpiozero.DigitalOutputDevice(self.dirPin, initial_value = True)
			else:
				dir = gpiozero.DigitalOutputDevice(self.dirPin) # initial_value = False
			# Do move
			while distMoved_steps < abs(moveDist_steps):
				pulse.on()
				sleep(1/(self.frequency*2))
				pulse.off()
				sleep(1/(self.frequency*2))
				# Update relevant values
				distMoved_steps += 1

		except Exception as e:
			# Re-raise exception
			raise
		finally:
			# Update current position
			if dir.value > 0:
				self.currentPosition += distMoved_steps
			else:
				self.currentPosition -= distMoved_steps
			# Cleanup
			pulse.off()
			dir.off()
			pulse.close()
			dir.close()

# TODO Make a BOARD pin numbering library or enum for GPIO. gpiozero uses BCM numbering


# BCM 23 = step pin = 16
# BCM 24 = dir pin = 18
if __name__ == '__main__':
	s = Stepper(23, 24, 1000)
	s.MoveRel(3200)
	print(s.currentPosition)
	s.MoveRel(3200)
	print(s.currentPosition)
	s.MoveRel(-3200)
	print(s.currentPosition)
