from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__pol = QPolygonF()
        self.__q = QPointF(100, 100)
        self.__add_vertex = True
        

    def mousePressEvent(self, e):
        #Get cursor coordinates 
        x = e.position().x()
        y = e.position().y()
        
        #Create polygon vertex
        if self.__add_vertex == True:
            
            #Create new point
            p = QPointF(x,y)
            
            #Add P to polygon
            self.__pol.append(p)
            
        #Set new q coordinates
        else: 
            self.__q.setX(x)
            self.__q.setY(y)
                    
        #Repaint
        self.repaint()

    def paintEvent(self, e):
        #Draw situation
        qp = QPainter(self)
        
        #Start draw
        qp.begin(self)
        
        #Set attributes, polygon
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.yellow)
        
        #Draw polygon
        qp.drawPolygon(self.__pol)
        
        #Set attributes, point
        qp.setBrush(Qt.GlobalColor.green)
        
        
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
        self.__pol.clear()
        self.repaint()
        self.__q.setX(-25)
        self.__q.setY(-25)
    
    def getQ(self):
        #Return point
        return self.__q
    
    def getPol(self):
        #Return polygon
        return self.__pol
    
        
          