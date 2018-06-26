import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711
import csv
import numpy as np

def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()
    
while True:
    try:
        tic = time.time()
        time.sleep(1)
        toc = time.time()-tic
        print(toc)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()