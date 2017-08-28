
import sys
import pigpio
import settings


class servo(object):
	
	def __init__(self, pin, number, mini, maxi, direction):
		self.direction = direction
		self.max = maxi
		self.min = mini
		self.number = number
		self.pin = pin

		self.angle = 0
		self.pwm = (maxi - mini)/2
		self.per = 50
	
		settings.mainControl.setUp(self.pin)

		self.moveAngle(self.angle)

		

	def moveAngle(self, angle):
		self.angle = angle
		self.pwm = self.min + (self.max - self.min) * ((angle + 90)/ 180)
		if (self.direction == "right"):
			self.per = 100 - (angle + 90) / 1.8	
		else:	
			self.per = (angle + 90) / 1.8
		settings.mainControl.move(self.pin, self.pwm)

	def movePWM(self, pwm):
		self.angle = (pwm - self.min) / (self.max - self.min) * 180 - 90
		self.per = (pwm - self.min) / (self.max - self.min) * 100
		settings.mainControl.move(self.pin, self.pwm)


	def movePer(self, per):
		self.angle = (180 * per / 100) - 90
		self.pwm = (self.max - self.min) * per / 100 + self.min
		self.per = per
		settings.mainControl.move(self.pin, self.pwm)
