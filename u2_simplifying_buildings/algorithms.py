from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
import numpy as np
import numpy.linalg as np2

class Algorithms:
    
    def __init__(self):
        self.sigma = 0
        pass
    
    def get2VectorsAngle(self, p1:QPointF, p2:QPointF, p3:QPointF, p4:QPointF):
        #Angle between two vectors
        ux = p2.x() - p1.x()    
        uy = p2.y() - p1.y()
        
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()    
        
        #Dot product
        dot = ux*vx + uy*vy
        
        #Norms
        nu = (ux**2 + uy**2)**0.5
        nv = (vx**2 + vy**2)**0.5
        
        #Correct interval
        arg = dot/(nu*nv)
        arg = max(-1, min(1,arg)) 
        
        return acos(arg)
    
    
    def createCH(self, pol:QPolygonF):
        #Create Convex Hull using Jarvis Scan
        ch = QPolygonF()
        
        #SINGULAR CASE 1: Not enough points
        #If there are less than 3 points, we can't create a hull
        if len(pol) < 3:
            return pol
        
        #Find pivot q (minimize y)
        q = min(pol, key = lambda k: k.y())

        #SINGULAR CASE 2: Safety (Initial vector)
        #We need a point strictly to the left to create a horizontal vector, false point
        pj = q
        pj1 = QPointF(q.x() - 100, q.y())
        
        #Add to CH
        ch.append(pj)
        
        #Find all points of CH
        while True:
            #Maximum and its index
            omega_max = 0
            index_max = -1
            
            #Browse all points
            for i in range(len(pol)):
                
                #Different points
                if pj != pol[i]:
                    
                    #Compute omega
                    omega = self.get2VectorsAngle(pj, pj1, pj, pol[i])
            
                    #Actualize maximum
                    if(omega > omega_max):
                        omega_max = omega
                        index_max = i
                        
                    #SINGULAR CASE 3: Collinear points
                    #If the angle is exactly the same, pick the point that is further away
                    elif omega == omega_max:
                        #Compute distance to current max point (without sqrt to save time)
                        dx_max = pol[index_max].x() - pj.x()
                        dy_max = pol[index_max].y() - pj.y()
                        dist_max = dx_max**2 + dy_max**2
                        
                        #Compute distance to this new point
                        dx_i = pol[i].x() - pj.x()
                        dy_i = pol[i].y() - pj.y()
                        dist_i = dx_i**2 + dy_i**2
                        
                        #If the new point is further away, overwrite the index
                        if dist_i > dist_max:
                            index_max = i
                    
            #Add point to the convex hull
            ch.append(pol[index_max])
            
            #Reasign points
            pj1 = pj
            pj = pol[index_max]
            
            # Stopping condition
            if pj == q:
                break
            
        return ch
    
    
    def createMMB(self, pol:QPolygonF):
        # Create min max box and compute its area

        #Points with extreme coordinates        
        p_xmin = min(pol, key = lambda k: k.x())
        p_xmax = max(pol, key = lambda k: k.x())
        p_ymin = min(pol, key = lambda k: k.y())
        p_ymax = max(pol, key = lambda k: k.y())
        
        #Create vertices
        v1 = QPointF(p_xmin.x(), p_ymin.y())
        v2 = QPointF(p_xmax.x(), p_ymin.y())
        v3 = QPointF(p_xmax.x(), p_ymax.y())
        v4 = QPointF(p_xmin.x(), p_ymax.y())
        
        #Create new polygon
        mmb = QPolygonF([v1, v2, v3, v4])
        
        #Area of MMB
        area = (v2.x() - v1.x()) * (v3.y() - v2.y())
        
        return mmb, area
     

    def rotatePolygon(self, pol:QPolygonF, sig:float):
        #Rotate polygon according to a given angle
        pol_rot = QPolygonF()

        #Process all polygon vertices
        for i in range(len(pol)):

            #Rotate point
            x_rot = pol[i].x() * cos(sig) - pol[i].y() * sin(sig)
            y_rot = pol[i].x() * sin(sig) + pol[i].y() * cos(sig)

            #Create QPoint
            vertex = QPointF(x_rot, y_rot)

            # Add vertex to rotated polygon
            pol_rot.append(vertex)

        return pol_rot
    
    
    def createMBR(self, building:QPolygonF):
        #Create minimum bounding rectangle using repeated construction of mmb
        sigma_min = 0
        
        #Convex hull
        ch = self.createCH(building)
        
        #Initialization
        mmb_min, area_min = self.createMMB(ch)
        
        # Process all edges of convex hull
        n = len(ch)
        for i in range(n):
            #Coordinate differences
            dx = ch[(i+1)%n].x() - ch[i].x()
            dy = ch[(i+1)%n].y() - ch[i].y()
            
            # Compute direction
            sigma = atan2(dy, dx)
            
            #Rotate convex hull
            ch_r = self.rotatePolygon(ch, -sigma)
        
            #Compute min-max box
            mmb, area = self.createMMB(ch_r)
            
            #Did we find a better min-max box?
            if area < area_min:    
                #Update minimum
                area_min = area
                mmb_min = mmb
                sigma_min = sigma
                
        self.sigma = sigma_min
        #Back rotation
        return  self.rotatePolygon(mmb_min, sigma_min) 

    
    def getArea(self, pol:QPolygonF):
        #Compute area    
        area = 0
        n = len(pol)
        
        # Process all vertices
        for i in range(n):
            area += pol[i].x() * (pol[(i + 1) % n].y() - pol[(i - 1 + n) % n].y())
            
        return abs(area)/2    
    
        
    def resizeRectangle(self, building:QPolygonF, mbr: QPolygonF):
        #Resizing rectangle area to match building area
        
        #Area of the rectangle
        A = self.getArea(mbr)
        
        #Area of the building
        Ab = self.getArea(building)
        
        #Fraction of both areas
        k = Ab / A
        
        #Compute centroid of the rectangle
        x_c = (mbr[0].x()+mbr[1].x()+mbr[2].x()+mbr[3].x()) / 4
        y_c = (mbr[0].y()+mbr[1].y()+mbr[2].y()+mbr[3].y()) / 4
        
        #Compute vectors 
        v1_x = mbr[0].x() - x_c
        v1_y = mbr[0].y() - y_c 
        
        v2_x = mbr[1].x() - x_c
        v2_y = mbr[1].y() - y_c 

        v3_x = mbr[2].x() - x_c
        v3_y = mbr[2].y() - y_c 
        
        v4_x = mbr[3].x() - x_c
        v4_y = mbr[3].y() - y_c
        
        #Resize vectors v1 - v4 
        v1_x_res = v1_x * sqrt(k)
        v1_y_res = v1_y * sqrt(k)
        
        v2_x_res = v2_x * sqrt(k)
        v2_y_res = v2_y * sqrt(k)
        
        v3_x_res = v3_x * sqrt(k)
        v3_y_res = v3_y * sqrt(k)
        
        v4_x_res = v4_x * sqrt(k)
        v4_y_res = v4_y * sqrt(k)
        
        #Compute new vertices
        p1_x = v1_x_res + x_c  
        p1_y = v1_y_res + y_c 
        
        p2_x = v2_x_res + x_c  
        p2_y = v2_y_res + y_c 
        
        p3_x = v3_x_res + x_c  
        p3_y = v3_y_res + y_c 
        
        p4_x = v4_x_res + x_c  
        p4_y = v4_y_res + y_c
        
        # Compute new coordinates
        p1 = QPointF(p1_x,  p1_y)
        p2 = QPointF(p2_x,  p2_y)
        p3 = QPointF(p3_x,  p3_y)
        p4 = QPointF(p4_x,  p4_y)   
        
        #Create polygon
        mbr_res = QPolygonF()
        mbr_res.append(p1)
        mbr_res.append(p2)
        mbr_res.append(p3)
        mbr_res.append(p4)
       
        return mbr_res
    
    
    def simplifyBuildingMBR(self, building:QPolygonF):
        #Simplify building using MBR
        mbr = self.createMBR(building)
        
        #Resize rectangle
        mbr_res = self.resizeRectangle(building, mbr)
        
        return mbr_res
    
    
    
    def simplifyBuildingPCA(self, building:QPolygonF):
        #Simplify building using PCA
        X, Y = [], []
        
        #Convert polygon vertices to matrix
        for p in building:
            X.append(p.x())
            Y.append(p.y())
            
        #Create A
        A = np.array([X, Y])

        #Compute covariance matrix
        C = np.cov(A)
        
        #Singular Value Decomposition
        [U, S, V] = np2.svd(C)
        
        #Compute direction of the principal component
        sigma = atan2(V[0][1], V[0][0])

        #Rotate building by -sigma
        build_rot = self.rotatePolygon(building, -sigma)
        
        #Create min-max box
        mmb, area = self.createMMB(build_rot)
        
        #Rotate min-max box by sigma
        mbr = self.rotatePolygon(mmb, sigma)
        
        #Resize min-max box
        mbr_res = self.resizeRectangle(building, mbr)
        
        self.sigma = sigma
        return mbr_res
        
    def simplifyBuildingWB(self, building:QPolygonF):
        # Simplify building using Weighted Bisector
        n = len(building)
        diagonals = []

        edges = []

        # Pairing all points to creater diagonals
        for i in range(n):
            for j in range(i+2,n):      # i+2 used to not pair points which are on the edge of the bulding
                                        # i+1 would be the next point in the polygon, i+2 is the diagonal
                # Condition to ensure that the last point doesnt connect with the first - AI helped here
                if i == 0 and j == n-1:
                    continue

                p1 = building[i]        
                p2 = building[j]

                # Difference in coordinates to calculate lenght
                dx = p2.x() - p1.x()
                dy = p2.y() - p1.y()

                s = (dx**2 + dy**2)**0.5

                # Calculating sigma
                sigma = atan2(dy,dx)

                # Sigma lay in 0 to pi - AI helped here
                if sigma < 0:
                    sigma += pi

                diagonals.append((s,sigma))

        # Sorting the list to get the longest diagonals
        diagonals.sort(key=lambda x: x[0], reverse=True)

        # Choosing the 2 longest diagonals with their sigma
        s1 = diagonals[0][0]
        sigma1 = diagonals[0][1]

        s2 = diagonals[1][0]
        sigma2 = diagonals[1][1]
        
        angle_tolerance = 10 * pi / 180 # 10 degree difference of diagonals

        # Going through the list to get second longest diagonal which is in the tolerance => not parallel to the longest
        for i in range(1, len(diagonals)):
            s_cand = diagonals[i][0]
            sigma_cand = diagonals[i][1]
            
            # Calculating the difference of the diagonals
            diff = abs(sigma1 - sigma_cand)
            if diff > pi / 2:           # Condition that 0° is the same as 180°
                diff = pi - diff
                
            if diff > angle_tolerance:
                s2 = s_cand
                sigma2 = sigma_cand
                break

        # Condition to have the the correct angles
        # Subtracting pi so the sigma lays in 0 to pi range
        if abs(sigma1-sigma2)> pi/2:
            if sigma1 > sigma2:
                sigma1 -= pi
            else:
                sigma2 -= pi        

        # Calculating direction with using weights
        sigma_weight = (s1*sigma1 + s2*sigma2)/(s1+s2)

        # Rotate, MMB, rotate MMB, resize - same as for PCA
        #Rotate building by -sigma_weight
        build_rot = self.rotatePolygon(building, -sigma_weight)
        
        #Create min-max box
        mmb, area = self.createMMB(build_rot)
        
        #Rotate min-max box by sigma
        mbr = self.rotatePolygon(mmb, sigma_weight)
        
        #Resize min-max box
        mbr_res = self.resizeRectangle(building, mbr)
        
        self.sigma = sigma_weight
        return mbr_res
        
    
    
    def simplifyBuildingLongestEdge (self, building:QPolygonF):
        #Using Longest Edge method to simplify buildings
        
        n = len(building)
        max_length = 0
        best_angle = 0
        
        #Finding the longest edge, using for cycle 
        for i in range(n):
            p1 = building[i]
            p2 = building[(i + 1) % n]
            
            #Coordinate differences
            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            
            #Length of the edge
            length = sqrt(dx**2 + dy**2)
            
            #Update maximum length and best angle
            if length > max_length:
                max_length = length
                best_angle = atan2(dy, dx)
                
                
                
        #Rotate, MMB, rotate MMB, resize - same as for PCA
        #Rotate building by -best_angle
        build_rot = self.rotatePolygon(building, -best_angle)
        
        #Create min-max box
        mmb, area = self.createMMB(build_rot)
        
        #Rotate min-max box by best_angle
        mbr = self.rotatePolygon(mmb, best_angle)
        
        #Resize rectangle 
        mbr_res = self.resizeRectangle(building, mbr)
        
        self.sigma = best_angle
        return mbr_res        
    
    
    
    def simplifyBuildingWallAverage(self, building:QPolygonF):
        #Using Wall Average method to simplify buildings
        
        n = len(building)
        sum_angles_lenghts = 0
        sum_lenghts = 0
        
        #Finding the longest edge, using for cycle 
        for i in range(n):
            p1 = building[i]
            p2 = building[(i + 1) % n]
            
            #Coordinate differences
            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            
            #Length of the edge
            length = sqrt(dx**2 + dy**2)
            
            #Angle of the edge
            angle = atan2(dy, dx)
            
            #Reducing angle to 0 - pi
            angle = angle % (pi/2)
            
            #Update sums
            sum_angles_lenghts += angle * length
            sum_lenghts += length
        
        #Computing average angle
        best_angle = 0
        if sum_lenghts > 0:
            best_angle = sum_angles_lenghts / sum_lenghts
            
        
        
        #Rotate, MMB, rotate MMB, resize - same as for PCA, Longest edge...
        #Rotate building by -best_angle
        build_rot = self.rotatePolygon(building, -best_angle)
        
        #Create min-max box
        mmb, area = self.createMMB(build_rot)
        
        #Rotate min-max box by best_angle
        mbr = self.rotatePolygon(mmb, best_angle)
        
        #Resize rectangle 
        mbr_res = self.resizeRectangle(building, mbr)
        self.sigma = best_angle
        return mbr_res 
    
    """
     WALL AVERAGE, help with AI:

    1. Weighted Average: I used wall length as a weight (`angle * length`). This ensures that long, main walls dictate the building's main direction. A simple average would give too much power to tiny wall bumps.

    2. Modulo for Right Angles: To make perpendicular walls vote for the same main direction, I used `angle % (pi/2)`. This safely removes 90-degree differences using a single, stable line of code instead of complex math.
    """
    
    
    #Results evaluation 
    def getDirection(self, p1: QPointF, p2: QPointF):
        #Calculate differences in coordinates
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        
        #Calculate and return angle using atan2
        angle = atan2(dy, dx)
        return angle


    def ResultsEvaluation (self, building: QPolygonF, sigma):
        n = len(building)

        ri_list = []

        #Calculate ri for each edge
        for i in range(n):
            #First point
            p1 = building[i]
            #Second point with use od modulo
            next_indx = (i + 1) % n
            p2 = building[next_indx]

            sigma_i = self.getDirection(p1, p2)

            sigma_diff = sigma_i - sigma

            #Calculate ki from presentation
            ki = (2 * sigma_diff) / pi

            #Calculate ri
            ri = (ki - round(ki)) * (pi / 2)

            #Now add back ri to the list
            ri_list.append(ri)

        #Compute average for further action
        r_sum = 0
        for ri in ri_list:
            r_sum = r_sum + ri

        r_mean = r_sum / n

        #Calculate sum of squares
        sum_squares = 0
        for ri in ri_list:
            diff = ri - r_mean

            #Square the difference
            squared_diff = diff **2

            #Add to total sum
            sum_squares = sum_squares + squared_diff
            
        #Calculate the final result in radians, last step in the presentation, just computing the final result
        fraction = pi / (2 * n)
        root = sqrt(sum_squares)
        result_rad = fraction * root
        
        #Convert result from radians to degrees
        result_deg = result_rad * (180 / pi)
        
        #Return the final angle
        return result_deg
            
            
                
                