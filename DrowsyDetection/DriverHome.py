


from PyQt5 import QtCore, QtGui, QtWidgets
from detect_drowsiness import VisualBehaviour
from History import history
class Ui_driverhome(object):

    def __init__(self, Dialog,druid):
        self.dialog = Dialog
        self.druid=druid


    def drowsy_detection(self):
        try:
            d = VisualBehaviour()
            d.start(self.druid)

        except Exception as e:
            print(e.args[0])
            tb = sys.exc_info()[2]
            print(tb.tb_lineno)

            
    def history(self):
        try:
            self.hstry= QtWidgets.QDialog()
            self.ui1 = history()
            self.ui1.setupUi(self.hstry)
            self.ui1.viewdata(self.druid)
            self.hstry.show()


        except Exception as e:
            print(e.args[0])
            tb = sys.exc_info()[2]
            print(tb.tb_lineno)            
    def showMessageBox(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()
        
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(619, 526)
        Dialog.setStyleSheet("background-color: rgb(170, 85, 0);")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(190, 90, 241, 41))
        self.pushButton.setStyleSheet("font: 14pt \"Georgia\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.drowsy_detection)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 190, 241, 41))
        self.pushButton_2.setStyleSheet("font: 14pt \"Georgia\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.history)
        
        

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "DriverHome"))
        self.pushButton.setText(_translate("Dialog", "Drowsy Detection"))
        self.pushButton_2.setText(_translate("Dialog", "Driver History"))
      
       



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
