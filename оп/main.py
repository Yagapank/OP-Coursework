import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from check_db import *
from des import *
from entry_form import *
from Levenstein import *
import sqlite3


class Interface(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.reg)
        self.ui.pushButton_2.clicked.connect(self.auth)
        self.base_line_edit = [self.ui.lineEdit, self.ui.lineEdit_2]

        self.check_db = CheckThread()
        self.check_db.mysignal.connect(self.signal_handler)

        self.entryform = EntryForm()

    # Проверка правильности ввода
    def check_input(funct):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit.text()) == 0:
                    return
            funct(self)

        return wrapper

    # Обработчик сигналов
    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Оповещение', value)
        if value == 'Успешная авторизация!':
            self.entryform.show()

    @check_input
    def auth(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        self.check_db.thr_login(name, passw)

    @check_input
    def reg(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        self.check_db.thr_register(name, passw)


class EntryForm(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form2()
        self.ui.setupUi(self)

        self.levenstein = Levenstein()
        self.ui.pushButton.clicked.connect(self.LevensteinCalc)
        self.ui.pushButton_2.clicked.connect(self.database_entry)
        self.ui.pushButton_3.clicked.connect(self.select_from_database)

    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, "Оповещение", value)

    def LevensteinCalc(self):
        str1 = self.ui.lineEdit.text()
        str2 = self.ui.lineEdit_2.text()
        otv = self.levenstein.levenstein(str1, str2)
        self.ui.lineEdit_3.setText(str(otv))

    def database_entry(self):
        con = sqlite3.connect(f'handler/users')
        cur = con.cursor()

        str1 = self.ui.lineEdit.text()
        str2 = self.ui.lineEdit_2.text()
        otv = self.ui.lineEdit_3.text()

        cur.execute(f"INSERT INTO levenstein_data (str1, str2, otv) VALUES ('{str1}', '{str2}', '{otv}');")
        self.signal_handler('Данные успешно записаны в базу данных!')
        con.commit()

        cur.close()
        con.close()

    def select_from_database(self):
        connection = sqlite3.connect(f'handler/users')
        cur = connection.cursor()
        sqlquery = f'SELECT * FROM levenstein_data'

        list_of_rows = list(cur.execute(sqlquery))

        self.ui.tableWidget.setRowCount(len(list_of_rows))
        tablerow = 0
        for row in list_of_rows:
            self.ui.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.ui.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.ui.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            tablerow += 1

        connection.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mywin = Interface()
    mywin.show()
    sys.exit(app.exec_())
