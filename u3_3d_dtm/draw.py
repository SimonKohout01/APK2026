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
        
        # Different color schemes for user to choose from - help from AI with a pseudocode
        # Stores the selected scheme index
        self.__aspect_scheme = 0
        
        # 0 = bright rainbow
        self.aspect_colors_0 = [
            QColor("#fa0100"), QColor("#ffa401"), QColor("#fdfe01"), QColor("#00fe03"),
            QColor("#00ffff"), QColor("#00a5fe"), QColor("#0000fd"), QColor("#fc00f9")]
            
        # 1 = pastel rainbow
        self.aspect_colors_1 = [
            QColor("#FFB5B5"), QColor("#FFD9B5"), QColor("#FFFFB5"), QColor("#B5FFC9"),
            QColor("#80E5FF"), QColor("#A0C4FF"), QColor("#C4B5FD"), QColor("#FFB5FF")]
            
        # 2 = magma
        self.aspect_colors_2 = [
            QColor("#003F5C"), QColor("#58508D"), QColor("#8A508F"), QColor("#BC5090"),
            QColor("#DE5A8D"), QColor("#FF6361"), QColor("#FF8531"), QColor("#FFA600")]
            
        # 3 = contrast scheme
        self.aspect_colors_3 = [
            QColor("#111D31"), QColor("#EAE5DF"), QColor("#5CA6CA"), QColor("#2376B7"),
            QColor("#F29F05"), QColor("#D02339"), QColor("#84404D"), QColor("#405E72")]

        # Stores the selected scheme index
        self.__slope_scheme = 0
        
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

                # Picks the color of the selected scheme 0-3
                if self.__aspect_scheme == 0:
                    color = self.aspect_colors_0[idx]
                elif self.__aspect_scheme == 1:
                    color = self.aspect_colors_1[idx]
                elif self.__aspect_scheme == 2:
                    color = self.aspect_colors_2[idx]
                elif self.__aspect_scheme == 3:
                    color = self.aspect_colors_3[idx]
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
                interpolation = int(255 - (slope * k))

                #Create Qt Color
                # QColor(int 'red', int 'green', int 'blue', int a = 255)
                if self.__slope_scheme == 0:
                    # 0 = White to black
                    color = QColor(interpolation, interpolation, interpolation)
                    
                elif self.__slope_scheme == 1:
                    # 1 = Yellow to red
                    color = QColor(255, interpolation, 0)
                    
                elif self.__slope_scheme == 2:
                    # 2 = White to blue
                    color = QColor(interpolation, interpolation, 255)
                    
                elif self.__slope_scheme == 3:
                    # 3 = White to Pink
                    color = QColor(255, interpolation, 255)

                #Assign brush color
                qp.setBrush(color)

                #Draw polygon
                qp.drawPolygon(pol)
            
        #Draw DT edges
        if self.__view_DT:
            #Set properties
            pen.setColor(Qt.GlobalColor.gray)
            qp.setPen(pen)
            
            #Draw edges
            for e in self.__DT:
                qp.drawLine(e.getStart(), e.getEnd())

        #Draw contour lines
        if self.__view_Contours: 
            counter_highlight = 0   # Counts number of line segments on canvas (highlighted contours)
            counter_normal = 0      # -,,- normal contou
            #Draw lines
            for c in self.__contours:
                z = c.getStart().z() # Saving height z from the start of the contour

                if z % (self.__dz * 5) == 0:    # % = modulo (= division of whole number)
                                                # dz = step between each contour - 
                                                # * 5 means every 5th contour is highlighted

                    pen.setColor(QColor(100, 50, 20))
                    pen.setWidth(2) # Thicker and darker line for highlighted contour

                    if counter_highlight % 20 == 0:   # Each 20th line segment will get its description of 'z'
                        mid_x = int((c.getStart().x() + c.getEnd().x()) / 2)    # Description is in the middle of the contour
                        mid_y = int((c.getStart().y() + c.getEnd().y()) / 2)

                        qp.setFont(QFont("Arial", 10))  # Bigger font for highlighted contour
                        qp.setPen(QColor(100, 50, 20))

                        qp.drawText(mid_x, mid_y, str(int(z)))
                
                    counter_highlight += 1
                else:
                    if counter_normal % 35 == 0:   # Each 35th line segment will get its description of 'z'
                        mid_x = int((c.getStart().x() + c.getEnd().x()) / 2)    # Description is in the middle of the contour
                        mid_y = int((c.getStart().y() + c.getEnd().y()) / 2)

                        qp.setFont(QFont("Arial", 7))   # Smaller font for highlighted contour
                        qp.setPen(QColor(140, 90, 50))

                        qp.drawText(mid_x, mid_y, str(int(z)))
                
                    counter_normal += 1
                    pen.setColor(QColor(140, 90, 50))
                    pen.setWidth(1)

                qp.setPen(pen)
                qp.drawLine(c.getStart(), c.getEnd())
            
        #Draw points
        pen.setWidth(5)
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
        
        
    def setContours(self, contours, dz):
        #Set contour lines
        self.__contours = contours
        self.__dz = dz
    

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
        
    def setAspectScheme(self, scheme_index):
        # Saves the index of the color scheme
        self.__aspect_scheme = scheme_index

    def setSlopeScheme(self, scheme_index):
        # Saves the index of the color scheme
        self.__slope_scheme = scheme_index    
        