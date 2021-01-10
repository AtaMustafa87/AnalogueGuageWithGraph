import math
from PyQt5.QtWidgets import QMainWindow,QWidget, QApplication
from PyQt5.QtGui import QPolygon, QPolygonF, QColor, QPen, QFont
from PyQt5.QtGui import QPainter, QFontMetrics, QConicalGradient
from PyQt5.QtCore import Qt ,QTime, QTimer, QPoint, QPointF, QRect, QSize
from PyQt5.QtCore import QObject, pyqtSignal

class GaugeWidget(QWidget):
    def __init__(self, _width=400,_height=400, parent=None):
        super(GaugeWidget, self).__init__(parent)
        
        self.setWidth(_width)
        self.setHeight(_height)
        self.pen = QPen(QColor(0, 0, 0))
        self.widgetDiameter = 0
        if _width > _height: 
            self.widgetDiameter = _width
        else:
            self.widgetDiameter = _height
        self.outerRadiusFactor = 1 
        self.innerRadiusFactor = 0.9
        self.scaleAngleStartValue = 135
        self.scaleAngleSize = 270
        self.angleOffset = 0
        self.scalePolygonColors = [[.0, Qt.red],[.33, Qt.yellow],[.66, Qt.green],[1, Qt.transparent]]
        self.scaleMainCount = 10 # For main ticks
        self.scaleSubDivisionCount = 5 # for inner ticks
        self.scaleValueColor = QColor(50, 50, 50, 255)
        self.valueMin = 0
        self.valueMax = 100

        self.scaleFontName = "Decorative"
        self.scaleFontSize = 15

    def setWidth(self,_width):
        self.resize(_width,self.height())

    def setHeight(self,_height):
        self.resize(self.width(),_height)
    
    def paintEvent(self, event):
        self.drawFilledPolygon()
        self.createFineScaledMarker()
        self.drawBigScaledMarker()
        self.createScaleMarkerValuesText()
    
    def createPloygonPie(self, outer_radius, inner_raduis, start, lenght):
        """ Create Polygon for given parameters"""
        polygonPie = QPolygonF()
        n = 360     # angle steps size for full circle
        # changing n value will causes drawing issues
        w = 360 / n   # angle per step
        # create outer circle line from "start"-angle to "start + lenght"-angle
        x = 0
        y = 0

        for i in range(lenght+1):                                              # add the points of polygon
            t = w * i + start - self.angleOffset
            x = outer_radius * math.cos(math.radians(t))
            y = outer_radius * math.sin(math.radians(t))
            polygonPie.append(QPointF(x, y))
        # create inner circle line from "start + lenght"-angle to "start"-angle
        for i in range(lenght+1):                                              # add the points of polygon
            # print("2 " + str(i))
            t = w * (lenght - i) + start - self.angleOffset
            x = inner_raduis * math.cos(math.radians(t))
            y = inner_raduis * math.sin(math.radians(t))
            polygonPie.append(QPointF(x, y))

        # close outer line
        polygonPie.append(QPointF(x, y))
        return polygonPie

    def drawFilledPolygon(self,outlinePenWidth=0):
        """Fill polygon with gradiant colors, polygon created through createPolygonPie"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Position in middle of the widget
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.NoPen)
        self.pen.setWidth(0)
        if outlinePenWidth > 0:
            painter.setPen(self.pen)

        coloredScalePolygon = self.createPloygonPie(
            ((self.widgetDiameter / 2) - (self.pen.width() / 2)) * self.outerRadiusFactor,
            (((self.widgetDiameter / 2) - (self.pen.width() / 2)) * self.innerRadiusFactor),
            self.scaleAngleStartValue, self.scaleAngleSize)

        grad = QConicalGradient(QPointF(0, 0), - self.scaleAngleSize - self.scaleAngleStartValue +
                                self.angleOffset - 1)

        # set gradiant colors
        for eachcolor in self.scalePolygonColors:
            grad.setColorAt(eachcolor[0], eachcolor[1])
        painter.setBrush(grad)
        painter.drawPolygon(coloredScalePolygon)

    def createFineScaledMarker(self):
        """Draw fine tick marsk on the color bar"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.setPen(Qt.black)
        painter.rotate(self.scaleAngleStartValue - self.angleOffset)
        stepSize = (float(self.scaleAngleSize) / float(self.scaleMainCount * self.scaleSubDivisionCount))
        scaleLineOuterStart = self.widgetDiameter/2
        #scaleLineLenght = (self.widgetDiameter / 2) - (self.widgetDiameter / 40)
        scaleLineLenght = (self.widgetDiameter / 2) - (self.widgetDiameter*(self.outerRadiusFactor-self.innerRadiusFactor)/2)
        for i in range((self.scaleMainCount * self.scaleSubDivisionCount)+1):
            painter.drawLine(scaleLineLenght, 0, scaleLineOuterStart, 0)
            painter.rotate(stepSize)

    def drawBigScaledMarker(self):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        self.pen = QPen(QColor(0, 0, 0, 255))
        self.pen.setWidth(2)
        painter.setPen(self.pen)
        painter.rotate(self.scaleAngleStartValue - self.angleOffset)
        stepsSize = (float(self.scaleAngleSize) / float(self.scaleMainCount))
        scaleLineOuterStart = self.widgetDiameter/2
        scaleLineLenght = (self.widgetDiameter / 2) - (self.widgetDiameter / 20)
        for _ in range(self.scaleMainCount+1):
            painter.drawLine(scaleLineLenght, 0, scaleLineOuterStart, 0)
            painter.rotate(stepsSize)

    def createScaleMarkerValuesText(self):
        painter = QPainter(self)
        # painter.setRenderHint(QPainter.HighQualityAntialiasing)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        # painter.save()
        font = QFont(self.scaleFontName, self.scaleFontSize)
        fm = QFontMetrics(font)

        penShadow = QPen()

        penShadow.setBrush(self.scaleValueColor)
        painter.setPen(penShadow)

        textRadiusFactor = 0.8
        textRadius = self.widgetDiameter/2 * textRadiusFactor

        scalePerDiv = int((self.valueMax - self.valueMin) / self.scaleMainCount)

        angleDistance = (float(self.scaleAngleSize) / float(self.scaleMainCount))
        for i in range(self.scaleMainCount + 1):
            # text = str(int((self.valueMax - self.valueMin) / self.scaleMainCount * i))
            text = str(int(self.valueMin + scalePerDiv * i))
            w = fm.width(text) + 1
            h = fm.height()
            painter.setFont(QFont(self.scaleFontName, self.scaleFontSize))
            angle = angleDistance * i + float(self.scaleAngleStartValue - self.angleOffset)
            x = textRadius * math.cos(math.radians(angle))
            y = textRadius * math.sin(math.radians(angle))
            # print(w, h, x, y, text)
            text = [x - int(w/2), y - int(h/2), int(w), int(h), Qt.AlignCenter, text]
            painter.drawText(text[0], text[1], text[2], text[3], text[4], text[5])
        # painter.restore()
