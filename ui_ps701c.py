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

        if (len(self.devices)<1):
            print "Devices < than 1"
            self.showDialog()

        self.deviceNameLabel = list()
        self.statusLed = list()
        self.voltageValueSpinBox = list()
        self.setVoltageButton = list()
        self.measLabel = list()
        self.voltageLabel = list()

        for i in range(0,len(self.devices)):
            self.statusLed.append(TaurusLed(self))
            self.statusLed[i].setModel(str(self.devices[i]) + "/State")
            # df = TaurusLed()
            # df.too
            self.statusLed[i].setAutoTooltip(False) # ??? Всплывающая подсказка

            self.voltageValueSpinBox.append(QtGui.QSpinBox())
            self.voltageValueSpinBox[i].setMinimum(0)
            self.voltageValueSpinBox[i].setMaximum(500)
            self.voltageValueSpinBox[i].setValue(0)

            self.setVoltageButton.append(QtGui.QPushButton())
            self.setVoltageButton[i].setText("set Voltage")

            self.measLabel.append(TaurusLCD())
            self.measLabel[i].setEnabled(True)
            self.measLabel[i].setDigitCount(3)
            palette = self.measLabel[i].palette()
            palette.setColor(palette.WindowText, QtGui.QColor("blue"))
            self.measLabel[i].setPalette(palette)

            self.voltageLabel.append(TaurusLabel())

            self.deviceNameLabel.append(QtGui.QLabel())
            textLabel = "<font color = red> <b>"
            textLabel += QtCore.QString(self.devices[i])
            textLabel += "<\b><\font>"

            self.deviceNameLabel[i].setText(textLabel)
            self.deviceNameLabel[i].setFixedWidth(200)
            self.deviceNameLabel[i].setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


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
        self.initDevices()

        vertWinSize = 50 + len(self.devices)*50
        MainWindow.setFixedSize(481,vertWinSize)


    def layouts(self,MainWindow):
        mainLayout = QtGui.QVBoxLayout()
        # testLayout = QtGui.QHBoxLayout() # ???

        htopLayout=list()

        for i in range(0,len(self.devices)):
            htopLayout.append(QtGui.QHBoxLayout())
            htopLayout[i].addWidget(self.deviceNameLabel[i])
            # htopLayout[i].addStretch(1)
            htopLayout[i].addWidget(self.measLabel[i])
            htopLayout[i].addWidget(self.voltageLabel[i])
            htopLayout[i].addWidget(self.voltageValueSpinBox[i])
            htopLayout[i].addWidget(self.setVoltageButton[i])
            htopLayout[i].addStretch(1)
            htopLayout[i].addWidget(self.statusLed[i])

        hbottomLayout = QtGui.QHBoxLayout()
        hbottomLayout.addStretch(1)
        hbottomLayout.addWidget(self.settingsButton )
        hbottomLayout.addWidget(self.reconnectButton)

        for i in range(0,len(self.devices)):
            mainLayout.addLayout(htopLayout[i])

        mainLayout.addLayout(hbottomLayout)

        centralWidget = MainWindow.centralWidget()
        centralWidget.setLayout(mainLayout)

    def centerOnScreen (self,MainWindow):
        resolution = QtGui.QDesktopWidget().screenGeometry()
        MainWindow.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

        # for i in range(0,len(self.devices)):
        #     self.statusLed[i].setLedColor(_translate("MainWindow", "green", None))
            # self.measLabel[i].setText(_translate("MainWindow", " 99.99", None))

        self.reconnectButton.setText(_translate("MainWindow", "Reconnect", None))
        self.settingsButton.setText(_translate("MainWindow","Settings",None))

    def runDevice(self):
        print "Number of active devices: " + str(len(self.devices))
        self.checkStatus(self.devices[0])

    def initDevices(self):
        if len(self.devices) < 1:
            print("Devices less than 1")
            return
        print "Number of devices: " + str(len(self.devices))

        for i in range(0,len(self.devices)):
            try:
                print("Device: -> " + self.devices[i])
                deviceTan = PyTango.DeviceProxy(self.devices[i])
                if deviceTan.state() == PyTango.DevState.OFF:
                    # self.statusLed[i].setLedColor("white")
                    self.voltageValueSpinBox[i].setEnabled(False)
                    self.setVoltageButton[i].setEnabled(False)
                    self.statusLed[i].setToolTip("TESTOFF") # ??? test
                    print("TESTOFF")
                elif deviceTan.state() == PyTango.DevState.FAULT:
                    # self.statusLed[i].setLedColor("red")
                    self.voltageValueSpinBox[i].setEnabled(False)
                    self.setVoltageButton[i].setEnabled(False)
                    self.statusLed[i].setToolTip("TESTFAULT") # ??? test
                    print self.statusLed[i].getFormatedToolTip(True)
                    print("TESTFAULT")
                elif deviceTan.state() == PyTango.DevState.ON:
                    # self.statusLed[i].setLedColor("green")
                    self.voltageValueSpinBox[i].setEnabled(True)
                    self.setVoltageButton[i].setEnabled(True)
                    self.statusLed[i].setToolTip("TESTON") # ??? test
                    print("TESTON")
                self.tangoDevices.append(deviceTan)
            except PyTango.DevFailed as exc:
                self.statusLed[i].setLedColor("red")
                self.statusLed[i].setToolTip(str(exc)) # ??? test
                self.voltageValueSpinBox[i].setEnabled(False)
                self.setVoltageButton[i].setEnabled(False)



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