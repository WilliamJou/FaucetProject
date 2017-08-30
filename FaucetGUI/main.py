# always seem to need this
import sys

# This gets the Qt stuff
import PyQt5
from PyQt5.QtWidgets import *
import settings
# This is our window from QtCreator
import mainwindow_auto
import time


# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    # access variables inside of the UI's file
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setupUi(self)  # gets defined in the UI file

        ##Listeners
        self.pushButton.clicked.connect(lambda: self.pushButtonClicked())
        self.cSlider.valueChanged.connect(lambda:self.cSliderMoved(self.cSlider.value()))
        self.txtTemp.returnPressed.connect(lambda:self.txtTempChanged(self.txtTemp.text()))
        print("testing")
###initialize GUI State

        ### setup pin numbers



    def pushButtonClicked(self):
        print("pushed!")
    def cSliderMoved(self, value):
        settings.servos[0].index = round(value/22.5)
        value = round(value/22.5)*22.5 #input = degrees, output scaled to 22.5 intervals
        self.cSlider.setValue(value)
        settings.servos[0].moveAngle(value)
        print(str(settings.temp[settings.servos[0].index][settings.servos[1].index]))
        self.txtTemp.setText(str(settings.temp[settings.servos[0].index][settings.servos[1].index])
        time.sleep(.750)
        if (settings.servos[0].prevAngle> value):
            settings.servos[0].moveAngle(value+4)
        else:
            settings.servos[0].moveAngle(value-4)

        print(value)
