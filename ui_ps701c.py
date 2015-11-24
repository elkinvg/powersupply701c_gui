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
import os.path
#from taurus.qt.qtgui.button import TaurusCommandButton

#devName = "sock/pssocket/1"
fileCfg = "devsockets.cfg"

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
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setFixedSize(481, 250) #elkin

        self.devices = list() # list of names of devices
        self.tangoDevices = list() # list of tango-devices
        #self.devicesState = list() # list of statuses of devices

        self.checkCfgFile()

        if (len(self.devices)<1):
            print "Devices < than 1"
            self.showDialog()
        else:
            self.statusLed = list()
            self.voltageWheelEdit = list()
            self.measLabel = list()
            self.voltageLabel = list()

            for i in range(0,len(self.devices)):
                self.statusLed.append(TaurusLed())

                self.voltageWheelEdit.append(TaurusWheelEdit())
                self.voltageWheelEdit[i].setProperty("integerDigits", 3)
                self.voltageWheelEdit[i].setProperty("decimalDigits", 0)
                self.voltageWheelEdit[i].setMinValue(0.0)
                self.voltageWheelEdit[i].setMaxValue(500.0)

                self.measLabel.append(TaurusLabel())
                self.measLabel[i].setEnabled(True)
                self.measLabel[i].setTextFormat(QtCore.Qt.AutoText)

                self.voltageLabel.append(TaurusLabel())


        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))


        self.outputEdit = QtGui.QTextEdit()
        self.outputEdit.setGeometry(QtCore.QRect(30, 80, 411, 81))
        self.outputEdit.setObjectName(_fromUtf8("outputEdit"))
        self.outputEdit.setReadOnly(True)

        self.reconnectButton = TaurusCommandButton(self.centralwidget)
        self.reconnectButton.setObjectName(_fromUtf8("reconnectButton"))

        self.settingsButton = QtGui.QPushButton(self.centralwidget)
        self.settingsButton.setObjectName(_fromUtf8("settingsButton"))

        #clicked connect
        self.settingsButton.clicked.connect(self.showDialog)



        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #elkin
        mainLayout = QtGui.QVBoxLayout()

        htopLayout=list()

        for i in range(0,len(self.devices)):
            htopLayout.append(QtGui.QHBoxLayout())
            htopLayout[i].addWidget(self.measLabel[i])
            htopLayout[i].addWidget(self.voltageLabel[i])
            htopLayout[i].addWidget(self.voltageWheelEdit[i])
            htopLayout[i].addStretch(1)
            htopLayout[i].addWidget(self.statusLed[i])

        hbottomLayout = QtGui.QHBoxLayout()
        hbottomLayout.addStretch(1)
        hbottomLayout.addWidget(self.settingsButton )
        hbottomLayout.addWidget(self.reconnectButton)

        for i in range(0,len(self.devices)):
            mainLayout.addLayout(htopLayout[i])

        #mainLayout.addLayout(htopLayout)
        mainLayout.addWidget(self.outputEdit)
        mainLayout.addLayout(hbottomLayout)

        centralWidget = MainWindow.centralWidget()
        centralWidget.setLayout(mainLayout)

        self.initDevices()

        #self.checkCfgFile()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))

        for i in range(0,len(self.devices)):
            self.statusLed[i].setLedColor(_translate("MainWindow", "green", None))
            self.measLabel[i].setText(_translate("MainWindow", " 99.99", None))

        self.reconnectButton.setText(_translate("MainWindow", "Reconnect", None))
        self.settingsButton.setText(_translate("MainWindow","Settings",None))

    def runDevice(self):
        print "Number of active devices: " + str(len(self.devices))
        self.checkStatus(self.devices[0])

    def checkCfgFile(self):
        #isCorrect = True
        if os.path.exists(fileCfg):
            try:
                file = open(fileCfg,"r")
                lines = file.readlines()
                file.close()
                print "Lines: " + str(len(lines)) # ??? debug
                if len(lines) > 0:
                    for line in lines:
                        lineDevName = line # ??? debug if lenth >1
                        splitLine = lineDevName.split("=")
                        if len(splitLine) >3: # ???
                            #isCorrect = False
                            continue
                            #self.printMessageToOutputEdit("Incorrect format of configfile")

                        else:
                            if (splitLine[0]=="[sock]"):
                                self.devices.append(splitLine[1])
                                # print "dev_: "


                    #if(isCorrect==False):
                    if(len(self.devices)==0):
                        self.showDialog()
                        return

                    print self.devices[0]
                    #self.initDevices()
                            #self.runDevice()
                else:
                    self.showDialog()

            except IOError as e:
                self.printMessageToOutputEdit(str(e))
        else:
            self.showDialog()

    def initDevices(self):
        if len(self.devices) < 1:
            return
        print "Number of devices: " + str(len(self.devices))

        for i in range(0,len(self.devices)):
            try:
                print("Device: -> " + self.devices[i])
                deviceTan = PyTango.DeviceProxy(self.devices[i])
                if deviceTan.state() == PyTango.DevState.OFF:
                    #mes = self.devices[0] + " is OFF"
                    mes = deviceTan.status()
                    self.printMessageToOutputEdit(mes)
                    self.statusLed[i].setLedColor("white")
                    self.voltageWheelEdit[i].setEnabled(False)
                elif deviceTan.state() == PyTango.DevState.FAULT:
                    mes = deviceTan.status()
                    self.printMessageToOutputEdit(mes)
                    self.statusLed[i].setLedColor("red")
                    self.voltageWheelEdit[i].setEnabled(False)
                elif deviceTan.state() == PyTango.DevState.ON:
                    # mes = self.devices[0] + " is ON"
                    mes = deviceTan.status()
                    self.printMessageToOutputEdit(mes)
                    self.statusLed[i].setLedColor("green")
                    self.voltageWheelEdit[i].setEnabled(True)
                self.tangoDevices.append(deviceTan)
            except PyTango.DevFailed as exc: #??? вылетает даже если только один из девайсов глючит
                # for i in range(0,len(self.devices)):
                self.statusLed[i].setLedColor("red")
                self.voltageWheelEdit[i].setEnabled(False)
                self.printMessageToOutputEdit(str(exc))


    # def checkStatus(self, devName):
    #     try:
    #         device = PyTango.DeviceProxy(str(devName)) # ??????? Debug. Get name of proxy from settings
    #         # device = PyTango.DeviceProxy("sock/pssocketaa/1")
    #
    #         # self.devicesState[0] = device.state()
    #         mes2 = device.status()
    #         #print "State: " + mes
    #         print "Status: " + mes2
    #         self.tangoDevices.append(device)
    #     except PyTango.DevFailed as exc:
    #         self.printMessageToOutputEdit(str(exc))

    def addDeviceToCfgFile(self,devName): # ??? for many devices
        with open(fileCfg,"w") as fileWrite:
                fileWrite.write(str("[sock]=" +devName+"="))


    def printMessageToOutputEdit(self, message):
        dateTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        self.outputEdit.append("<b>" + dateTime + "</b>")
        excMes = "Exception message: " + message
        self.outputEdit.append(excMes)



    def showDialog(self):
        dial = SettingsDialog(self)
        if (len(self.devices)!=0):
            dial.setDefaultValue(self.devices[0])
        dial.show()

        if dial.exec_():
            text = dial.getValue()
            MainWindow.setWindowTitle(_translate(text, text, None))
            self.addDeviceToCfgFile(text)
            self.initDevices()
        else:
            print "ELSE"

from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from taurus.qt.qtgui.input import TaurusWheelEdit
from taurus.qt.qtgui.button import TaurusCommandButton

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

