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
        self.pushButton.clicked.connect(lambda: self.pushButtonClicked())
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
        self.channel = [6,7]
        CLK  = 23
        MISO = 10
        MOSI = 9
        CS   = 11
        self.mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
        self.potRange = [[250,660],[0,410]]
        self.prevPot = [self.scale(self.constrain(self.mcp.read_adc(self.channel[0]),self.potRange[0][0], self.potRange[0][1]), self.potRange[0][0], self.potRange[0][1] ,0, 180),
                        self.scale(self.constrain(self.mcp.read_adc(self.channel[1]),self.potRange[1][0], self.potRange[1][1]), self.potRange[1][0], self.potRange[1][1] ,0, 180)]
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
                pot2deg = self.scale(self.constrain(val[i], self.potRange[i][0], self.potRange[i][1]),self.potRange[i][0], self.potRange[i][1], 0, 180)
                Rounded = round(pot2deg/22.5)*22.5

                print('Current Potentiometer Reading of', i, pot2deg)
                print('Previous potentiometer value of', i, self.prevPot[i])
                #print(i, 'Previous Potentiometer Value: ', self.prevPot[i])
                if abs(pot2deg -  self.prevPot[i]) > 5:
                    print('Handle Engaged', i)
                    print('Current Potentiometer Reading of', i, pot2deg)
                    print('Previous potentiometer value of', i, self.prevPot[i])
                    if i == 0:
                        #pot2deg = self.scale(self.constrain(self.mcp.read_adc(self.channel[i]), self.potRange[i][0], self.potRange[i][1]),self.potRange[i][0], self.potRange[i][1], 0, 180)
                        Rounded = round(pot2deg/22.5)*22.5
                        #val[i]= self.constrain(self.scale(val[i],self.potRange[0][0], self.potRange[1][0] ,settings.servos[0].min, settings.servos[0].max),0,180)
                        self.cSlider.setValue(Rounded)
                    if i == 1:
                        #pot2deg = self.scale(self.constrain(self.mcp.read_adc(self.channel[i]), self.potRange[i][0], self.potRange[i][1]),self.potRange[i][0], self.potRange[i][1], 0, 180)
                        Rounded = round(pot2deg/22.5)*22.5
                        #val[i]= self.constrain(self.scale(val[i],self.potRange[0][0], self.potRange[1][0] ,settings.servos[0].min, settings.servos[0].max),0,180)
                        self.hSlider.setValue(Rounded)
                    self.prevPot[i] = pot2deg
                    #Scales potentiometer reading into degrees
                    #settings.servos[i].prevAngle = self.scale(self.constrain(self.mcp.read_adc(self.channel[i]), self.potRange[i][0], self.potRange[i][1]), self.potRange[i][0], self.potRange[i][1], 0,180)
                self.prevPot[i] = pot2deg
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
### Gui Functions
    def c0Clicked(self):
        self.cSlider.setValue(0)
    def c1Clicked(self):
        self.cSlider.setValue(1*22.5)
    def c2Clicked(self):
        self.cSlider.setValue(2*22.5)
    def c3Clicked(self):
        self.cSlider.setValue(3*22.5)
    def c4Clicked(self):
        self.cSlider.setValue(4*22.5)
    def c5Clicked(self):
        self.cSlider.setValue(5*22.5)
    def c6Clicked(self):
        self.cSlider.setValue(6*22.5)
    def c7Clicked(self):
        self.cSlider.setValue(7*22.5)
    def c8Clicked(self):
        self.cSlider.setValue(8*22.5)
    #Hot Buttons
    def h0Clicked(self):
        self.hSlider.setValue(0)
    def h1Clicked(self):
        self.hSlider.setValue(1*22.5)
    def h2Clicked(self):
        self.hSlider.setValue(2*22.5)
    def h3Clicked(self):
        self.hSlider.setValue(3*22.5)
    def h4Clicked(self):
        self.hSlider.setValue(4*22.5)
    def h5Clicked(self):
        self.hSlider.setValue(5*22.5)
    def h6Clicked(self):
        self.hSlider.setValue(6*22.5)
    def h7Clicked(self):
        self.hSlider.setValue(7*22.5)
    def h8Clicked(self):
        self.hSlider.setValue(8*22.5)    
    def pushButtonClicked(self):
        print("pushed!")
        for i in range(0,2):
            print('Before Zeroing', i, self.prevPot[i])
        self.cSlider.setValue(0)
        self.hSlider.setValue(0)
        for i in range(0,2):
            print('After Zeroing', i, self.prevPot[i])
        time.sleep(1)
        
    def cSliderMoved(self, value):
        print('Cold Value set to:', value)
        #print('prevangle:', settings.servos[0].prevAngle)
        newAngle = 0
        settings.servos[0].index = int(round(value/22.5))
        #print('index: ', settings.servos[0].index)
        value = round(value/22.5)*22.5 #input = degrees, output scaled to 22.5 intervals
        #print('rounded value', value)
