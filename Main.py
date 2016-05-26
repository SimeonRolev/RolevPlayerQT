import sys
import QtInterface
from PyQt5 import QtWidgets
import LibraryLoader

app = QtWidgets.QApplication(sys.argv)
GUI = QtInterface.Window()
sys.exit(app.exec_())
