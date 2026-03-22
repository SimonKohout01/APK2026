from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import *
import shapefile

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(1043, 948)
        self.centralwidget = QtWidgets.QWidget(parent=MainForm)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(parent=self.centralwidget)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        MainForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1043, 33))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuInput = QtWidgets.QMenu(parent=self.menubar)
        self.menuInput.setObjectName("menuInput")
        self.menuAnalyze = QtWidgets.QMenu(parent=self.menubar)
        self.menuAnalyze.setObjectName("menuAnalyze")
        MainForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainForm)
        self.statusbar.setObjectName("statusbar")
        MainForm.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainForm)
        self.toolBar.setObjectName("toolBar")
        MainForm.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        self.actionOpen = QtGui.QAction(parent=MainForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExit = QtGui.QAction(parent=MainForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName("actionExit")
        self.actionPoint_polygon = QtGui.QAction(parent=MainForm)
        self.actionPoint_polygon.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/pointpol.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPoint_polygon.setIcon(icon2)
        self.actionPoint_polygon.setObjectName("actionPoint_polygon")
        self.actionClear = QtGui.QAction(parent=MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/clear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear.setIcon(icon3)
        self.actionClear.setObjectName("actionClear")
        self.actionRay_Crossing = QtGui.QAction(parent=MainForm)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/ray.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionRay_Crossing.setIcon(icon4)
        self.actionRay_Crossing.setObjectName("actionRay_Crossing")
        self.actionWinding_Number = QtGui.QAction(parent=MainForm)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/winding.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWinding_Number.setIcon(icon5)
        self.actionWinding_Number.setObjectName("actionWinding_Number")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuInput.addAction(self.actionPoint_polygon)
        self.menuInput.addSeparator()
        self.menuInput.addAction(self.actionClear)
        self.menuAnalyze.addAction(self.actionRay_Crossing)
        self.menuAnalyze.addAction(self.actionWinding_Number)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuInput.menuAction())
        self.menubar.addAction(self.menuAnalyze.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRay_Crossing)
        self.toolBar.addAction(self.actionWinding_Number)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPoint_polygon)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)
        
        #Connect signals and slots 
        self.actionPoint_polygon.triggered.connect(self.changeStatusClick)
        self.actionClear.triggered.connect(self.clearClick)
        self.actionOpen.triggered.connect(self.openFile)   # For importing .shp file
        
        #Connect signals and slots WN
        self.actionRay_Crossing.triggered.connect(self.analyzePointAndPositionClick)
        self.actionWinding_Number.triggered.connect(self.analyzeWindingNumberClick)
        
        
    def changeStatusClick(self):
        #User defined slot, change source
        self.Canvas.changeStatus()
        
    def clearClick(self):
        #User defined slot, clear data
        self.Canvas.clearData()    
        
    def analyzePointAndPositionClick(self):
        #Get point
        q = self.Canvas.getQ()
        
        #Get polygon
        pols = self.Canvas.getPols()
      
        #Create new object
        a = Algorithms()
        
        result = -2
        highlight_index = -1

        #Analyze point and polygon position
        for i in range(len(pols)):
            res = a.getPointPolygonPositionRC(q, pols[i])
            if res == 1 or res == -1:
                result = res    
                highlight_index = i
                break
            elif res == 0:
                result = 0

        self.Canvas.setResult(result, highlight_index)
        
        #Create message box
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle('Point and polygon position')
        
        #Set results 
        if result == 1:
            mb.setText("Point is inside the polygon - RC")
        elif result == 0: 
            mb.setText("Point is outside the polygon - RC") 
        elif result == -1:
            mb.setText("Point is on the Edge or Vertex of the polygon - RC")
        elif result == -2:
            mb.setText("Point is outside the polygon - Min-Max Box filter")    
        #Show message box
        mb.exec()
        
        
        
        
    def analyzeWindingNumberClick(self):
        q = self.Canvas.getQ()
        pols = self.Canvas.getPols()
      
        #Create new object
        a = Algorithms()

        result = -2
        hightlight_index = -1

        for i in range(len(pols)):
            res = a.getPointPolygonPositionWN(q, pols[i])

            if res == 1 or res == -1:
                result = res
                hightlight_index = i
                break
            elif res == 0:
                result = 0
        self.Canvas.setResult(result, hightlight_index)
        
        mb = QtWidgets.QMessageBox()
        mb.setWindowTitle('Point and polygon position')
        
        if result == 1:
            mb.setText("Point is inside the polygon - WN")
        elif result == 0: 
            mb.setText("Point is outside the polygon - WN") 
        elif result == -1:
            mb.setText("Point is on the Edge or Vertex of the polygon - WN")
        elif result == -2:
            mb.setText("Point is outside the polygon - Min-Max Box filter")
            
        mb.exec()


    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Analyze point and polygon position"))
        self.menuFile.setTitle(_translate("MainForm", "File"))
        self.menuInput.setTitle(_translate("MainForm", "Input"))
        self.menuAnalyze.setTitle(_translate("MainForm", "Analyze"))
        self.toolBar.setWindowTitle(_translate("MainForm", "toolBar"))
        self.actionOpen.setText(_translate("MainForm", "Open"))
        self.actionExit.setText(_translate("MainForm", "Exit"))
        self.actionPoint_polygon.setText(_translate("MainForm", "Point / polygon"))
        self.actionClear.setText(_translate("MainForm", "Clear"))
        self.actionRay_Crossing.setText(_translate("MainForm", "Ray Crossing"))
        self.actionWinding_Number.setText(_translate("MainForm", "Winding Number"))

    # LOADING  SHAPEFILE
    # AI used here for a correction of syntax and creating workflow/pseudocode of choosing and loading .shp
    def openFile(self):
        # Pop-up window for searching the shp 
        file_shp, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Open .shp", "", "")
        
        # Then loading .shp
        if file_shp:
            self.loadShapefile(file_shp)

    def loadShapefile(self, file_path):
        # Loading .shp from library
        sf = shapefile.Reader(file_path)
        shapes = sf.shapes()

        # Define initializating value of Min-Max Box of our .shp
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')
        
        # Determine the min and max points 
        for shape in shapes:
            for point in shape.points:
                if point[0] < min_x: 
                    min_x = point[0]
                if point[0] > max_x: 
                    max_x = point[0]
                if point[1] < min_y: 
                    min_y = point[1]
                if point[1] > max_y: 
                    max_y = point[1]

        print(min_x, max_x, min_y, max_y)
        # Calculating a scale so it fits to the canvas window
        zoom = 300 / max(max_x - min_x, max_y - min_y)

        # Clear canvas
        self.Canvas.clearData()

        # Create a list of polygons
        list_pols = []

        # Get polygon
        pol = self.Canvas.getPols()

        # Scaling all points in the .shp and creating a polygon
        # +100 sets the new coordinates to left and down so the polygon has stable position
        for shape in shapes:
            pol = QtGui.QPolygonF()
            for point in shape.points:
                x = (point[0] - min_x) * zoom + 100
                y = (max_y - point[1] ) * zoom + 100
            
                pol.append(QtCore.QPointF(x, y))
            list_pols.append(pol)
        self.Canvas.setPols(list_pols)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())