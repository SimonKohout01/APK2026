from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *
from random import *
from math import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__points =[]
        self.__DT = []
        self.__contours = []
        self.__slope = []
        self.__view_DT = True
        self.__view_Slope = False
        self.__view_Aspect = False
        self.__view_Contours = True
        
        self.aspect_colors = [
            QColor("#fa0100"),
            QColor("#ffa401"),
            QColor("#fdfe01"),
            QColor("#00fe03"),
            QColor("#00ffff"),
            QColor("#00a5fe"),
            QColor("#0000fd"),
            QColor("#fc00f9"),]
        
    
        
        
    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Get random z
        z_min = 200
        z_max = 600
        z = random() * (z_max - z_min) + z_min

        #Create new point
        p = QPoint3DF(x, y, z)
        
        #Add P to polygon
        self.__points.append(p)
        
        #Repaint
        self.repaint()
        

    def paintEvent(self, e):
        #Draw situation
        qp = QPainter(self)
        qp.begin(self)
        pen = QPen()
        
        #Draw aspect (Exposition)
        if self.__view_Aspect:
            #Set properties
            pen.setColor(Qt.GlobalColor.gray)
            pen.setWidth(1)
            qp.setPen(pen)
            
            #8 colors
            res = 2 * pi / 8 
                
            #Process triangles
            for triangle in self.__slope: 
                #Get polygon
                pol = triangle.getPolygon()
                
                #Get aspect
                aspect = triangle.getAspect()
            
                #Calculate color index
                idx = int((aspect + res/2) / res) % 8

                #Assign brush color
                color = self.aspect_colors[idx]
                qp.setBrush(color)
                
                #Draw polygon
                qp.drawPolygon(pol)
                
        #Draw slope
        if self.__view_Slope:
            #Set properties
            pen.setColor(Qt.GlobalColor.black)
            qp.setPen(pen)

            #Process triangles
            for triangle in self.__slope:
                #Get polygon
                pol = triangle.getPolygon()

                #Get slope
                slope = triangle.getSlope()

                #Rescale slope to 0-255
                k = (2*255) / pi
                gray = int(255 - (slope * k))

                #Create Qt Color
                color = QColor(gray, gray, gray)

                #Assign brush color
                qp.setBrush(color)

                #Draw polygon
                qp.drawPolygon(pol)
            
        #Draw DT edges
        if self.__view_DT:
            #Set properties
            pen.setColor(Qt.GlobalColor.green)
            qp.setPen(pen)
            
            #Draw edges
            for e in self.__DT:
                qp.drawLine(e.getStart(), e.getEnd())

        #Draw contour lines
        if self.__view_Contours:        
            #Set properties
            pen.setColor(QColor(140, 90, 50)) 
            qp.setPen(pen)
            
            #Draw lines
            for c in self.__contours:
                qp.drawLine(c.getStart(), c.getEnd())
            
        #Draw points
        pen.setWidth(15)
        pen.setColor(Qt.GlobalColor.black)
        qp.setPen(pen)
   
        #Execute draw
        qp.drawPoints(self.__points)
        
        #End draw
        qp.end()
        
        
    def setDT(self, DT):
        #Set DT
        self.__DT = DT
        
    
    def getDT(self):
        return self.__DT
    
    def setPoints(self, points):
        self.__points = points
        self.repaint()
    

    def getPoints(self):
        #Get points
        return self.__points
    
    
    def clearAll(self):
        #Clear everything including input points
        self.__points.clear()
        self.__DT.clear()
        self.__contours.clear()
        self.__slope.clear()
        # Repaint screen
        self.repaint()
        
    def clearResults(self):
        # Clear only results of analyses (keep points)
        self.__DT.clear()
        self.__contours.clear()
        self.__slope.clear()
        #Repaint screen
        self.repaint()
        
        
    def setContours(self, contours):
        #Set contour lines
        self.__contours = contours
    

    def setSlope(self, slope):
        #Set slope
        self.__slope = slope
 
    def setViewDT(self, view):
        #Set view DT
        self.__view_DT = view
        

    def setViewSlope(self, view):
        #Set view Slope
        self.__view_Slope = view
        

    def setViewAspect(self, view):
        #Set view Aspect
        self.__view_Aspect = view
        
        
    def setViewContours(self, view):
        #Set view contours
        self.__view_Contours = view
        
        
    def setResult(self, res):
        # get result and repaint canvas
        self.__result = res
        self.repaint()
        
    
        
        