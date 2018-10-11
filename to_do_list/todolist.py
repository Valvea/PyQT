import sys
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui



class Central_Widget(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):


        self.input=QtWidgets.QLineEdit("Введите задание",self)
        self.input.setFont(QtGui.QFont("Arial",12))
        self.input.resize(self.input.width()+140,self.input.height())
        self.add_task_but=QtWidgets.QPushButton("Добавить",self)
        self.add_task_but.setFont(QtGui.QFont("Arial",12))
        self.vrl=QtWidgets.QWidget(self)
        self.im=QtGui.QPixmap()
        self.im.load("x.png")
        self.vlayout=QtWidgets.QVBoxLayout(self.vrl)
        self.setGeometry(0,30,700,500)
        self.input.move(150,40)
        self.input.setMaximumWidth(600)
        self.add_task_but.move(self.input.x()+self.input.width(),self.input.y()-1)
        self.add_task_but.resize(self.add_task_but.width(),self.input.height()+2)
        self.vrl.setGeometry(self.input.x()-20,self.input.y()+30, 500, 50)
        self.setWindowTitle('Список Дел')
        self.add_task_but.clicked.connect(self.push_on_add_task_but)
        #self.show()

    def changeFont(self, state):
        temp = QtGui.QFont("Arial", 12)
        if state == Qt.Checked:
            temp.setStrikeOut(True)
        else:
            temp.setStrikeOut(False)
        self.sender().setFont(temp)


    def push_on_add_task_but(self):
        if (self.height()-self.vrl.height())<=60:
            self.resize(self.width(),self.height()+90)
        del_but = QtWidgets.QPushButton()
        del_but.resize(self.im.size())
        del_but.setIcon(QtGui.QIcon(self.im))
        del_but.setFixedSize(20,20)
        temp_hrl=QtWidgets.QHBoxLayout()
        temp=QCheckBox(self.input.text())
        temp.setFont(QtGui.QFont("Arial",12))
        temp.stateChanged.connect(self.changeFont)
        temp_hrl.addWidget(temp)
        temp_hrl.addWidget(del_but)
        self.vlayout.addLayout(temp_hrl)
        del_but.clicked.connect(self.on_clicked_del_but)
        self.vrl.resize(self.vrl.width(),self.vrl.height()+self.input.height())
        self.input.clear()






    def on_clicked_del_but(self):
        for j in range(self.vlayout.count()):
            temp_h_l =self.vlayout.itemAt(j)
            if self.sender()==temp_h_l.itemAt(1).widget():
                temp_h_l.itemAt(0).widget().hide()
                temp_h_l.itemAt(1).widget().hide()
                self.vlayout.removeItem(self.vlayout.itemAt(j))
                self.vrl.resize(self.vrl.width(), self.vrl.height()-self.input.height())
                break

class Mainwidge(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):

        self.Scroll_W=QtWidgets.QScrollArea()
        self.main_widget=Central_Widget()
        self.Scroll_W.resize(self.main_widget.size())
        self.Scroll_W.setWidget(self.main_widget)
        self.setCentralWidget(self.Scroll_W)
        self.resize(self.centralWidget().width(),self.centralWidget().height())
        self.show()







if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainwidge()
    sys.exit(app.exec_())
