import sys
import sqlite3
from PyQt6 import QtWidgets
from UI.main_ui import Ui_CoffeeMainWindow
from addEditCoffeeForm import AddEditCoffeeForm

class CoffeeApp(QtWidgets.QMainWindow, Ui_CoffeeMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loadData()
        self.addButton.clicked.connect(self.openAddForm)
        self.editButton.clicked.connect(self.openEditForm)

    def loadData(self):
        conn = sqlite3.connect("data/coffee.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT id, sort, roast, grind_or_beans, taste, price, volume FROM coffee")
        rows = cur.fetchall()
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Молотый/В зернах", "Описание вкуса", "Цена", "Объем упаковки"])
        for row_index, row in enumerate(rows):
            for col_index, item in enumerate(row):
                self.tableWidget.setItem(row_index, col_index, QtWidgets.QTableWidgetItem(str(item)))
        conn.close()

    def openAddForm(self):
        form = AddEditCoffeeForm()
        if form.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = form.getData()
            conn = sqlite3.connect("data/coffee.sqlite")
            cur = conn.cursor()
            cur.execute("INSERT INTO coffee (sort, roast, grind_or_beans, taste, price, volume) VALUES (?, ?, ?, ?, ?, ?)", data)
            conn.commit()
            conn.close()
            self.loadData()

    def openEditForm(self):
        selected = self.tableWidget.currentRow()
        if selected < 0:
            return
        id_item = self.tableWidget.item(selected, 0)
        if not id_item:
            return
        record_id = id_item.text()
        conn = sqlite3.connect("data/coffee.sqlite")
        cur = conn.cursor()
        cur.execute("SELECT sort, roast, grind_or_beans, taste, price, volume FROM coffee WHERE id=?", (record_id,))
        record = cur.fetchone()
        conn.close()
        if record:
            form = AddEditCoffeeForm()
            form.setData(record)
            if form.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                data = form.getData()
                conn = sqlite3.connect("data/coffee.sqlite")
                cur = conn.cursor()
                cur.execute("UPDATE coffee SET sort=?, roast=?, grind_or_beans=?, taste=?, price=?, volume=? WHERE id=?", (*data, record_id))
                conn.commit()
                conn.close()
                self.loadData()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())