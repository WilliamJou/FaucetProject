# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(890, 560)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 150, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.cSlider = QtWidgets.QSlider(self.centralWidget)
        self.cSlider.setGeometry(QtCore.QRect(540, 310, 261, 22))
        self.cSlider.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.cSlider.setMaximum(180)
        self.cSlider.setSingleStep(22)
        self.cSlider.setPageStep(22)
        self.cSlider.setProperty("value", 0)
        self.cSlider.setOrientation(QtCore.Qt.Horizontal)
        self.cSlider.setInvertedAppearance(False)
        self.cSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.cSlider.setObjectName("cSlider")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(290, 250, 131, 41))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.txtTemp = QtWidgets.QLineEdit(self.centralWidget)
        self.txtTemp.setGeometry(QtCore.QRect(290, 210, 131, 31))
        self.txtTemp.setObjectName("txtTemp")
        self.txtFlow = QtWidgets.QLineEdit(self.centralWidget)
        self.txtFlow.setGeometry(QtCore.QRect(440, 210, 151, 31))
        self.txtFlow.setObjectName("txtFlow")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(450, 250, 131, 41))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(610, 340, 131, 41))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.hSlider = QtWidgets.QSlider(self.centralWidget)
        self.hSlider.setGeometry(QtCore.QRect(120, 310, 261, 22))
        self.hSlider.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.hSlider.setMaximum(180)
        self.hSlider.setSingleStep(22)
        self.hSlider.setPageStep(22)
        self.hSlider.setProperty("value", 0)
        self.hSlider.setOrientation(QtCore.Qt.Horizontal)
        self.hSlider.setInvertedAppearance(False)
        self.hSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.hSlider.setObjectName("hSlider")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(180, 350, 131, 41))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.manualButton = QtWidgets.QRadioButton(self.centralWidget)
        self.manualButton.setGeometry(QtCore.QRect(110, 100, 261, 41))
        self.manualButton.setObjectName("manualButton")
        self.pshBut2 = QtWidgets.QPushButton(self.centralWidget)
        self.pshBut2.setGeometry(QtCore.QRect(550, 150, 91, 29))
        self.pshBut2.setObjectName("pshBut2")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 890, 26))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "please work"))
        self.label.setText(_translate("MainWindow", "Temperature (C)"))
        self.label_2.setText(_translate("MainWindow", "Flow Rate"))
        self.label_3.setText(_translate("MainWindow", "Cold"))
        self.label_4.setText(_translate("MainWindow", "Hot"))
        self.manualButton.setText(_translate("MainWindow", "Faucet Handle Control"))
        self.pshBut2.setText(_translate("MainWindow", "PushButton"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

