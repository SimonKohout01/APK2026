from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_Settings(object):
    def __init__(self):
        #Parameters of contour lines
        self.zmin = 150
        self.zmax = 2000
        self.dz = 25
    
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(403, 240)
        self.verticalLayout = QtWidgets.QVBoxLayout(Settings)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(parent=Settings)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setText("Z min:")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        
        self.spinBox = QtWidgets.QSpinBox(parent=self.groupBox)
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(2000)
        self.spinBox.setSingleStep(10)
        self.gridLayout.addWidget(self.spinBox, 0, 1, 1, 1)
        
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_4.setText("Z max:")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        
        self.spinBox_2 = QtWidgets.QSpinBox(parent=self.groupBox)
        self.spinBox_2.setMinimum(0)
        self.spinBox_2.setMaximum(2000)
        self.spinBox_2.setSingleStep(10)
        self.gridLayout.addWidget(self.spinBox_2, 1, 1, 1, 1)
        
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_6.setText("Step (dz):")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        
        self.spinBox_3 = QtWidgets.QSpinBox(parent=self.groupBox)
        self.spinBox_3.setMinimum(1)
        self.spinBox_3.setMaximum(100)
        self.spinBox_3.setSingleStep(1)
        self.gridLayout.addWidget(self.spinBox_3, 2, 1, 1, 1)
        
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Settings)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(Settings.accept)
        self.buttonBox.rejected.connect(Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)
        
        # Set default values at the start
        self.spinBox.setValue(self.zmin)
        self.spinBox_2.setValue(self.zmax)
        self.spinBox_3.setValue(self.dz)