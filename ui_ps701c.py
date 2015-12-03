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

# from datetime import datetime
# import os.path
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
# from taurus.qt.qtgui.input import TaurusWheelEdit
from taurus.qt.qtgui.button import TaurusCommandButton
from taurus.qt.qtgui.display import TaurusLCD
# from taurus.qt.qtgui.input import TaurusValueSpinBox

MDEBUG = True
timerval = 10000

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

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.reconnectButton = TaurusCommandButton(self.centralwidget)
        self.reconnectButton.setObjectName(_fromUtf8("reconnectButton"))
        self.reconnectButton.clicked.connect(self.reconnectCommand)


        self.settingsButton = QtGui.QPushButton(self.centralwidget)
        # self.settingsButton.setObjectName(_fromUtf8("settingsButton"))
        self.settingsButton.clicked.connect(self.showSettDialog)

        # timer init
        for i in range(0,len(self.devices)):
            self.timer.append(MyTimer()) # установка таймера для проверки актуального заряда конденсаторов
            self.timer[i].iter = i
            self.setWidgetView(i) # установка параметров виджетов
            self.setSignalHandler(i) # установка обработчиков
        # clicked connect
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.layouts(MainWindow)  # установка компоновки

        self.centerOnScreen(MainWindow)
        self.initTangoDevices() # tango devices
        if MDEBUG:
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
        self.statusLed.append(MyTaurusLed(self))
        self.statusLed[i].iter = i
        self.statusLed[i].setModel(str(self.devices[i]) + "/State")
        self.statusLed[i].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # self.statusLed[i].setAutoTooltip(False) # ??? Всплывающая подсказка

        self.voltageValueSpinBox.append(QtGui.QSpinBox())
        self.voltageValueSpinBox[i].setMinimum(50)
        self.voltageValueSpinBox[i].setMaximum(500)
        self.voltageValueSpinBox[i].setValue(50)

        self.setVoltageButton.append(MyQPushButton())
        self.setVoltageButton[i].setText("set Voltage")
        self.setVoltageButton[i].iter = i

        self.measLCD.append(TaurusLCD())
        self.measLCD[i].setEnabled(True)
        self.measLCD[i].setDigitCount(3)
        # self.measLCD[i].setBgRole('state')
        # self.measLCD[i].setFgRole('state')
        palette = self.measLCD[i].palette()
        palette.setColor(palette.WindowText, QtGui.QColor("green"))
        # palette.setColor(palette.Background, QtGui.QColor("black"))
        palette.setColor(palette.Light, QtGui.QColor("orange"))
        palette.setColor(palette.Dark, QtGui.QColor("magenta"))
        self.measLCD[i].setPalette(palette)
        self.measLCD[i].setSegmentStyle(TaurusLCD.Flat)

        self.deviceNameLabel.append(QtGui.QLabel())
        textLabel = "<font color = black>"
        textLabel += QtCore.QString(self.devices[i])
        textLabel += "<\font>"

        self.deviceNameLabel[i].setText(textLabel)
        self.deviceNameLabel[i].setFixedWidth(200)
        # self.deviceNameLabel[i].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.checkActiveBox.append(MyQCheckBox())
        self.checkActiveBox[i].setText("Charging")
        self.checkActiveBox[i].iter = i
        self.checkActiveBox[i].setChecked(False)

    def setSignalHandler(self,i):
        # self.reconnectButton.clicked.connect(self.reconnectCommand)
        self.connect(self.setVoltageButton[i],QtCore.SIGNAL("clicked(int)"),self.setVoltageAttr)
        self.connect(self.checkActiveBox[i], QtCore.SIGNAL("stateChanged(int,int)"),self.chargingOnOffCommand)
        self.connect(self.timer[i],QtCore.SIGNAL("timeout(int)"),self.checkADCoutput)
        self.connect(self.statusLed[i],QtCore.SIGNAL("clicked(int)"),self.statusLedInfo)

    def statusLedInfo(self,i):
        if MDEBUG:
            print("StatusLedInfo: " + str(i))
        cd = deviceInfoDialog(self.tangoDevices[i],self)
        cd.show()

    def checkADCoutput(self,i):
        if MDEBUG:
            print("check ADC")
        result = self.tangoDevices[i].command_inout("CheckAdcOutput")
        if (result != -1):
            self.measLCD[i].setProperty("intValue", result)
        else:
            self.setEnabledVoltageEdit(i,False)
            if (self.checkActiveBox[i].isChecked()):
                self.checkActiveBox[i].setChecked(False)
            self.timer[i].stop()

    def chargingOnOffCommand(self,i,state):
        if MDEBUG:
            print("ChargingOnOff : " + str(i) + " " + str(state))
        if (self.checkActiveBox[i].isChecked()):
            self.checkActiveBox[i].setChecked(False)
            self.tangoDevices[i].command_inout("ChargingOff")
            if self.timer[i].isActive() == True:
                self.timer[i].stop()
            if MDEBUG:
                print("charging off")
        else:
            self.checkActiveBox[i].setChecked(True)
            self.tangoDevices[i].command_inout("ChargingOn")
            if self.timer[i].isActive() == False:
                self.timer[i].start(timerval)
            if MDEBUG:
                print("charging on")


    def setVoltageAttr(self,i):
        voltage = self.voltageValueSpinBox[i].value()
        self.tangoDevices[i].write_attribute("Voltage", voltage)
        if (self.checkActiveBox[i].isChecked() == False):
            self.checkActiveBox[i].setChecked(True)
            self.tangoDevices[i].command_inout("ChargingOn")
        if self.timer[i].isActive() == False:
            self.timer[i].start(timerval)
        if MDEBUG:
            print("voltage charging on")
            print(voltage)

    def reconnectCommand(self):
        for i in range(0,len(self.tangoDevices)):
            if self.tangoDevices[i] != False and self.tangoDevices[i].state()!= PyTango.DevState.ON:
                self.tangoDevices[i].command_inout("Init")
                self.checkStatus(self.tangoDevices[i],i)
                if MDEBUG:
                    print("reInit")

    def initTangoDevices(self):
        if len(self.devices) < 1:
            print("Devices less than 1")
            return
        # print "Number of devices: " + str(len(self.devices)) # for debug
    
        for i in range(0,len(self.devices)):
            try:
                # print("Device: -> " + self.devices[i])
                deviceTan = PyTango.DeviceProxy(self.devices[i])
                self.checkStatus(deviceTan,i)
                self.tangoDevices.append(deviceTan)
            except PyTango.DevFailed as exc:
                self.statusLed[i].setLedColor("red")
                self.statusLed[i].setToolTip(str(exc)) # ??? test
                # self.voltageValueSpinBox[i].setEnabled(False)
                # self.setVoltageButton[i].setEnabled(False)
                self.setEnabledVoltageEdit(i,False)
                self.tangoDevices.append(False)
                
    def checkStatus(self,deviceTan,i):
        if deviceTan.state() == PyTango.DevState.OFF:
            if MDEBUG:
                self.setEnabledVoltageEdit(i,True) # ??? test
                self.statusLed[i].setToolTip("TESTOFF") # ??? test
                print("TESTOFF is True now")
            else:
                self.setEnabledVoltageEdit(i,False)
        elif deviceTan.state() == PyTango.DevState.FAULT:
            if MDEBUG:
                self.setEnabledVoltageEdit(i,True)
                self.statusLed[i].setToolTip("TESTFAULT") # ??? test
                print("TESTFAULT is True now")
            else:
                self.setEnabledVoltageEdit(i,False)
        elif deviceTan.state() == PyTango.DevState.ON:
            if MDEBUG:
                self.statusLed[i].setToolTip("TESTON") # ??? test
                print("TESTON")
            else:
                self.setEnabledVoltageEdit(i,True)
        elif deviceTan.state() == PyTango.DevState.DISABLE:
            self.setEnabledVoltageEdit(i,False)
            if MDEBUG:
                self.statusLed[i].setToolTip("TESTDISABLE") # ??? test
                print("TESTDISABLE")
        elif deviceTan.state() == PyTango.DevState.RUNNING:
            self.setEnabledVoltageEdit(i,True)
            if MDEBUG:
                self.statusLed[i].setToolTip("TESTRUNNING") # ??? test
                print("TESTRUNNING")

    def showSettDialog(self):
        dial = SettingsDialog(self)
        dial.show()
        if dial.exec_():
            ntime = dial.getValue()
            timerval = ntime
            for i in range(0,len(self.tangoDevices)):
                if self.tangoDevices[i] != False:
                    if (self.tangoDevices[i].state() == PyTango.DevState.ON
                        or self.tangoDevices[i].state() == PyTango.DevState.RUNNING):
                        if self.timer[i].isActive() == True:
                            self.timer[i].stop()
                            self.timer[i].start(ntime*1000)
                        else:
                            self.timer[i].start(ntime*1000)
            if MDEBUG:
                print("EXEC DIAL" + str(ntime))
        else:
            if MDEBUG:
                print("ELSE DIAL")

    def setEnabledVoltageEdit(self,iter,isEnabled):
        self.voltageValueSpinBox[iter].setEnabled(isEnabled)
        self.setVoltageButton[iter].setEnabled(isEnabled)
        self.checkActiveBox[iter].setEnabled(isEnabled)

    def centerOnScreen(self,MainWindow):
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


