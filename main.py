import sys

from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('test.ui', self)
        self.pushButton.clicked.connect(self.run)

    def run(self):
        self.label.setText("OK")


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())