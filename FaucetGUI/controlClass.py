
import sys
import pigpio

class control(object):
	
	def __init__(self):
		self.pi = pigpio.pi()
		self.freq = 50
		

	def setUp(self, pin):
		self.pi.set_PWM_frequency(pin, self.freq)	

	def move(self, pin, pwm):
		self.pi.set_PWM_dutycycle(pin, pwm)
	
		
		
