
import sys
import time
from main import *
import settings

# I feel better having one of these

    # a new app instance

try:
	
	settings.init()
	app = QApplication(sys.argv)
	form = MainWindow()
	form.show()
	flag = 1

	# without this, the script exits immediately.
	sys.exit(app.exec_())
	while flag ==1:
            print('kappa')
finally:
	print("has quit")







