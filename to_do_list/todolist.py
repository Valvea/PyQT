import sys
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication,QAction
from PyQt5.QtCore import Qt,QSettings
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


CONFIG_FILE_NAME = 'config3.ini'

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
        self.im.load("weather/x.png")
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
        chbox=QtWidgets.QCheckBox(self.input.text())
        chbox.setFont(QtGui.QFont("Arial",12))
        chbox.stateChanged.connect(self.changeFont)
        temp_hrl.addWidget(chbox)
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
        self.load_settings()


    def initUI(self):
        self.list_settings=[]
        self.Scroll_W=QtWidgets.QScrollArea()
        self.main_widget=Central_Widget()
        self.Scroll_W.resize(self.main_widget.size())
        self.Scroll_W.setWidget(self.main_widget)
        self.setCentralWidget(self.Scroll_W)
        self.resize(self.centralWidget().width(),self.centralWidget().height())
        self.setWindowTitle(self.main_widget.windowTitle())
        self.menu=self.menuBar()
        self.filemenu= self.menu.addMenu("&Файл")
        saveAction = QAction(QtGui.QIcon('weather/file.png'), '&Сохранить', self)
        self.filemenu.addAction(saveAction)
        saveAction.triggered.connect(self.save_file)
        self.show()





    def save_file(self):

        settings = QSettings(CONFIG_FILE_NAME, QSettings.IniFormat)
        settings.setValue('WindowState', self.saveState())
        for obj in range(self.main_widget.vlayout.count()):
            temp_h_l = self.main_widget.vlayout.itemAt(obj)
            self.list_settings.append({"text":temp_h_l.itemAt(0).widget().text(),"isChecked()":temp_h_l.itemAt(0).widget().isChecked()})
        settings.setValue("Central_widget",self.list_settings.copy())







    def load_settings(self):
        settings = QSettings(CONFIG_FILE_NAME, QSettings.IniFormat)
        cenral = settings.value('Central_widget')
        if cenral is None:
            return 0

        state = settings.value('WindowState')
        if state:
            self.restoreState(state)


        print(cenral)
        if cenral:
            i=0
            for d in cenral:
                self.main_widget.input.setText(d["text"])
                self.main_widget.push_on_add_task_but()
                if d["isChecked()"] is True:
                    h_l=self.main_widget.vlayout.itemAt(i)
                    temp = QtGui.QFont("Arial", 12)
                    temp.setStrikeOut(True)
                    h_l.itemAt(i).widget().setFont(temp)





        # self.cb_flag.setChecked(settings.value('BoolValue', 'false') == 'true')






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwidge()
    sys.exit(app.exec_())
