from PyQt5.QtWidgets import QApplication
from guageWidget import GaugeWidget
import sys
app = QApplication(sys.argv)
my_gauge = GaugeWidget()
my_gauge.show()
sys.exit(app.exec_())