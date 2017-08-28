
import sys
import time
import random
from main import *
from controlClass import controller
import RPi.GPIO as GPIO
import settings

# I feel better having one of these

    # a new app instance

try:
	
	settings.init()
	app = QApplication(sys.argv)
	form = MainWindow()
	form.show()
	# without this, the script exits immediately.
	sys.exit(app.exec_())

finally:
	print("has quit")
	GPIO.cleanup()






