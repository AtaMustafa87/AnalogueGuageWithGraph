from PyQt5.QtWidgets import QApplication
from guageWidget import GaugeWidget
from graphwidget import GarphWidget
import sys
app = QApplication(sys.argv)
my_gauge = GarphWidget()
my_gauge.show()
sys.exit(app.exec_())