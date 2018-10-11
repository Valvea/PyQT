from PyQt5 import QtCore, QtGui, QtWidgets
import data_w as d

class Ui_Form(object):
    weather = d.Weather()
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 200)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        Form.setFont(font)

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(40, 30, 200, 80))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.refresh = QtWidgets.QPushButton("Обновить",Form)
        self.refresh.move(40,150)
        self.refresh.clicked.connect(self.refresh_weather)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.clouds = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.clouds.setObjectName("clouds")
        self.verticalLayout_2.addWidget(self.clouds)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.temperature = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.time=QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font_time=QtGui.QFont()
        font_time.setPointSize(10)
        self.temperature.setFont(font)
        self.time.setFont(font_time)
        self.temperature.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.time.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.temperature.setObjectName("temperature")
        self.time.setObjectName("time")
        self.horizontalLayout.addWidget(self.temperature)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.horizontalLayout.addStretch(0.5)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.time)

        self.img=QtGui.QPixmap()
        self.img.load(self.weather.get_icon())
        self.retranslateUi(Form)

        QtCore.QMetaObject.connectSlotsByName(Form)



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Погода"))
        self.clouds.resize(self.img.size())
        self.clouds.setPixmap(self.img)
        self.temperature.setText(_translate("Form",self.weather.get_temp()))
        self.time.setText(_translate("Form",str(self.weather.get_time())))
        self.label_2.setText(_translate("Form", "°С"))

    def refresh_weather(self):
        self.weather.refresh_weather()
        self.retranslateUi(Form)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())