# This Python file uses the following encoding: utf-8
from PyQt5 import QtCore
from PyQt5 import QtWidgets, QtGui
from CustomMiniWidgets import MyDoubleSpinBox, MyComboBox
from LayerData import LayerData

class LayerWidget(QtWidgets.QWidget):
    def __init__(self,position,mode,data=None):
        QtWidgets.QWidget.__init__(self)

        #information from upper levels
        self.mode=mode
        """mode the layer is currently operating in"""
        self.position=position
        """position the layer currently has in the list of layers"""


        #flag to check whether calculations should happen or not. used for loading/startup process
        self.calculateFlag = 1
        """falg to help prevent calculation loops during live calculation"""
        self.customNameFlag = 0
        """flag to check whether layer has been given custom name"""

        #layouts
        #main layout
        self.mainLayout = QtWidgets.QVBoxLayout()
        """layout of the LayerWidget"""
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(10)

        #head layout
        self.head = QtWidgets.QWidget()
        """upper part of LayerWidget"""
        self.headButtons = QtWidgets.QWidget()
        """buttons located in upper part of LayerWidget"""

        self.headLayout = QtWidgets.QHBoxLayout()
        self.headLayout.setContentsMargins(0,0,0,0)
        self.headLayout.setSpacing(10)

        self.headButtonLayout = QtWidgets.QHBoxLayout()
        self.headButtonLayout.setContentsMargins(0,0,0,0)
        self.headButtonLayout.setSpacing(0)

 
        self.layerTitleLabel = QtWidgets.QLineEdit()
        """Title of layer"""
        self.layerTitleLabel.setFixedWidth(400)
        self.layerTitleLabel.editingFinished.connect(self.layerTitleEntered)

        self.layerDeleteButton = QtWidgets.QPushButton()
        """Delete button"""
        self.layerDeleteButton.clicked.connect(self.deleteButtonPressed)
        self.layerAddAfterButton = QtWidgets.QPushButton()
        """Add (after) button"""
        self.layerAddAfterButton.clicked.connect(self.addAfterButtonPressed)

        self.headButtonLayout.addWidget(self.layerAddAfterButton)
        self.headButtonLayout.addWidget(self.layerDeleteButton)
        self.headButtonLayout.setAlignment(QtCore.Qt.AlignRight)
        self.headButtons.setLayout(self.headButtonLayout)

        self.headLayout.addWidget(self.layerTitleLabel)
        self.headLayout.addWidget(self.headButtons)


        self.head.setLayout(self.headLayout)


        #body layout
        self.body = QtWidgets.QWidget()
        """main part of layer"""

        self.bodyLayout = QtWidgets.QGridLayout()
        self.bodyLayout.setContentsMargins(0,0,0,0)
        self.bodyLayout.setSpacing(10)

        self.layerWidthLabel = QtWidgets.QLabel()
        self.layerWidthDoubleSpinBox = MyDoubleSpinBox()
        """input/output of width"""
        self.layerWidthDoubleSpinBox.setSingleStep(0.001)
        self.layerWidthDoubleSpinBox.setMaximum(9.9999)
        self.layerWidthDoubleSpinBox.setMaximumWidth(100)
        self.layerWidthDoubleSpinBox.valueChanged.connect(self.widthChanged)

        self.layerWidthComboBox = MyComboBox()
        """unit selection for width"""
        self.layerWidthComboBox.addItems({"m"})
        self.layerWidthComboBox.addItems({"cm"})
        self.layerWidthComboBox.addItems({"mm"})

        self.layerWidthComboBox.currentIndexChanged.connect(self.widthFactorChanged)

        self.layerLambdaLabel = QtWidgets.QLabel()
        self.layerLambdaLabel.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignRight)
        self.layerLambdaDoubleSpinBox = MyDoubleSpinBox()
        """input/output of lambda"""
        self.layerLambdaDoubleSpinBox.setMinimum(0.000)
        self.layerLambdaDoubleSpinBox.setValue(0.01)
        self.layerLambdaDoubleSpinBox.setSingleStep(0.01)
        self.layerLambdaDoubleSpinBox.setMaximumWidth(100)
        self.layerLambdaDoubleSpinBox.valueChanged.connect(self.lambdaChanged)
        self.layerLambdaUnitLabel = QtWidgets.QLabel()

        self.layerResLabel = QtWidgets.QLabel()
        self.layerResLabel.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignRight)
        self.layerResDoubleSpinBox = MyDoubleSpinBox()
        """input/output of R"""
        self.layerResDoubleSpinBox.setDecimals(5)
        self.layerResDoubleSpinBox.setSingleStep(0.0001)
        self.layerResDoubleSpinBox.setMaximum(999.9999)
        self.layerResDoubleSpinBox.setEditable(0)
        self.layerResDoubleSpinBox.setMaximumWidth(100)
        self.layerResDoubleSpinBox.valueChanged.connect(self.rChanged)
        self.layerResUnitLabel = QtWidgets.QLabel()

        self.layerResGivenCheckBox = QtWidgets.QCheckBox(QtCore.QCoreApplication.translate("LayerWidget", "R gegeben "))
        """checkbox whether R is given and lambda should be calculated instead"""
        self.layerResGivenCheckBox.stateChanged.connect(self.resGivenCheckboxChanged)

        #data
        if(data is None):
            self.data=LayerData()
            """data of layer"""
            self.widthFactor = 1
            self.initData()
        else:
            self.data=data
            """data of layer"""
            self.updateValues()

        #assemble body layout
        self.bodyLayout.addWidget(self.layerWidthLabel,0,0)
        self.bodyLayout.addWidget(self.layerWidthDoubleSpinBox,0,1)
        self.bodyLayout.addWidget(self.layerWidthComboBox,0,2)
        self.bodyLayout.addWidget(self.layerLambdaLabel,0,3)
        self.bodyLayout.addWidget(self.layerLambdaDoubleSpinBox,0,4)
        self.bodyLayout.addWidget(self.layerLambdaUnitLabel,0,5)
        self.bodyLayout.addWidget(self.layerResLabel,0,6)
        self.bodyLayout.addWidget(self.layerResDoubleSpinBox,0,7)
        self.bodyLayout.addWidget(self.layerResUnitLabel,0,8)
        self.bodyLayout.addWidget(self.layerResGivenCheckBox,0,9)

        self.body.setLayout(self.bodyLayout)

        #bottom layout could be placed here if neccessary


        #check for mode, right now not really neccessary
        self.switchMode(self.mode)

        self.mainLayout.addWidget(self.head)
        self.mainLayout.addWidget(self.body)
        self.setLayout(self.mainLayout)

        """
        self.setStyleSheet("QWidget {"
        "background-color: #f0f0f0;"
        "}"
        "QPushButton{"
        "border: 0px solid #ff0000;"
        "color: rgb(255, 255, 255);"
        "padding: 5px;"
        "background-color: #7099D6;;"
        "}"

        "QPushButton:hover {"
        "border: 1px solid #333333;"
        "color: rgb(255, 255, 255);"
        "background-color: #2F63AF;"
        "}"
        "QPushButton:pressed {"
        "border: 1px solid #333333;"
        "color: rgb(255, 255, 255);"
        "background-color: #12499A;"
        "}"
        "QPushButton:disabled {"
        "border: 0px solid #333333;"
        "color: rgb(150, 150, 150);"
        "background-color: #134078;"
        "};")
        """

        self.retranslateUi()

        #set position and text
        self.updatePos(self.position)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        if self.customNameFlag == 0:
            self.layerTitleLabel.setText(_translate("LayerWidget", "Schicht "))

        self.layerWidthLabel.setText(_translate("LayerWidget", "Dicke:"))

        self.layerLambdaLabel.setText(_translate("LayerWidget", "λ:"))
        self.layerLambdaUnitLabel.setText(_translate("LayerWidget", "Wm<sup>-1</sup>K<sup>-1</sub>"))

        self.layerResLabel.setText(_translate("LayerWidget", "R_i:"))
        self.layerResUnitLabel.setText(_translate("LayerWidget", "m<sup>2</sup>KW<sup>-1</sub>"))

        self.layerAddAfterButton.setText(_translate("LayerWidget", "+"))
        self.layerDeleteButton.setText(_translate("LayerWidget", "–"))

        #self.layerTempInLabel.setText(_translate("LayerWidget", "Temp_in:"))
        #self.layerTempOutLabel.setText(_translate("LayerWidget", "Temp_out"))
        #self.layerTempUnitLabel1.setText(_translate("LayerWidget", "°C"))
        #self.layerTempUnitLabel2.setText(_translate("LayerWidget", "°C"))

    #delete this layer
    def deleteButtonPressed(self):
        self.parent().parent().parent().parent().parent().deleteLayer(self.position)

    #add layer beneath
    def addAfterButtonPressed(self):
        self.parent().parent().parent().parent().parent().addLayer(self.position+1)

    #update own position and modify text
    def updatePos(self, pos):
        """update own position and modify text"""
        self.position=pos
        if self.customNameFlag==0:
            self.layerTitleLabel.setText(QtCore.QCoreApplication.translate("LayerWidget", "Schicht ")+str(pos+1))
        self.layerResLabel.setText(QtCore.QCoreApplication.translate("LayerWidget", "R")+"<sub>"+str(pos+1)+"</sub>"+":")

    #enable/disable delete button
    def setRemovable(self, flag):
        """enable/disable delete button"""
        if flag == True:
            self.layerDeleteButton.setEnabled(1)
        else:
            self.layerDeleteButton.setEnabled(0)

    #enable/disable lambda box
    def resGivenCheckboxChanged(self):
        """enable/disable lambda box"""
        if self.layerResGivenCheckBox.checkState():
            self.layerLambdaDoubleSpinBox.setEditable(0)
            self.layerResDoubleSpinBox.setEditable(1)
        else:
            self.layerLambdaDoubleSpinBox.setEditable(1)
            self.layerResDoubleSpinBox.setEditable(0)

    #modify mode of layer
    def switchMode(self,mode):
        """modify mode of layer"""
        self.mode = mode

    #value changes
    def initData(self):
        self.data.width=self.layerWidthDoubleSpinBox.value()*self.widthFactor
        self.data.lambda_=self.layerLambdaDoubleSpinBox.value()

    def widthChanged(self):
        self.data.width=self.layerWidthDoubleSpinBox.value()*self.widthFactor
        self.calculate()

    def lambdaChanged(self):
        self.data.lambda_=self.layerLambdaDoubleSpinBox.value()
        self.calculate()

    def rChanged(self):
        self.data.r=self.layerResDoubleSpinBox.value()
        self.calculate()

    def widthFactorChanged(self):
        index = self.layerWidthComboBox.currentIndex()
        self.data.widthUnit=index
        if index == 0:
            self.widthFactor = 1
            self.layerWidthDoubleSpinBox.setMaximum(9.9999)
            self.layerWidthDoubleSpinBox.setDecimals(4)
            self.layerWidthDoubleSpinBox.setSingleStep(0.001)
        elif index == 1:
            self.widthFactor = 0.01
            self.layerWidthDoubleSpinBox.setMaximum(999.99)
            self.layerWidthDoubleSpinBox.setDecimals(2)
            self.layerWidthDoubleSpinBox.setSingleStep(0.1)
        elif index == 2:
            self.widthFactor = 0.001
            self.layerWidthDoubleSpinBox.setMaximum(9999.9)
            self.layerWidthDoubleSpinBox.setDecimals(1)
            self.layerWidthDoubleSpinBox.setSingleStep(0.1)
        self.widthChanged()
        self.calculate()

    def calculate(self):
        """calculation of layer and then overall calculation"""
        if(self.calculateFlag):
            if self.layerResGivenCheckBox.checkState():
                self.calculate_lambda()
            else:
                self.calculate_r()
            self.parent().parent().parent().parent().parent().calculate()

    def calculate_r(self):
        """subfunction of calculate, calculates R for layer"""
        if(self.calculateFlag):
            self.calculateFlag=0
            try:
                self.data.calculate()
                self.layerLambdaDoubleSpinBox.setBackGroundColor(QtGui.QColor(255,255,255))
                self.layerResDoubleSpinBox.setValue(self.data.r)
            except ZeroDivisionError:
                self.layerLambdaDoubleSpinBox.setBackGroundColor(QtGui.QColor(255,0,0))
            self.calculateFlag=1

    def calculate_lambda(self):
        """subfunction of calculate, calculates lambda for layer"""
        if(self.calculateFlag):
            self.calculateFlag=0
            try:
                self.data.calculate_lambda()
                self.layerResDoubleSpinBox.setBackGroundColor(QtGui.QColor(255,255,255))
                self.layerLambdaDoubleSpinBox.setValue(self.data.lambda_)
            except ZeroDivisionError:
                self.layerResDoubleSpinBox.setBackGroundColor(QtGui.QColor(255,0,0))
            self.calculateFlag=1

    def updateValues(self):
        """updates values in layer with corresponding values from data"""
        self.calculateFlag=0
        if self.data.widthUnit==0:
            self.widthFactor=1
        elif self.data.widthUnit==1:
            self.widthFactor=0.01
        else:
            self.widthFactor=0.001
        self.layerWidthDoubleSpinBox.setValue(self.data.width/self.widthFactor)
        self.layerWidthComboBox.setCurrentIndex(self.data.widthUnit)
        self.layerLambdaDoubleSpinBox.setValue(self.data.lambda_)
        self.layerResDoubleSpinBox.setValue(self.data.r)
        if self.data.name != "":
            self.customNameFlag = 1
            self.layerTitleLabel.setText(self.data.name)
        self.calculateFlag=1

    def layerTitleEntered(self):
        self.data.name = self.layerTitleLabel.text()
        self.customNameFlag = 1
        