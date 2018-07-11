
import sys
import pigpio

from controlClass import control
from servoClass import servo

def init():
	#ex:

	#global varName
	#varName = varNameClass()

	#import settings into other scripts
	#refer to global variable by "settings.varName"

	global mainControl
	mainControl = control()

	#cservo = servo(24 , 10, 32, "cw")
	cservo = servo(24 , 7, 28, "cw")
	hservo = servo(22 , 6, 32, "ccw")

	global servos
	servos = [cservo,hservo]
	
	
