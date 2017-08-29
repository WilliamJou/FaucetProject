# always seem to need this
import sys

# This gets the Qt stuff
import PyQt5
from PyQt5.QtWidgets import *
import settings
# This is our window from QtCreator
import mainwindow_auto


# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
    # access variables inside of the UI's file
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setupUi(self)  # gets defined in the UI file
        self.pushButton.clicked.connect(lambda: self.pushButtonClicked())
        print("testing")
###initialize GUI State

        ### setup pin numbers



    def pushButtonClicked(self):
        print("pushed!")
    def cSliderMoved(self, value):
        settings.mainControl.move(servos[1], value)

