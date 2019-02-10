# Applies python3 style division to module
from __future__ import division

import gpiozero
from time import sleep
from enum import Enum

BoardPins = {
	3 : 2, # SDA
	5 : 3, # SCL
	7 : 4, # GPCLK0
	8 : 14, # TXD
	10 : 15, # RXD
	11 : 17,
	12 : 18, # PWM0
	13 : 27,
	15 : 22,
	16 : 23,
	18 : 24,
	19 : 10, # MOSI
	21 : 9, # MISO
	22 : 25,
	23 : 11, # SCLK
	24 : 8, # CE0
	26 : 7, # CE1
	27 : 0, # EEPROM Data
	28 : 1, # EEPROM Clock
	29 : 5,
	31 : 6,
	32 : 12, # PWM0
	33 : 13, # PWM1
	35 : 19, # MISO
	36 : 16,
	37 : 26,
	38 : 20, # MOSI
	40 : 21 # SCLK
}

# Call using Board.PXX.value
# Don't really like the syntax as much as the dictionary.
class Board(Enum):
	P3 = 2 # SDA
	P5 = 3 # SCL
	P7 = 4 # GPCLK0
	P8 = 14 # TXD
	P10 = 15 # RXD
	P11 = 17
	P12 = 18 # PWM0
	P13 = 27
	P15 = 22
	P16 = 23
	P18 = 24
	P19 = 10 # MOSI
	P21 = 9 # MISO
	P22 = 25
	P23 = 11 # SCLK
	P24 = 8 # CE0
	P26 = 7 # CE1
	P27 = 0 # EEPROM Data
	P28 = 1 # EEPROM Clock
	P29 = 5
	P31 = 6
	P32 = 12 # PWM0
	P33 = 13 # PWM1
	P35 = 19 # MISO
	P36 = 16
	P37 = 26
	P38 = 20 # MOSI
	P40 = 21 # SCLK

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
				# Generate pulse train
				pulse.on()
				sleep( 1 / (self.frequency * 2) )
				pulse.off()
				sleep( 1.0 / (self.frequency * 2) )
				# Update relevant values
				distMoved_steps += 1

		except Exception as e:
			# Re-raise exception
			raise
		finally:
			# Update current position with actual distance moved
			if dir.value > 0:
				self.currentPosition += distMoved_steps
			else:
				self.currentPosition -= distMoved_steps
			# Cleanup
			pulse.off()
			dir.off()
			pulse.close()
			dir.close()

	def MoveAbs(self, targetPosition_steps):
		pass

# gpiozero uses BCM numbering, not changeable to BOARD numbering
# BCM 23 = step pin = 16
# BCM 24 = dir pin = 18
if __name__ == '__main__':
	s = Stepper(Board[16], Board[18], 3200)
	s.MoveRel(3200)
	print(s.currentPosition)
	s.MoveRel(3200)
	print(s.currentPosition)
	s.MoveRel(-3200)
	print(s.currentPosition)
