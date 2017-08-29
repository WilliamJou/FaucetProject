
import sys
import pigpio
import settings


class servo(object):
	
	def __init__(self, pin, direction):
		self.direction = direction
		self.pin = pin
		self.angle = 0
		self.pwm = 0
		self.per = 50
	
		settings.mainControl.setUp(self.pin)

		self.moveAngle(self.angle)

	def scale(self, value, low, high, newlow, newhigh):
		newVal = newlow + (newhigh - newlow)/(high-low)*(value-low)
		return newVal

	def moveAngle(self, angle):
		self.angle = angle
		self.pwm = self.scale(angle,0,180,0,255)
		settings.mainControl.move(self.pin, self.pwm)

	'''def movePWM(self, pwm):
		self.angle = (pwm - self.min) / (self.max - self.min) * 180 - 90
		self.per = (pwm - self.min) / (self.max - self.min) * 100
		settings.mainControl.move(self.pin, self.pwm)


	def movePer(self, per):
		self.angle = (180 * per / 100) - 90
		self.pwm = (self.max - self.min) * per / 100 + self.min
		self.per = per
		settings.mainControl.move(self.pin, self.pwm)'''
