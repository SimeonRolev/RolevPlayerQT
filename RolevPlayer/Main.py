import sys
from RolevPlayer import QtInterface
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
GUI = QtInterface.Window()
sys.exit(app.exec_())
