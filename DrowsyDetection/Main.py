

from PyQt5 import QtCore, QtGui, QtWidgets
from Driver import Ui_driver

class Ui_Main(object):


    def driver_login(self, event):
        try:
            self.drvr = QtWidgets.QDialog()
            self.ui = Ui_driver(self.drvr)
            self.ui.setupUi(self.drvr)
            self.drvr.show()
        except Exception as e:
            print(e.args[0])
            tb = sys.exc_info()[2]
            print(tb.tb_lineno)
        event.accept()


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(741, 491)
        Dialog.setStyleSheet("background-color: rgb(200, 52, 74);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(130, 40, 681, 51))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 20pt \"Vani\";")
        self.label.setObjectName("label")
        self.driver = QtWidgets.QLabel(Dialog)
        self.driver.setGeometry(QtCore.QRect(200, 150, 271, 191))
        self.driver.setStyleSheet("image: url(../DrowsyDetection/images/driverr.png);")
        self.driver.setText("")
        self.driver.setObjectName("faculty")
        self.driver.mousePressEvent=self.driver_login
        '''self.admin = QtWidgets.QLabel(Dialog)
        self.admin.setGeometry(QtCore.QRect(50, 160, 251, 191))
        self.admin.setStyleSheet("image: url(../DrowsyDetection/images/adminn.png);")
        self.admin.setText("")
        self.admin.setObjectName("admin")
        self.admin.mousePressEvent=self.admin_login'''
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(140, 370, 121, 31))
        self.label_2.setStyleSheet("font: 16pt \"Vani\";\n"
"color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(300, 360, 121, 41))
        self.label_3.setStyleSheet("font: 16pt \"Vani\";\n"
"color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Main"))
        self.label.setText(_translate("Dialog", "Driver Drowsiness Monitoring System"))
        #self.label_2.setText(_translate("Dialog", "Admin"))
        self.label_3.setText(_translate("Dialog", "Driver"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Main()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
