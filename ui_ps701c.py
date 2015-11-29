#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ps701c.ui'
#
# Created: Wed Nov 18 12:06:41 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import PyTango
from PyTango import Except
#from logilab.common.fileutils import lines

from dialogParameter import SettingsDialog
from datetime import datetime
# import os.path
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from taurus.qt.qtgui.input import TaurusWheelEdit
from taurus.qt.qtgui.button import TaurusCommandButton
from taurus.qt.qtgui.display import TaurusLCD
from taurus.qt.qtgui.input import TaurusValueSpinBox
import common_func

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(QtGui.QMainWindow):
    def setupUi(self, MainWindow,devices):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))

        self.devices = devices
        self.tangoDevices = list() # list of tango-devices

        self.nMaxRows = 10 # maximal number of rows in mainWidget
        self.nMinRowsForDecrSize = 3 # минимальное число строк для изменения размера

        self.deviceNameLabel = list()
        self.statusLed = list()
        self.voltageValueSpinBox = list()
        self.setVoltageButton = list()
        self.measLCD = list()
        self.voltageLabel = list()

        for i in range(0,len(self.devices)):
            self.setWidgetView(i) # установка параметров виджетов

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.reconnectButton = TaurusCommandButton(self.centralwidget)
        self.reconnectButton.setObjectName(_fromUtf8("reconnectButton"))

        self.settingsButton = QtGui.QPushButton(self.centralwidget)
        self.settingsButton.setObjectName(_fromUtf8("settingsButton"))

        #clicked connect
        # self.settingsButton.clicked.connect(self.showDialog)

        MainWindow.setCentralWidget(self.centralwidget)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.layouts(MainWindow)

        # self.centerOnScreen()
        self.centerOnScreen(MainWindow)
        common_func.setCommonProp(self)

        self.widgetSizes(MainWindow) # установка размеров виджетов

        # if len(self.devices) < 11:
        #     sep =
        # if len(self.devices) > 10:

    def widgetSizes(self,MainWindow):
        if len(self.devices) > self.nMinRowsForDecrSize:
            horSizeBlock = 481
            if len(self.devices) > self.nMaxRows:
                vertWinSize = 50 + len(self.devices)*50/2
            else:
                vertWinSize = 50 + len(self.devices)*50
            horWinSize = horSizeBlock + (len(self.devices)//11)*horSizeBlock
            MainWindow.setFixedSize(horWinSize,vertWinSize)
        else:
            horWinSize = 800
            vertWinSize = 80 + len(self.devices)*80
            for i in range(0,len(self.devices)):
                self.measLCD[i].setFixedHeight(70)
                self.voltageValueSpinBox[i].setFixedHeight(70)
                self.statusLed[i].setFixedSize(40,40)
                font = self.voltageValueSpinBox[i].font()
                font.setPointSize(20)
                self.voltageValueSpinBox[i].setFont(font)

                labelFont = self.deviceNameLabel[i].font()
                labelFont.setPointSize(10)
                self.deviceNameLabel[i].setFont(labelFont)
                # self.voltageValueSpinBox[i].setPointSize(48)
            MainWindow.setFixedSize(horWinSize,vertWinSize)

    def layouts(self,MainWindow):
        if len(self.devices) < self.nMaxRows + 1:
            mainLayout = QtGui.QVBoxLayout()
        if len(self.devices) > self.nMaxRows:
            mainLayout = QtGui.QGridLayout()
        # testLayout = QtGui.QHBoxLayout() # ???

        htopLayout=list()

        for i in range(0,len(self.devices)):
            htopLayout.append(QtGui.QHBoxLayout())
            htopLayout[i].addWidget(self.statusLed[i])
            htopLayout[i].addWidget(self.deviceNameLabel[i])
            # htopLayout[i].addStretch(1)
            htopLayout[i].addWidget(self.measLCD[i])
            # htopLayout[i].addWidget(self.voltageLabel[i])
            htopLayout[i].addWidget(self.voltageValueSpinBox[i])
            htopLayout[i].addWidget(self.setVoltageButton[i])
            # htopLayout[i].addStretch(1)


        hbottomLayout = QtGui.QHBoxLayout()
        hbottomLayout.addStretch(1)
        hbottomLayout.addWidget(self.settingsButton )
        hbottomLayout.addWidget(self.reconnectButton)

        j = k = 0
        for i in range(0,len(self.devices)):
            if len(self.devices) < self.nMaxRows + 1:
                mainLayout.addLayout(htopLayout[i])
            if len(self.devices) > self.nMaxRows:
                mainLayout.addLayout(htopLayout[i],j,k)
                k = k + 1
                if k >= 2:
                    j = j + 1
                    k = 0

        if (k != 0):
            j = j + 1

        if len(self.devices) < self.nMaxRows + 1:
            mainLayout.addLayout(hbottomLayout)
        if len(self.devices) > self.nMaxRows:
            mainLayout.addLayout(hbottomLayout,j,0,1,2)

        centralWidget = MainWindow.centralWidget()
        centralWidget.setLayout(mainLayout)

    def setWidgetView(self,i):
        self.statusLed.append(TaurusLed(self))
        self.statusLed[i].setModel(str(self.devices[i]) + "/State")
        # df = QtGui.QLCDNumber
        # df.setFixedHeight()

        self.statusLed[i].setAutoTooltip(False) # ??? Всплывающая подсказка

        self.voltageValueSpinBox.append(QtGui.QSpinBox())
        self.voltageValueSpinBox[i].setMinimum(0)
        self.voltageValueSpinBox[i].setMaximum(500)
        self.voltageValueSpinBox[i].setValue(0)

        self.setVoltageButton.append(QtGui.QPushButton())
        self.setVoltageButton[i].setText("set Voltage")

        self.measLCD.append(TaurusLCD())
        self.measLCD[i].setEnabled(True)
        self.measLCD[i].setDigitCount(3)
        palette = self.measLCD[i].palette()
        palette.setColor(palette.WindowText, QtGui.QColor("green"))
        palette.setColor(palette.Background, QtGui.QColor("black"))
        self.measLCD[i].setPalette(palette)

        self.voltageLabel.append(TaurusLabel())

        self.deviceNameLabel.append(QtGui.QLabel())
        textLabel = "<font color = red> <b>"
        textLabel += QtCore.QString(self.devices[i])
        textLabel += "<\b><\font>"

        self.deviceNameLabel[i].setText(textLabel)
        self.deviceNameLabel[i].setFixedWidth(200)
        self.deviceNameLabel[i].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


    def centerOnScreen (self,MainWindow):
        resolution = QtGui.QDesktopWidget().screenGeometry()
        MainWindow.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

        # for i in range(0,len(self.devices)):
        #     self.statusLed[i].setLedColor(_translate("MainWindow", "green", None))
            # self.measLCD[i].setText(_translate("MainWindow", " 99.99", None))

        self.reconnectButton.setText(_translate("MainWindow", "Reconnect", None))
        self.settingsButton.setText(_translate("MainWindow","Settings",None))

    def runDevice(self):
        print "Number of active devices: " + str(len(self.devices))
        self.checkStatus(self.devices[0])

    # def initDevices(self):


    def printMessageToOutputEdit(self, message):
        dateTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        self.outputEdit.append("<b>" + dateTime + "</b>")
        excMes = "Exception message: " + message
        self.outputEdit.append(excMes)



    # def showDialog(self):
    # #def showDialog(self,MainWindow):
    #     dial = SettingsDialog(self)
    #     if (len(self.devices)!=0):
    #         dial.setDefaultValue(self.devices[0])
    #     dial.show()
    #
    #     if dial.exec_():
    #         text = dial.getValue()
    #         self.devices.append(str(text))
    #         # MainWindow.setWindowTitle(_translate(text, text, None))
    #         self.addDeviceToCfgFile(text)