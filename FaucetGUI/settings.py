
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
	
	cservo = servo(24 ,8, 32, "right")
	hservo = servo(22 , 8, 32, "left")
	
	global servos
	servos = [cservo, hservo]
	
