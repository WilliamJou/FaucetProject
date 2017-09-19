
import sys
import pigpio
import time
import settings


class servo(object):

	def __init__(self, pin, min, max, direction):
		self.direction = direction
		self.pin = pin
		self.angle = 0
		self.pwm = 0
		self.min = min
		self.max = max
		self.prevAngle = 0
		self.index = 0
		self.temp = [[0, 26, 26, 26, 52, 50, 47, 46, 44],
                             [25, 26, 25, 26, 51, 48, 45, 44, 44],
                [25, 26, 25, 26, 48, 43, 44, 44, 44],
                [26, 26, 25, 26, 45, 43, 43, 42, 43],
                [25, 25, 26, 26, 40, 42, 42, 42, 42],
                [25, 26, 25, 26, 40, 42, 42, 41, 42],
                [25, 25, 26, 26, 42, 41, 40, 42, 43],
                [25, 26, 26, 26, 41, 43, 41, 41, 42],
                [25, 26, 26, 26, 41, 41, 42, 42, 41]]
		
		self.flow= [[0, 5, 20, 36, 56, 68, 71, 71, 75],
                            [5, 14, 23, 47, 63, 73, 77, 79, 81],
                [19, 26, 31, 57, 81, 87, 87, 82, 86],
                [40, 49, 52, 79, 90, 96, 97, 97, 97],
                [53, 60, 65, 84, 92, 92, 95, 97, 99],
                [60, 66, 76, 90, 99, 100, 99, 97, 99],
                [61, 67, 76,  89, 97, 103, 104,  100, 100],
                [62, 71, 75, 93, 99, 103, 100, 100, 103],
                [64, 69, 78, 95, 97, 101, 104, 100, 103]]
		settings.mainControl.setUp(self.pin)
		self.moveAngle(self.angle)

	def scale(self, value, low, high, newlow, newhigh):
		newVal = newlow + (value-low)*(newhigh - newlow)/(high-low)
		return newVal
		
	def moveAngle(self, angle):
            if (self.direction == "cw"):
                self.angle = angle
                print('pwm:', self.pwm)
                print(angle)
                #print(self.min, self.max)
                self.pwm = self.scale(angle,0,180,self.min, self.max)
                print('pwm: ', self.pwm)
                settings.mainControl.move(self.pin, self.pwm)
            elif (self.direction == "ccw"):
                self.angle = angle
                self.pwm = self.scale(angle,180,0,self.min, self.max)
                print('pwm: ', self.pwm)
                settings.mainControl.move(self.pin, self.pwm)               
                
	def movePWM(self, pwm):
            if (self.direction == "cw"):
                self.angle = (pwm - self.min) / (self.max - self.min) * 180 - 90
                settings.mainControl.move(self.pin, pwm)
            elif (self.direction =="ccw"):
                settings.mainControl.move(self.pin, (self.max-pwm+self.min))

	def movePer(self, per):
		self.angle = (180 * per / 100) - 90
		self.pwm = (self.max - self.min) * per / 100 + self.min
		self.per = per
		settings.mainControl.move(self.pin, self.pwm)