class MyTaurusLed(TaurusLed):
    def __init(self, parent):
        TaurusLed.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked(int)'),self.iter)

class deviceInfoDialog(QtGui.QDialog):
    def __init__(self,device, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(400, 200)
        self.buttonOk = QtGui.QPushButton('Ok', self)
        vertLayout = QtGui.QVBoxLayout(self)
        self.state = QtGui.QLineEdit()
        self.status = QtGui.QTextEdit()

        self.state.setReadOnly(True)
        self.status.setReadOnly(True)

        if device != False:
            state = device.command_inout("State")
            status = device.command_inout("Status")

            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)

            self.status.setFont(font)
            self.state.setFont(font)

            self.state.setText(str(state))
            self.status.setText(str(status))

        vertLayout.addWidget(self.state)
        vertLayout.addWidget(self.status)
        buttonLayout = QtGui.QHBoxLayout(self)
        buttonLayout.addStretch(0)
        buttonLayout.addWidget(self.buttonOk)
        vertLayout.addLayout(buttonLayout)

        self.setLayout(vertLayout)

        self.buttonOk.clicked.connect(self.accept)

class MyQPushButton(QtGui.QPushButton):
    def __init(self, parent):
        QtGui.QPushButton.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked(int)'),self.iter)

class MyQCheckBox(QtGui.QCheckBox):
    def __init(self, parent):
        QtGui.QCheckBox.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked(int)'),self.iter)
        self.emit(QtCore.SIGNAL('stateChanged(int,int)'),self.iter,self.checkState())

class MyTimer(QtCore.QTimer):
    def __init(self, parent):
        QtGui.QTimer.__init__(self, parent)

    def timerEvent(self, event):
        self.emit(QtCore.SIGNAL('timeout(int)'),self.iter)

class SettingsDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        vertLayout = QtGui.QVBoxLayout(self)
        layout1 = QtGui.QHBoxLayout()

        self.setFixedSize(300, 150)
        self.timerSpinBox = QtGui.QSpinBox()
        self.timerSpinBox.setMinimum(1)
        self.timerSpinBox.setMaximum(60)
        self.timerSpinBox.setValue(10)
        self.setModal(True)

        self.label = QtGui.QLabel()
        self.label.setText("timer in sec")

        layout1.addWidget(self.label)
        layout1.addWidget(self.timerSpinBox)

        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal
        )

        vertLayout.addLayout(layout1)
        vertLayout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def getValue(self):
        return self.timerSpinBox.value()