from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time

class Worker(QObject):
    finished = pyqtSignal()
    intReady= pyqtSignal(int)
    
    @pyqtSlot()
    def procCounter(self):
        for i in range(1,100):
            time.sleep(1)
            self.intReady.emit(i)
            
        self.finished.emit()