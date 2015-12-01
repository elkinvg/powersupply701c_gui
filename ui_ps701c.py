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

from dialogParameter import SettingsDialog
# from datetime import datetime
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
        self.checkActiveBox = list()

        self.timer = list() # список таймеров
        # self.voltageLabel = list()

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.reconnectButton = TaurusCommandButton(self.centralwidget)
        self.reconnectButton.setObjectName(_fromUtf8("reconnectButton"))

        self.settingsButton = QtGui.QPushButton(self.centralwidget)
        self.settingsButton.setObjectName(_fromUtf8("settingsButton"))

        self.reconnectButton.clicked.connect(self.reconnectCommand)

        for i in range(0,len(self.devices)):
            self.timer.append(common_func.MyTimer()) # установка таймера для проверки актуального заряда конденсаторов
            self.timer[i].iter = i
            self.setWidgetView(i) # установка параметров виджетов
            self.setSignalHandler(i) # установка обработчиков
        # clicked connect
        # self.settingsButton.clicked.connect(self.tempConsoleOut)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.layouts(MainWindow)  # установка компоновки

        # self.centerOnScreen()
        self.centerOnScreen(MainWindow)
        common_func.initTangoDevices(self)
        print("Number of TanDev: " + str(self.tangoDevices))

        self.widgetSizes(MainWindow) # установка размеров виджетов

    def widgetSizes(self,MainWindow):
        if len(self.devices) > self.nMinRowsForDecrSize:
            horSizeBlock = 600
            if len(self.devices) > self.nMaxRows:
                vertWinSize = 50 + len(self.devices)*50/2
            else:
                vertWinSize = 50 + len(self.devices)*50
            horWinSize = horSizeBlock + (len(self.devices)//11)*horSizeBlock
            MainWindow.setFixedSize(horWinSize,vertWinSize)
            for i in range(0,len(self.devices)):
                self.checkActiveBox[i].setFixedWidth(120)
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
                self.checkActiveBox[i].setFixedHeight(50)
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
            htopLayout[i].addWidget(self.checkActiveBox[i])
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
        self.voltageValueSpinBox[i].setMinimum(50)
        self.voltageValueSpinBox[i].setMaximum(500)
        self.voltageValueSpinBox[i].setValue(50)

        # self.setVoltageButton.append(QtGui.QPushButton())
        self.setVoltageButton.append(common_func.MyQPushButton())
        self.setVoltageButton[i].setText("set Voltage")
        self.setVoltageButton[i].iter = i

        self.measLCD.append(TaurusLCD())
        self.measLCD[i].setEnabled(True)
        self.measLCD[i].setDigitCount(3)
        # self.measLCD[i].setBgRole('state')
        # self.measLCD[i].setFgRole('state')
        palette = self.measLCD[i].palette()
        # sd = TaurusLCD()
        # sd.set

        palette.setColor(palette.WindowText, QtGui.QColor("green"))
        # palette.setColor(palette.Background, QtGui.QColor("black"))
        palette.setColor(palette.Light, QtGui.QColor("orange"))
        palette.setColor(palette.Dark, QtGui.QColor("magenta"))
        self.measLCD[i].setPalette(palette)
        self.measLCD[i].setSegmentStyle(TaurusLCD.Flat)

        # self.voltageLabel.append(TaurusLabel())

        self.deviceNameLabel.append(QtGui.QLabel())
        textLabel = "<font color = black>"
        textLabel += QtCore.QString(self.devices[i])
        textLabel += "<\font>"

        self.deviceNameLabel[i].setText(textLabel)
        self.deviceNameLabel[i].setFixedWidth(200)
        self.deviceNameLabel[i].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # self.radioButton.append(QtGui.QRadioButton())
        # self.radioButton.append(QtGui.QCommandLinkButton())
        self.checkActiveBox.append(common_func.MyQCheckBox())
        self.checkActiveBox[i].setText("Charging")
        self.checkActiveBox[i].iter = i
        self.checkActiveBox[i].setChecked(False)

    def setSignalHandler(self,i):
        self.connect(self.setVoltageButton[i],QtCore.SIGNAL("clicked(int)"),self.setVoltageAttr)
        self.connect(self.checkActiveBox[i], QtCore.SIGNAL("stateChanged(int,int)"),self.chargingOnOffCommand)
        self.connect(self.timer[i],QtCore.SIGNAL("timeout(int)"),self.checkADCoutput)
        # for i in range(0,len(self.tangoDevices)):
        #     if self.tangoDevices[i] != False:
        #         self.connect(self.measLCD[i],QtCore.SIGNAL()

        # print("Hanler")

    def checkADCoutput(self,i):
        print("check ADC")
        result = self.tangoDevices[i].command_inout("CheckAdcOutput")
        if (result != -1):
            self.measLCD[i].setProperty("intValue", result)
        else:
            common_func.setEnabledVoltageEdit(self,i,False)
            if (self.checkActiveBox[i].isChecked()):
                self.checkActiveBox[i].setChecked(False)
            self.timer[i].stop()

    def chargingOnOffCommand(self,i,state):
        print("ChargingOnOff : " + str(i) + " " + str(state))
        if (self.checkActiveBox[i].isChecked()):
            self.checkActiveBox[i].setChecked(False)
            self.tangoDevices[i].command_inout("ChargingOff")
            if self.timer[i].isActive() == True:
                self.timer[i].stop()
            print("charging off")
        else:
            self.checkActiveBox[i].setChecked(True)
            self.tangoDevices[i].command_inout("ChargingOn")
            if self.timer[i].isActive() == False:
                self.timer[i].start(10000)
            print("charging on")


    def setVoltageAttr(self,i):
        voltage = self.voltageValueSpinBox[i].value()
        self.tangoDevices[i].write_attribute("Voltage", voltage)
        if (self.checkActiveBox[i].isChecked() == False):
            self.checkActiveBox[i].setChecked(True)
            self.tangoDevices[i].command_inout("ChargingOn")
        if self.timer[i].isActive() == False:
            self.timer[i].start(10000)
        print("voltage charging on")
        print(voltage)

    def reconnectCommand(self):
        for i in range(0,len(self.tangoDevices)):
            if self.tangoDevices[i] != False and self.tangoDevices[i].state()!= PyTango.DevState.ON:
                self.tangoDevices[i].command_inout("Init")
                common_func.checkStatus(self,self.tangoDevices[i],i)
                print("reInit")


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



    def tempConsoleOut(self,i):
        # val = self.voltageValueSpinBox[i].value()
        # print i
        print "sds" + str(i)
        # print(val)

