from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import sqrt, acos, pi

class Algorithms:
    
    def getPointPolygonPositionRC(self, q:QPointF, pol:QPolygonF):
        #Analyze point and polygon position using ray crossing algorithm
        
        if len(pol) < 3:
            return 0
        
        # Min-max Box filter
        # Define initializating value of Min-Max Box of created polygon
        min_x = pol[0].x()
        max_x = pol[0].x()
        min_y = pol[0].y()
        max_y = pol[0].y()
        
        # Determine the min and max points 
        for i in range (len(pol)):
            if pol[i].x() < min_x:
                min_x = pol[i].x()
            if pol[i].x() > max_x:
                max_x = pol[i].x()
            if pol[i].y() < min_y:
                min_y = pol[i].y()
            if pol[i].y() > max_y:
                max_y = pol[i].y()
        
        # Checking if x of y coordinate of our point is lower or higher than the Min-max box -> definitely outside the polygon
        if q.x() < min_x or q.x() > max_x or q.y() < min_y or q.y() > max_y:
            return -2   # Point lays outside the polygon checked by Min-max box filter


        #Intersects 
        k = 0  
        #Left intersects counter
        kl = 0 
      
        #Number of vertices
        n = len(pol) 
        
        #Process all polygon edges
        for i in range(n):
            #Start point of the edge
            xi = pol[i].x() - q.x()
            yi = pol[i].y() - q.y()
            
            #End point of the edge        
            xi1 = pol[(i+1)%n].x() - q.x()
            yi1 = pol[(i+1)%n].y() - q.y()
            
            # Check if q is exactly on vertex
            if xi == 0 and yi == 0:
                return -1
            
            #Find suitable segment
            if (yi1 > 0) and (yi<= 0) or (yi > 0) and (yi1 <= 0):
                
                #Compute intersection
                xm = (xi1 * yi - xi * yi1) / (yi1 - yi) 
                
                # Intersection is 0, so q is on edge
                if xm == 0:
                    return -1
                
                #Correct intersection
                if xm > 0:
                    
                    #Increment number of intersections 
                    k = k + 1   
                
                elif xm < 0:
                    kl = kl + 1
                    
        #Check if point is on the edge
        if (k % 2) != (kl % 2):
            return -1

                        
        #Point is inside the polygon
        if k % 2 == 1:
            return 1 
        #Point is outside the polygon
        return 0    
    
    
    
    
# Analyze point and polygon position using WINDING NUMBER
    def getPointPolygonPositionWN(self, q:QPointF, pol:QPolygonF):
        
        if len(pol) < 3:
            return 0 
           
        # Min-max Box filter
        # Define initializating value of Min-Max Box of created polygon
        min_x = pol[0].x()
        max_x = pol[0].x()
        min_y = pol[0].y()
        max_y = pol[0].y()
        
        # Determine the min and max points 
        for i in range (len(pol)):
            if pol[i].x() < min_x:
                min_x = pol[i].x()
            if pol[i].x() > max_x:
                max_x = pol[i].x()
            if pol[i].y() < min_y:
                min_y = pol[i].y()
            if pol[i].y() > max_y:
                max_y = pol[i].y()
        
        # Checking if x of y coordinate of our point is lower or higher than the Min-max box -> definitely outside the polygon
        if q.x() < min_x or q.x() > max_x or q.y() < min_y or q.y() > max_y:
            return -2   # Point lays outside the polygon checked by Min-max box filter

        wn_total = 0.0
        n = len(pol)
        epsilon = 1.0e-7 #Tolerance for float numbers
        
        
        for i in range(n):
            point1 = pol[i]
            point2 = pol[(i + 1) % n]
            
            #Vectors from point q to edge
            v1_x = point1.x() - q.x()
            v1_y = point1.y() - q.y()
            
            v2_x = point2.x() - q.x()
            v2_y = point2.y() - q.y()
            
            #Get vector length
            dist1 = sqrt(v1_x**2 + v1_y**2)
            dist2 = sqrt(v2_x**2 + v2_y**2)
            
            #If distance is 0, q is on vertex, similar like in RC
            if dist1 == 0 or dist2 == 0:
                return -1 
                
            # Dot product is for calculate the angle size between vectors, cross product is for determine the direction of the turn (left or right)
            dot_product = (v1_x * v2_x) + (v1_y * v2_y)
            cross_product = (v1_x * v2_y) - (v1_y * v2_x)
            
            #Calculate angle and fix float bugs
            val = dot_product / (dist1 * dist2)
            if val > 1.0: val = 1.0
            if val < -1.0: val = -1.0
            angle = acos(val)
             
            #If no turn and angle is 180 degrees its on the edge
            if abs(cross_product) < epsilon and abs(angle - pi) < epsilon:
                return -1
                
            #Add or subtract angle
            if cross_product > 0:
                wn_total += angle # left side
            elif cross_product < 0:
                wn_total -= angle # right side
                
        #If total is 360 degrees (2*pi), it is inside the polygon
        if abs(abs(wn_total) - 2 * pi) < epsilon:
            return 1 
        
        return 0 #Point is outside the polygon