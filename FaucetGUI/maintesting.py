# always seem to need this
import sys
import math
# This gets the Qt stuff
import PyQt5
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import settings
# This is our window from QtCreator
import mainwindow_auto
import mainwindow
import time
import traceback
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:
    finished - No data
    error - `tuple` (exctype, value, traceback.format_exc() )
    result - `object` data returned from processing, anything
    progress - `int` indicating % progress
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.channel = 7
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()


        # Add the callback to our kwargs
        kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, mainwindow.Ui_MainWindow):
    # access variables inside of the UI's file
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setupUi(self)  # gets defined in the UI file
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        #Initial State
        self.manualButton.setChecked(False)
        
        #Listeners
        self.manualButton.toggled.connect(lambda:self.oh_no())
        self.pshBut2.clicked.connect(lambda: self.oh_no())
        self.cSlider.valueChanged.connect(lambda:self.cSliderMoved(self.cSlider.value()))
        self.hSlider.valueChanged.connect(lambda:self.hSliderMoved(self.hSlider.value()))
        self.txtTemp.returnPressed.connect(lambda:self.txtTempChanged(self.txtTemp.text()))
        self.txtFlow.returnPressed.connect(lambda:self.txtFlowChanged(self.txtFlow.text()))
        self.c0.clicked.connect(lambda: self.c0Clicked())
        self.c1.clicked.connect(lambda: self.c1Clicked())
        self.c2.clicked.connect(lambda: self.c2Clicked())
        self.c3.clicked.connect(lambda: self.c3Clicked())
        self.c4.clicked.connect(lambda: self.c4Clicked())
        self.c5.clicked.connect(lambda: self.c5Clicked())
        self.c6.clicked.connect(lambda: self.c6Clicked())
        self.c7.clicked.connect(lambda: self.c7Clicked())
        self.c8.clicked.connect(lambda: self.c8Clicked())
        self.h0.clicked.connect(lambda: self.h0Clicked())
        self.h1.clicked.connect(lambda: self.h1Clicked())
        self.h2.clicked.connect(lambda: self.h2Clicked())
        self.h3.clicked.connect(lambda: self.h3Clicked())
        self.h4.clicked.connect(lambda: self.h4Clicked())
        self.h5.clicked.connect(lambda: self.h5Clicked())
        self.h6.clicked.connect(lambda: self.h6Clicked())
        self.h7.clicked.connect(lambda: self.h7Clicked())
        self.h8.clicked.connect(lambda: self.h8Clicked())
        self.b11.clicked.connect(lambda: self.b11Clicked())
        self.b12.clicked.connect(lambda: self.b12Clicked())
        self.b13.clicked.connect(lambda: self.b13Clicked())
        self.b14.clicked.connect(lambda: self.b14Clicked())
        self.b15.clicked.connect(lambda: self.b15Clicked())
        self.b16.clicked.connect(lambda: self.b16Clicked())
        self.b17.clicked.connect(lambda: self.b17Clicked())
        self.b18.clicked.connect(lambda: self.b18Clicked())
        self.b21.clicked.connect(lambda: self.b21Clicked())
        self.b22.clicked.connect(lambda: self.b22Clicked())
        self.b23.clicked.connect(lambda: self.b23Clicked())
        self.b24.clicked.connect(lambda: self.b24Clicked())
        self.b25.clicked.connect(lambda: self.b25Clicked())
        self.b26.clicked.connect(lambda: self.b26Clicked())
        self.b27.clicked.connect(lambda: self.b27Clicked())
        self.b28.clicked.connect(lambda: self.b28Clicked())
        self.b31.clicked.connect(lambda: self.b31Clicked())
        self.b32.clicked.connect(lambda: self.b32Clicked())
        self.b33.clicked.connect(lambda: self.b33Clicked())
        self.b34.clicked.connect(lambda: self.b34Clicked())
        self.b35.clicked.connect(lambda: self.b35Clicked())
        self.b36.clicked.connect(lambda: self.b36Clicked())
        self.b37.clicked.connect(lambda: self.b37Clicked())
        self.b38.clicked.connect(lambda: self.b38Clicked())
        self.b41.clicked.connect(lambda: self.b41Clicked())
        self.b42.clicked.connect(lambda: self.b42Clicked())
        self.b43.clicked.connect(lambda: self.b43Clicked())
        self.b44.clicked.connect(lambda: self.b44Clicked())
        self.b45.clicked.connect(lambda: self.b45Clicked())
        self.b46.clicked.connect(lambda: self.b46Clicked())
        self.b47.clicked.connect(lambda: self.b47Clicked())
        self.b48.clicked.connect(lambda: self.b48Clicked())
        self.b51.clicked.connect(lambda: self.b51Clicked())
        self.b52.clicked.connect(lambda: self.b52Clicked())
        self.b53.clicked.connect(lambda: self.b53Clicked())
        self.b54.clicked.connect(lambda: self.b54Clicked())
        self.b55.clicked.connect(lambda: self.b55Clicked())
        self.b56.clicked.connect(lambda: self.b56Clicked())
        self.b57.clicked.connect(lambda: self.b57Clicked())
        self.b58.clicked.connect(lambda: self.b58Clicked())
        self.b61.clicked.connect(lambda: self.b61Clicked())
        self.b62.clicked.connect(lambda: self.b62Clicked())
        self.b63.clicked.connect(lambda: self.b63Clicked())
        self.b64.clicked.connect(lambda: self.b64Clicked())
        self.b65.clicked.connect(lambda: self.b65Clicked())
        self.b66.clicked.connect(lambda: self.b66Clicked())
        self.b67.clicked.connect(lambda: self.b67Clicked())
        self.b68.clicked.connect(lambda: self.b68Clicked())
        self.b71.clicked.connect(lambda: self.b71Clicked())
        self.b72.clicked.connect(lambda: self.b72Clicked())
        self.b73.clicked.connect(lambda: self.b73Clicked())
        self.b74.clicked.connect(lambda: self.b74Clicked())
        self.b75.clicked.connect(lambda: self.b75Clicked())
        self.b76.clicked.connect(lambda: self.b76Clicked())
        self.b77.clicked.connect(lambda: self.b77Clicked())
        self.b78.clicked.connect(lambda: self.b78Clicked())
        self.b81.clicked.connect(lambda: self.b81Clicked())
        self.b82.clicked.connect(lambda: self.b82Clicked())
        self.b83.clicked.connect(lambda: self.b83Clicked())
        self.b84.clicked.connect(lambda: self.b84Clicked())
        self.b85.clicked.connect(lambda: self.b85Clicked())
        self.b86.clicked.connect(lambda: self.b86Clicked())
        self.b87.clicked.connect(lambda: self.b87Clicked())
        self.b88.clicked.connect(lambda: self.b88Clicked())
        self.channel = [6,7]
        CLK  = 23
        MISO = 10
        MOSI = 9
        CS   = 11
        self.mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
        #self.potRange = [[65,480],[10,480]]
        self.potRange = [[167,400],[0,204]]
        #180 --> 90
        self.prevPot = [self.scale(self.constrain(self.mcp.read_adc(self.channel[0]),self.potRange[0][0], self.potRange[0][1]), self.potRange[0][0], self.potRange[0][1] ,0, 90),
                        self.scale(self.constrain(self.mcp.read_adc(self.channel[1]),self.potRange[1][0], self.potRange[1][1]), self.potRange[1][0], self.potRange[1][1] ,0, 90)]
        settings.servos[0].movePWM(settings.servos[0].min+1)
        settings.servos[1].movePWM(settings.servos[1].min+1)
