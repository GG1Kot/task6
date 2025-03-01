from PyQt6 import QtWidgets
from UI.addEditCoffeeForm_ui import Ui_AddEditCoffeeForm

class AddEditCoffeeForm(QtWidgets.QDialog, Ui_AddEditCoffeeForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def getData(self):
        sort = self.sortLineEdit.text()
        roast = self.roastLineEdit.text()
        grind_or_beans = self.grindComboBox.currentText()
        taste = self.tasteTextEdit.toPlainText()
        price = float(self.priceLineEdit.text())
        volume = float(self.volumeLineEdit.text())
        return (sort, roast, grind_or_beans, taste, price, volume)

    def setData(self, data):
        sort, roast, grind_or_beans, taste, price, volume = data
        self.sortLineEdit.setText(sort)
        self.roastLineEdit.setText(roast)
        index = self.grindComboBox.findText(grind_or_beans)
        if index >= 0:
            self.grindComboBox.setCurrentIndex(index)
        self.tasteTextEdit.setPlainText(taste)
        self.priceLineEdit.setText(str(price))
        self.volumeLineEdit.setText(str(volume))