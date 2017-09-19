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
class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):
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
        self.channel = [6,7]
        CLK  = 23
        MISO = 10
        MOSI = 9
        CS   = 11
        self.mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
        self.potRange = [[250,660],[10,20]]
        self.prevPot = [self.scale(self.constrain(self.mcp.read_adc(self.channel[0]),self.potRange[0][0], self.potRange[0][1]), self.potRange[0][0], self.potRange[1][0] ,settings.servos[0].min, settings.servos[0].max),self.mcp.read_adc(self.channel[1])]
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
            time.sleep(1)
            print('in manual loop')
            val = [0,0]
            print('potentiometer value: ', self.mcp.read_adc(self.channel[0]))
            for i in range (0,1):
                val[i] = int(self.mcp.read_adc(self.channel[i]))
                print('this is testing constrain: ', self.constrain(val[i], self.potRange[0][0], self.potRange[0][1]))
                val[i]= self.scale(self.constrain(val[i], self.potRange[0][0], self.potRange[0][1]), self.potRange[0][0], self.potRange[0][1] ,settings.servos[0].min, settings.servos[0].max) #float pwm
                print('with constraints val[i]: ', val[i])
                print('Previous Potentiometer Value: ', self.prevPot[0])
                if abs(val[i] -  self.prevPot[i]) > 1:
                    print('turned faucet handle')
                    if i == 0:
                        #val[i]= self.constrain(self.scale(val[i],self.potRange[0][0], self.potRange[1][0] ,settings.servos[0].min, settings.servos[0].max),0,180)
                        #print("constrained value: ", val[i])
                        angle = self.scale(val[i], settings.servos[0].min, settings.servos[0].max, 0,180) #scale current pwm to angle
                        previous = self.scale(self.prevPot[i], settings.servos[i].min, settings.servos[i].max, 0 ,180) #scale previous pwm to angle
                        print(settings.servos[0].prevAngle)
                        print('move Angle; ', settings.servos[0].prevAngle + angle -previous)
                        settings.servos[i].moveAngle(settings.servos[0].prevAngle + angle - previous)
                        '''if (self.prevPot[i]> val[i]):
                            time.sleep(.5)
                            newAngle = math.floor(self.scale((settings.servos[0].prevAngle + angle - previous),0,180,settings.servos[0].min, settings.servos[0].max))+1
                            settings.servos[0].movePWM(newAngle)
                            print('if')
                            print(newAngle)
                        elif (self.prevPot[i] < val[i]):
                            time.sleep(.5)
                            newAngle = math.floor(self.scale((settings.servos[0].prevAngle + angle - previous),0,180,settings.servos[0].min, settings.servos[0].max))-1
                            settings.servos[0].movePWM(newAngle)
                            print('else')
                            print(newAngle)'''
                    self.prevPot[i] = val[i]
                    settings.servos[0].prevAngle = self.scale(self.constrain(self.mcp.read_adc(self.channel[i]), self.potRange[0][0], self.potRange[0][1]), self.potRange[0][0], self.potRange[0][1], 0,180)
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
    def pushButtonClicked(self):
        time.sleep(5)
        print("pushed!")

    def cSliderMoved(self, value):
        newAngle = 0
        settings.servos[0].index = int(round(value/22.5))
        print('index: ', settings.servos[0].index)
        value = round(value/22.5)*22.5 #input = degrees, output scaled to 22.5 intervals
##        self.cSlider.setValue(value)
        settings.servos[0].moveAngle(value)
        print('temperature: ', (settings.servos[0].temp[settings.servos[0].index][settings.servos[1].index]))
        self.txtTemp.setText(str(settings.servos[0].temp[settings.servos[0].index][settings.servos[1].index]))
        print('flow rate: ', (settings.servos[0].flow[settings.servos[0].index][settings.servos[1].index]))
        self.txtFlow.setText(str(settings.servos[0].flow[settings.servos[0].index][settings.servos[1].index]))
        print('previous angle: ', settings.servos[0].prevAngle)
        print('current value: ', value)
        if (settings.servos[0].prevAngle> value):
            time.sleep(.5)
            newAngle = math.floor(settings.servos[0].scale(value,0,180,settings.servos[0].min, settings.servos[0].max))+1
            settings.servos[0].movePWM(newAngle)
            print('if')
            print(newAngle)
        elif (settings.servos[0].prevAngle < value):
            time.sleep(.5)
            newAngle = math.floor(settings.servos[0].scale(value,0,180,settings.servos[0].min, settings.servos[0].max))-1
            settings.servos[0].movePWM(newAngle)
            print('else')
            print(newAngle)

        settings.servos[0].prevAngle = value
    
    #Hot Slider
    
    def hSliderMoved(self, value):
        newAngle = 0
        settings.servos[1].index = round(value/22.5)
        print('index: ', settings.servos[1].index)
        value = round(value/22.5)*22.5 #input = degrees, output scaled to 22.5 intervals
##        self.cSlider.setValue(value)
        settings.servos[1].moveAngle(value)
## update output values        
        print('temperature: ', (settings.servos[1].temp[settings.servos[0].index][settings.servos[1].index]))
        self.txtTemp.setText(str(settings.servos[1].temp[settings.servos[0].index][settings.servos[1].index]))
        print('flow rate: ', (settings.servos[0].flow[settings.servos[0].index][settings.servos[1].index]))
        self.txtFlow.setText(str(settings.servos[0].flow[settings.servos[0].index][settings.servos[1].index]))
        
        print('previous angle: ', settings.servos[1].prevAngle)
        print('current value: ', value)
        if (settings.servos[1].prevAngle> value):
            time.sleep(.5)
            newAngle = math.floor(settings.servos[1].scale(value,0,180,settings.servos[1].min, settings.servos[1].max))+1
            settings.servos[1].movePWM(newAngle)
            print('if')
            print(newAngle)
        elif (settings.servos[0].prevAngle < value):
            time.sleep(.5)
            newAngle = math.floor(settings.servos[1].scale(value,0,180,settings.servos[1].min, settings.servos[1].max))-1
            settings.servos[1].movePWM(newAngle)
            print('else')
            print(newAngle)

