
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

	cservo = servo(24 , 10, 32, "right")
	hservo = servo(22 , 8, 32, "left")

	global servos
	servos = [cservo,hservo]
	temp = [
[0, 26, 26, 26, 52, 50, 47, 46, 44],
[25, 26, 25, 26, 51, 48, 45, 44, 44],
[25, 26, 25, 26, 48, 43, 44, 44, 44],
[26, 26, 25, 26, 45, 43, 43, 42, 43],
[25, 25, 26, 26, 40, 42, 42, 42, 42],
[25, 26, 25, 26, 40, 42, 42, 41, 42],
[25, 25, 26, 26, 42, 41, 40, 42, 43],
[25, 26, 26, 26, 41, 43, 41, 41, 42],
[25, 26, 26, 26, 41, 41, 42, 42, 41]
]
	flowrate = [
[0, 5, 20, 36, 56, 68, 71, 71, 75],
[5, 14, 23, 47, 63, 73, 77, 79, 81],
[19, 26, 31, 57, 81, 87, 87, 82, 86],
[40, 49, 52, 79, 90, 96, 97, 97, 97],
[53, 60, 65, 84, 92, 92, 95, 97, 99],
[60, 66, 76, 90, 99, 100, 99, 97, 99],
[61, 67, 76,  89, 97, 103, 104,  100, 100],
[62, 71, 75, 93, 99, 103, 100, 100, 103],
[64, 69, 78, 95, 97, 101, 104, 100, 103]
]
