from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__pols = []
        self.__q = QPointF(100, 100)
        self.__add_vertex = True
        
        #Variable to store analysis result (0 , 1 , -1)
        self.__result = 0 
        self.__highlight_index = -1     # index of polygon to highlight

    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Create polygon vertex
        if self.__add_vertex == True:
            
            #Create new point
            p = QPointF(x,y)
            
            if len(self.__pols) == 0:
                self.__pols.append(QPolygonF())

            #Add P to polygon
            self.__pols[0].append(p)
            
        #Set new q coordinates
        else: 
            self.__q.setX(x)
            self.__q.setY(y)
                    
        #Repaint
        self.repaint()

    # For this part was used AI for helping with adjusting the script to draw multiple polygons from .shp
    # AI was used to create worflow and to explain the problem
    def paintEvent(self, e):
        #Draw situation
        qp = QPainter(self)
        
        #Start draw
        qp.begin(self)
        
        #Set attributes, polygon outline
        qp.setPen(Qt.GlobalColor.black)
        
        # Go through all polygons, draw them
        # Set brush color based on the result
        for i in range(len(self.__pols)):
            if i == self.__highlight_index and self.__result == 1:
                qp.setBrush(Qt.GlobalColor.darkGreen)           # point is inside
            elif i == self.__highlight_index and self.__result == -1:
                qp.setBrush(Qt.GlobalColor.cyan)                # singularity: edge or vertex
            else:
                qp.setBrush(Qt.GlobalColor.yellow)              # outside or default
            
            #Draw polygon
            qp.drawPolygon(self.__pols[i])
        
        #Set attributes, point color
        qp.setBrush(Qt.GlobalColor.red)
        
        #Draw point
        r = 10
        qp.drawEllipse(int(self.__q.x()-r), int(self.__q.y()-r), 2*r, 2*r)
        
        #End draw
        qp.end()
        
    def changeStatus(self):
        #Input source: point or polygon
        self.__add_vertex = not (self.__add_vertex)
        
    def clearData(self):
        #Clear datas
        self.__pols = []
        self.__q.setX(-25)
        self.__q.setY(-25)
        
        # Reset result to default
        self.__result = 0
        self.repaint()
        self.__highlight_index = -1

    def getQ(self):
        #Return point
        return self.__q
    
    def getPols(self):
        #Return polygon
        return self.__pols
    
    def setPols(self, pols_list):
        self.__pols = pols_list
        self.repaint()    

    def setResult(self, res, index=-1):
        # get result and repaint canvas
        self.__result = res
        self.__highlight_index = index
        self.repaint()