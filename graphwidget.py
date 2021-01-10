
import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import QWidget,QVBoxLayout
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import date2num
from datetime import datetime,timedelta

class GarphWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(GarphWidget, self).__init__(fig)
        n_data = 50
        self.xdata = [datetime.now() + timedelta(seconds=i) for i in range(n_data)]#list(range(n_data))
        self.ydata = [random.randint(0, 10) for i in range(n_data)]
        self.update_plot()

        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.xdata = self.xdata[1:] + [datetime.now()]
        self.axes.cla()  # Clear the canvas.
        self.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.draw()