###Threaded Functions
    def scale(self, value, low, high, newlow, newhigh):
        newVal = newlow + (value-low)*(newhigh - newlow)/(high-low)
        return newVal
    def constrain(self, val, min_val, max_val):
        return min(max_val, max(min_val, val))
    def progress_fn(self,n):
        #settings.servos[0].movePWM(n)
        asdf=4

    def execute_this(self, progress_callback):
        while self.manualButton.isChecked():
            time.sleep(.5)
            #print('in manual loop')
            val = [0,0]
            #print('cold potentiometer value: ', self.mcp.read_adc(self.channel[0]))
            #print('hot potentiometer value: ', self.mcp.read_adc(self.channel[1]))
            for i in range (0,2):
                val[i] = int(self.mcp.read_adc(self.channel[i]))
                
                #print(i, 'this is testing constrain : ', self.constrain(val[i], self.potRange[0][0], self.potRange[0][1]))
                #val[i] = pwm value now
                
                #val[i]= self.scale(self.constrain(val[i], self.potRange[i][0], self.potRange[i][1]), self.potRange[i][0], self.potRange[i][1] ,settings.servos[i].min, settings.servos[i].max) #float pwm
                #print('value of i ', val[i])
                #180-->90
                if i == 0:
                    if (val[i]<=(self.potRange[i][0]+15)):
                        pot2deg = self.scale(self.constrain(val[i], self.potRange[i][0], self.potRange[i][1]),self.potRange[i][0], (self.potRange[i][0]+15), 0, 45)
                        Rounded = round(pot2deg/11.25)*11.25
                    else :
                        pot2deg = self.scale(self.constrain(val[i], self.potRange[i][0], self.potRange[i][1]), (self.potRange[i][0]+15), self.potRange[i][1], 45, 90)
                        Rounded = round(pot2deg/11.25)*11.25
                    print('Current Cold potentiometer reading of', pot2deg)
                    print('Previous Cold potentiometer value of', self.prevPot[i])
                    print(val[i])
                elif i == 1:
                    if (val[i]<=20):
                        #pot2deg = self.scale(self.constrain(val[i], self.potRange[i][0], self.potRange[i][1]),self.potRange[i][0], self.potRange[i][1], 0, 25)
                        pot2deg = round(val[i]/11.25)*11.25
                    else:
                        pot2deg = self.scale(self.constrain(val[i], self.potRange[i][0], self.potRange[i][1]), 20, self.potRange[i][1], 20, 90)
                        Rounded = round(pot2deg/11.25)*11.25
                    print('Current Hot potentiometer reading of', pot2deg)
                    print('Previous Hot potentiometer value of', self.prevPot[i])
                    print(val[i])
                    #print(i, 'Previous Potentiometer Value: ', self.prevPot[i])
                if abs(pot2deg -  self.prevPot[i]) > 5:
                    print('Handle Engaged', i)
                    print('Current Potentiometer Reading of', i, pot2deg)
                    print('Previous potentiometer value of', i, self.prevPot[i])
                    if i == 0:
                        #pot2deg = self.scale(self.constrain(self.mcp.read_adc(self.channel[i]), self.potRange[i][0], self.potRange[i][1]),self.potRange[i][0], self.potRange[i][1], 0, 180)
                        Rounded = round(pot2deg/11.25)*11.25
                        #val[i]= self.constrain(self.scale(val[i],self.potRange[0][0], self.potRange[1][0] ,settings.servos[0].min, settings.servos[0].max),0,180)
                        self.cSlider.setValue(Rounded)
                        print('Cold Handle set to :', Rounded)
                    if i == 1:
                        #pot2deg = self.scale(self.constrain(self.mcp.read_adc(self.channel[i]), self.potRange[i][0], self.potRange[i][1]),self.potRange[i][0], self.potRange[i][1], 0, 180)
                        Rounded = round(pot2deg/11.25)*11.25
                        #val[i]= self.constrain(self.scale(val[i],self.potRange[0][0], self.potRange[1][0] ,settings.servos[0].min, settings.servos[0].max),0,180)
                        self.hSlider.setValue(Rounded)
                    self.prevPot[i] = pot2deg
                    #Scales potentiometer reading into degrees
                    #settings.servos[i].prevAngle = self.scale(self.constrain(self.mcp.read_adc(self.channel[i]), self.potRange[i][0], self.potRange[i][1]), self.potRange[i][0], self.potRange[i][1], 0,180)
                #self.prevPot[i] = pot2deg
            progress_callback.emit(val)
            
        return "Done."
    def print_output(self,s):
        print(s)
    def thread_complete(self):
        print("THREAD COMPLETE")
    def oh_no(self):
        worker = Worker(self.execute_this)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
    
    def pushButtonClicked(self):
        print("pushed!")
        for i in range(0,2):
            print('Before Zeroing', i, self.prevPot[i])
        self.cSlider.setValue(0)
        self.hSlider.setValue(0)
        for i in range(0,2):
            print('After Zeroing', i, self.prevPot[i])
        time.sleep(0.5)
        
    def cSliderMoved(self, value):
        print('Cold Value set to:', value)
        #print('prevangle:', settings.servos[0].prevAngle)
        newAngle = 0
        settings.servos[0].index = int(round(value/11.25))
        #print('index: ', settings.servos[0].index)
        value = round(value/11.25)*11.25 #input = degrees, output scaled to 11.25 intervals
        #print('rounded value', value)
