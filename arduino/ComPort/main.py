import sys
from serial import Serial
from serial import *
import threading

from PyQt5.QtCore import Qt,pyqtSignal,QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider,
    QVBoxLayout, QApplication,QLineEdit,QPushButton)



class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.timeout = 0
        self.ser = Serial(
            port='COM6',
            baudrate=9600,
            bytesize=EIGHTBITS,
            parity=PARITY_NONE,
            stopbits=STOPBITS_ONE,
            timeout=0.1,
            xonxoff=0,
            rtscts=0,
            interCharTimeout=None
        )
        self.initUI()


    def initUI(self):

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal & slot')
        self.btnstopth=QPushButton("Закрыть поток",self)
        self.btnsrunth = QPushButton("Открыть поток", self)
        self.lined=QLineEdit("Данные",self)
        self.lined.setFont(QFont("Century Gothic",12))
        self.lined.move(30,30)
        self.btnstopth.move(30,80)
        self.btnsrunth.move(130,80)
        self.lined.resize(160,30)
        self.show()
        self.check_serial_event()
        self.btnstopth.clicked.connect(self.close_ser)
        self.btnsrunth.clicked.connect(self.open_ser)

    def closeEvent(self, event):
            self.close_ser()
            event.accept()


    def set_line(self,v):
        self.lined.setText(v)

    def close_ser(self):
        self.ser.close()
        #self.serial_thread.cancel()

    def open_ser(self):
        if self.ser.is_open is True:
            pass
        else:
            self.ser.open()
            self.restart()


    def restart(self):
        self.check_serial_event()



    def check_serial_event(self):
        self.serial_thread = threading.Timer(5, self.check_serial_event)
        if self.ser.is_open is True:
            self.serial_thread.start()
            if self.ser.in_waiting:
                z_str = "b''"
                while True :
                    if self.ser.is_open is False:
                        break
                    else:
                        buff = str(self.ser.readline())
                        if buff == z_str:
                            pass
                        else:
                            value=self.ser.readline().decode("utf-8")
                            print(value)
                            self.set_line(value)
        else:
            self.serial_thread.cancel()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