##        self.cSlider.setValue(value)
        #settings.servos[0].moveAngle(value)
        #print('temperature: ', (settings.servos[0].temp[settings.servos[0].index][settings.servos[1].index]))
        self.txtTemp.setText(str(settings.servos[0].temp[settings.servos[0].index][settings.servos[1].index]))
        #print('flow rate: ', (settings.servos[0].flow[settings.servos[0].index][settings.servos[1].index]))
        self.txtFlow.setText(str(settings.servos[0].flow[settings.servos[0].index][settings.servos[1].index]))
        #print('previous angle: ', settings.servos[0].prevAngle)
        #print('current value: ', value)
        if (settings.servos[0].prevAngle> value) and (abs(settings.servos[0].prevAngle-value)>12.5):
            settings.servos[0].moveAngle(value)
            time.sleep(.5)
            newAngle = math.floor(settings.servos[0].scale(value,0,180,settings.servos[0].min, settings.servos[0].max))+1
            settings.servos[0].movePWM(newAngle)
            print('close')
            settings.servos[0].prevAngle = value
            #print(newAngle)
        elif (settings.servos[0].prevAngle < value) and (abs(settings.servos[0].prevAngle-value)>12.5):
            settings.servos[0].moveAngle(value)
            time.sleep(.5)
            newAngle = math.floor(settings.servos[0].scale(value,0,180,settings.servos[0].min, settings.servos[0].max))-1
            settings.servos[0].movePWM(newAngle)
            print('open')
            settings.servos[0].prevAngle = value
            #print(newAngle)

        #settings.servos[0].prevAngle = value
    
    #Hot Slider
    
    def hSliderMoved(self, value):
        
        newAngle = 0
        settings.servos[1].index = int(round(value/22.5))
        #print('cold servo index:', settings.servos[0].index)
        #print('hot servo index:', settings.servos[1].index)
        #print('index: ', settings.servos[1].index)
        value = round(value/22.5)*22.5 #input = degrees, output scaled to 22.5 intervals
##        self.cSlider.setValue(value)
        #settings.servos[1].moveAngle(value)
## update output values        
        #print('temperature: ', (settings.servos[0].temp[settings.servos[0].index][settings.servos[1].index]))
        self.txtTemp.setText(str(settings.servos[0].temp[settings.servos[0].index][settings.servos[1].index]))
        #print('flow rate: ', (settings.servos[0].flow[settings.servos[0].index][settings.servos[1].index]))
        self.txtFlow.setText(str(settings.servos[0].flow[settings.servos[0].index][settings.servos[1].index]))
        if (settings.servos[1].prevAngle> value) and (abs(settings.servos[1].prevAngle-value)>12.5):
            settings.servos[1].moveAngle(value)
            print('Hot Moved to:', value)
            time.sleep(.5)
            newAngle = math.floor(settings.servos[1].scale(value,0,180,settings.servos[1].min, settings.servos[1].max))+1
            settings.servos[1].movePWM(newAngle)
            settings.servos[1].prevAngle = value
        elif (settings.servos[1].prevAngle < value) and (abs(settings.servos[1].prevAngle-value)>12.5):
            settings.servos[1].moveAngle(value)
            print('Hot Moved to:', value)
            time.sleep(.5)
            newAngle = math.floor(settings.servos[1].scale(value,0,180,settings.servos[1].min, settings.servos[1].max))-1
            settings.servos[1].movePWM(newAngle)
            settings.servos[1].prevAngle = value
        

