
from PyQt5 import QtCore, QtGui, QtWidgets
from dbconfig import DBConnection
class history(object):

    def viewdata(self,dr_uid):
        database = DBConnection.getConnection()
        cursor = database.cursor()
        cursor.execute("select EAR,MOR,NLR,status,data_time from driver_history where driver_uid='"+dr_uid+"'")
        row = cursor.fetchall()
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(row):
            self.tableWidget.insertRow(row_number)
            for col_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, col_number, QtWidgets.QTableWidgetItem((data)))

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 280)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 681, 281))
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        
        
        

        




        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Driver History"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "EAR"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "MOR"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "NLR"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "State"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Date_Time"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = history()
    ui.setupUi(Dialog)
    ui.viewdata()
    Dialog.show()
    sys.exit(app.exec_())

