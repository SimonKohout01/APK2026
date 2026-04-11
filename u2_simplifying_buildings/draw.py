from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__building = QPolygonF()
        self.__mbr = QPolygonF()
        self.__ch = QPolygonF()
        self.__pols = []        # For drawing shapes from .shp
        self.__mbrs = []        # For drawing multiple rectangles after simplification

        
    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Create new point
        p = QPointF(x,y)
        
        #Add P to polygon
        self.__building.append(p)
        
        #Repaint
        self.repaint()
        

    def paintEvent(self, e):
        #Draw situation
        qp = QPainter(self)
        
        #Start draw
        qp.begin(self)
        
        # Drawing from .shp
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.gray)

        for p in self.__pols:
            qp.drawPolygon(p)

        #Set attributes, building
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Draw building
        qp.drawPolygon(self.__building)
        
        #Set attributes, convex hull
        qp.setPen(Qt.GlobalColor.blue)
        qp.setBrush(Qt.GlobalColor.transparent)
        
        #Draw convex hull
        qp.drawPolygon(self.__ch)
        
        #Set attributes, MBR
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.transparent)
        
        for rect in self.__mbrs:
            qp.drawPolygon(rect)

        #Draw MBR
        qp.drawPolygon(self.__mbr)
        
        #End draw
        qp.end()
        
        
    def setMBR(self, mbr:QPolygonF):
        #Set MBR
        self.__mbr = mbr

    def setMBRs(self, mbrs_list):
        # Set MBRs for .shp    
        self.__mbrs = mbrs_list

    def setCH(self, ch:QPolygonF):
        #Set CH
        self.__ch = ch  
        
        
    def getBuilding(self):
        #Get building
        return self.__building
    
    
    def clearResult(self):
        #Clear data structures for results
        self.__ch.clear()
        self.__mbr.clear()
        self.__mbrs.clear()
    
        
        #Repaint screen
        self.repaint()

    # Clear all data
    def clearData(self):
        self.__ch.clear()
        self.__mbr.clear()
        self.__building.clear()
        self.__pols.clear()
        self.__mbrs.clear()

        self.repaint()

    def getPols(self):
        #Return polygon
        return self.__pols
    
    def setPols(self, pols_list):
        self.__pols = pols_list
        self.repaint()    

        
        