##        self.cSlider.setValue(value)
        #settings.servos[0].moveAngle(value)
        #print('temperature: ', (settings.servos[0].temp[settings.servos[0].index][settings.servos[1].index]))
        self.txtTemp.setText(str(settings.servos[0].temp[settings.servos[0].index][settings.servos[1].index]))
        #print('flow rate: ', (settings.servos[0].flow[settings.servos[0].index][settings.servos[1].index]))
        self.txtFlow.setText(str(settings.servos[0].flow[settings.servos[0].index][settings.servos[1].index]))
        #print('previous angle: ', settings.servos[0].prevAngle)
        #print('current value: ', value)
        if (settings.servos[0].prevAngle> value) and (abs(settings.servos[0].prevAngle-value)>7.5):
            settings.servos[0].moveAngle(value)
            print('First Cold MoveAngle: ', value)
            time.sleep(0.5)
            #180-->90
            newAngle = math.floor(settings.servos[0].scale(value,0,90,settings.servos[0].min, settings.servos[0].max))+1
            settings.servos[0].movePWM(newAngle)
            print('Second Cold movePWM: ', newAngle)
            settings.servos[0].prevAngle = value
            #print(newAngle)
        elif (settings.servos[0].prevAngle < value) and (abs(settings.servos[0].prevAngle-value)>7.5):
            settings.servos[0].moveAngle(value)
            print('First Cold MoveAngle: ', value)
            time.sleep(0.5)
            #180-->90
            newAngle = math.floor(settings.servos[0].scale(value,0,90,settings.servos[0].min, settings.servos[0].max))-1
            settings.servos[0].movePWM(newAngle)
            print('Second Cold movePWM: ', newAngle)
            settings.servos[0].prevAngle = value
            #print(newAngle)

        #settings.servos[0].prevAngle = value
    def hSliderMoved(self, value):
        
        newAngle = 0
        settings.servos[1].index = int(round(value/11.25))
        #print('cold servo index:', settings.servos[0].index)
        #print('hot servo index:', settings.servos[1].index)
        #print('index: ', settings.servos[1].index)
        value = round(value/11.25)*11.25 #input = degrees, output scaled to 11.25 intervals
        print(settings.servos[1].prevAngle)
        print(value)
        self.txtTemp.setText(str(settings.servos[0].temp[settings.servos[0].index][settings.servos[1].index]))
        self.txtFlow.setText(str(settings.servos[0].flow[settings.servos[0].index][settings.servos[1].index]))
        if (settings.servos[1].prevAngle> value) and (abs(settings.servos[1].prevAngle-value)>7.5):
            settings.servos[1].moveAngle(value)
            print('Hot Moved to:', value)
            time.sleep(0.5)
            #180-->90
            newAngle = math.floor(settings.servos[1].scale(value,0,90,settings.servos[1].min, settings.servos[1].max))+1
            settings.servos[1].movePWM(newAngle)
            settings.servos[1].prevAngle = value
        elif (settings.servos[1].prevAngle < value) and (abs(settings.servos[1].prevAngle-value)>7.5):
            settings.servos[1].moveAngle(value)
            print('Hot Moved to:', value)
            time.sleep(0.5)
            #180-->90
            newAngle = math.floor(settings.servos[1].scale(value,0,90,settings.servos[1].min, settings.servos[1].max))-1
            settings.servos[1].movePWM(newAngle)
            settings.servos[1].prevAngle = value
    #Gui Buttons
            #22.5-->11.25
    def c0Clicked(self):
        self.potRange[0][0] = int(self.mcp.read_adc(self.channel[0]))
        print('Cold lower Pot range set to: ', self.potRange[0][0])
    def c1Clicked(self):
        self.cSlider.setValue(1*11.25)
        self.hSlider.setValue(0)
    def c2Clicked(self):
        self.cSlider.setValue(2*11.25)
        self.hSlider.setValue(0)
    def c3Clicked(self):
        self.cSlider.setValue(3*11.25)
        self.hSlider.setValue(0)
    def c4Clicked(self):
        self.cSlider.setValue(4*11.25)
        self.hSlider.setValue(0)
    def c5Clicked(self):
        self.cSlider.setValue(5*11.25)
        self.hSlider.setValue(0)
    def c6Clicked(self):
        self.cSlider.setValue(6*11.25)
        self.hSlider.setValue(0)
    def c7Clicked(self):
        self.cSlider.setValue(7*11.25)
        self.hSlider.setValue(0)
    def c8Clicked(self):
        self.cSlider.setValue(8*11.25)
        self.hSlider.setValue(0)
    #Hot Buttons
    def h0Clicked(self):
        self.hSlider.setValue(0)
        self.cSlider.setValue(0)
    def h1Clicked(self):
        self.hSlider.setValue(1*11.25)
        self.cSlider.setValue(0)
    def h2Clicked(self):
        self.hSlider.setValue(2*11.25)
        self.cSlider.setValue(0)
    def h3Clicked(self):
        self.hSlider.setValue(3*11.25)
        self.cSlider.setValue(0)
    def h4Clicked(self):
        self.hSlider.setValue(4*11.25)
        self.cSlider.setValue(0)
    def h5Clicked(self):
        self.hSlider.setValue(5*11.25)
        self.cSlider.setValue(0)
    def h6Clicked(self):
        self.hSlider.setValue(6*11.25)
        self.cSlider.setValue(0)
    def h7Clicked(self):
        self.hSlider.setValue(7*11.25)
        self.cSlider.setValue(0)
    def h8Clicked(self):
        self.hSlider.setValue(8*11.25)
        self.cSlider.setValue(0)
    def b11Clicked(self):
        self.cSlider.setValue(1*11.25)
        self.hSlider.setValue(1*11.25)
    def b12Clicked(self):
        self.cSlider.setValue(1*11.25)
        self.hSlider.setValue(2*11.25)
    def b13Clicked(self):
        self.cSlider.setValue(1*11.25)
        self.hSlider.setValue(3*11.25)
    def b14Clicked(self):
        self.cSlider.setValue(1*11.25)
        self.hSlider.setValue(4*11.25)
    def b15Clicked(self):
        self.cSlider.setValue(1*11.25)
        self.hSlider.setValue(5*11.25)
    def b16Clicked(self):
        self.cSlider.setValue(1*11.25)
        self.hSlider.setValue(6*11.25)
    def b17Clicked(self):
        self.cSlider.setValue(1*11.25)
        self.hSlider.setValue(7*11.25)
    def b18Clicked(self):
        self.cSlider.setValue(1*11.25)
        self.hSlider.setValue(8*11.25)
    def b21Clicked(self):
        self.cSlider.setValue(2*11.25)
        self.hSlider.setValue(1*11.25)
    def b22Clicked(self):
        self.cSlider.setValue(2*11.25)
        self.hSlider.setValue(2*11.25)
    def b23Clicked(self):
        self.cSlider.setValue(2*11.25)
        self.hSlider.setValue(3*11.25)
    def b24Clicked(self):
        self.cSlider.setValue(2*11.25)
        self.hSlider.setValue(4*11.25)
    def b25Clicked(self):
        self.cSlider.setValue(2*11.25)
        self.hSlider.setValue(5*11.25)
    def b26Clicked(self):
        self.cSlider.setValue(2*11.25)
        self.hSlider.setValue(6*11.25)
    def b27Clicked(self):
        self.cSlider.setValue(2*11.25)
        self.hSlider.setValue(7*11.25)
    def b28Clicked(self):
        self.cSlider.setValue(2*11.25)
        self.hSlider.setValue(8*11.25)
    def b31Clicked(self):
        self.cSlider.setValue(3*11.25)
        self.hSlider.setValue(1*11.25)
    def b32Clicked(self):
        self.cSlider.setValue(3*11.25)
        self.hSlider.setValue(2*11.25)
    def b33Clicked(self):
        self.cSlider.setValue(3*11.25)
        self.hSlider.setValue(3*11.25)
    def b34Clicked(self):
        self.cSlider.setValue(3*11.25)
        self.hSlider.setValue(4*11.25)
    def b35Clicked(self):
        self.cSlider.setValue(3*11.25)
        self.hSlider.setValue(5*11.25)
    def b36Clicked(self):
        self.cSlider.setValue(3*11.25)
        self.hSlider.setValue(6*11.25)
    def b37Clicked(self):
        self.cSlider.setValue(3*11.25)
        self.hSlider.setValue(7*11.25)
    def b38Clicked(self):
        self.cSlider.setValue(3*11.25)
        self.hSlider.setValue(8*11.25)
    def b41Clicked(self):
        self.cSlider.setValue(4*11.25)
        self.hSlider.setValue(1*11.25)
    def b42Clicked(self):
        self.cSlider.setValue(4*11.25)
        self.hSlider.setValue(2*11.25)
    def b43Clicked(self):
        self.cSlider.setValue(4*11.25)
        self.hSlider.setValue(3*11.25)
    def b44Clicked(self):
        self.cSlider.setValue(4*11.25)
        self.hSlider.setValue(4*11.25)
    def b45Clicked(self):
        self.cSlider.setValue(4*11.25)
        self.hSlider.setValue(5*11.25)
    def b46Clicked(self):
        self.cSlider.setValue(4*11.25)
        self.hSlider.setValue(6*11.25)
    def b47Clicked(self):
        self.cSlider.setValue(4*11.25)
        self.hSlider.setValue(7*11.25)
    def b48Clicked(self):
        self.cSlider.setValue(4*11.25)
        self.hSlider.setValue(8*11.25)
    def b51Clicked(self):
        self.cSlider.setValue(5*11.25)
        self.hSlider.setValue(1*11.25)
    def b52Clicked(self):
        self.cSlider.setValue(5*11.25)
        self.hSlider.setValue(2*11.25)
    def b53Clicked(self):
        self.cSlider.setValue(5*11.25)
        self.hSlider.setValue(3*11.25)
    def b54Clicked(self):
        self.cSlider.setValue(5*11.25)
        self.hSlider.setValue(4*11.25)
    def b55Clicked(self):
        self.cSlider.setValue(5*11.25)
        self.hSlider.setValue(5*11.25)
    def b56Clicked(self):
        self.cSlider.setValue(5*11.25)
        self.hSlider.setValue(6*11.25)
    def b57Clicked(self):
        self.cSlider.setValue(5*11.25)
        self.hSlider.setValue(7*11.25)
    def b58Clicked(self):
        self.cSlider.setValue(5*11.25)
        self.hSlider.setValue(8*11.25)
    def b61Clicked(self):
        self.cSlider.setValue(6*11.25)
        self.hSlider.setValue(1*11.25)
    def b62Clicked(self):
        self.cSlider.setValue(6*11.25)
        self.hSlider.setValue(2*11.25)
    def b63Clicked(self):
        self.cSlider.setValue(6*11.25)
        self.hSlider.setValue(3*11.25)
    def b64Clicked(self):
        self.cSlider.setValue(6*11.25)
        self.hSlider.setValue(4*11.25)
    def b65Clicked(self):
        self.cSlider.setValue(6*11.25)
        self.hSlider.setValue(5*11.25)
    def b66Clicked(self):
        self.cSlider.setValue(6*11.25)
        self.hSlider.setValue(6*11.25)
    def b67Clicked(self):
        self.cSlider.setValue(6*11.25)
        self.hSlider.setValue(7*11.25)
    def b68Clicked(self):
        self.cSlider.setValue(6*11.25)
        self.hSlider.setValue(8*11.25)
    def b71Clicked(self):
        self.cSlider.setValue(7*11.25)
        self.hSlider.setValue(1*11.25)
    def b72Clicked(self):
        self.cSlider.setValue(7*11.25)
        self.hSlider.setValue(2*11.25)
    def b73Clicked(self):
        self.cSlider.setValue(7*11.25)
        self.hSlider.setValue(3*11.25)
    def b74Clicked(self):
        self.cSlider.setValue(7*11.25)
        self.hSlider.setValue(4*11.25)
    def b75Clicked(self):
        self.cSlider.setValue(7*11.25)
        self.hSlider.setValue(5*11.25)
    def b76Clicked(self):
        self.cSlider.setValue(7*11.25)
        self.hSlider.setValue(6*11.25)
    def b77Clicked(self):
        self.cSlider.setValue(7*11.25)
        self.hSlider.setValue(7*11.25)
    def b78Clicked(self):
        self.cSlider.setValue(7*11.25)
        self.hSlider.setValue(8*11.25)
    def b81Clicked(self):
        self.cSlider.setValue(8*11.25)
        self.hSlider.setValue(1*11.25)
    def b82Clicked(self):
        self.cSlider.setValue(8*11.25)
        self.hSlider.setValue(2*11.25)
    def b83Clicked(self):
        self.cSlider.setValue(8*11.25)
        self.hSlider.setValue(3*11.25)
    def b84Clicked(self):
        self.cSlider.setValue(8*11.25)
        self.hSlider.setValue(4*11.25)
    def b85Clicked(self):
        self.cSlider.setValue(8*11.25)
        self.hSlider.setValue(5*11.25)
    def b86Clicked(self):
        self.cSlider.setValue(8*11.25)
        self.hSlider.setValue(6*11.25)
    def b87Clicked(self):
        self.cSlider.setValue(8*11.25)
        self.hSlider.setValue(7*11.25)
    def b88Clicked(self):
        self.cSlider.setValue(8*11.25)
        self.hSlider.setValue(8*11.25)        
        

