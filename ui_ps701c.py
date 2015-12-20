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
import time

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
        self.timerVal = timerval # timer interval

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
                self.statusLed[i].setFixedSize(30,30)
        else:
            horWinSize = 900
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
                self.voltageValueSpinBox[i].setFixedWidth(150)
            if len(self.devices) > self.nMaxRows:
                mainLayout.addLayout(htopLayout[i],j,k)
                self.voltageValueSpinBox[i].setFixedWidth(70)
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
        try:
            result = self.tangoDevices[i].command_inout("CheckAdcOutput")
            if (result != 65535):
                self.measLCD[i].setProperty("intValue", result)
                if MDEBUG:
                    print("Result: " + str(result))
                if (self.tangoDevices[i].state()!= PyTango.DevState.RUNNING): #??? Выключение checkActiveBox
                    if (self.checkActiveBox[i].isChecked()):                  #??? если активный, при полной зарадке
                        self.checkActiveBox[i].setChecked(False)              #??? конденсатора
                        self.timer[i].stop()
                        if MDEBUG:
                            print("charging OFF. Completed")
            else:
                self.setEnabledVoltageEdit(i,False)
                if (self.checkActiveBox[i].isChecked()):
                    self.checkActiveBox[i].setChecked(False)
                self.timer[i].stop()
                if MDEBUG:
                    print("timer STOP")
        except PyTango.DevFailed as exc:
            self.exceptionDialog(i,exc)

    def chargingOnOffCommand(self,i,state):
        if MDEBUG:
            print("ChargingOnOff : " + str(i) + " " + str(state))
        try:
            if (self.checkActiveBox[i].isChecked()):
                self.tangoDevices[i].command_inout("ChargingOff")
                self.checkActiveBox[i].setChecked(False)
                if self.timer[i].isActive() == True:
                    self.timer[i].stop()
                if MDEBUG:
                    print("charging off")
            else:
                self.tangoDevices[i].command_inout("ChargingOn")
                self.checkActiveBox[i].setChecked(True)
                if self.timer[i].isActive() == False:
                    self.timer[i].setInterval(self.timerVal)
                    self.timer[i].start(0)
                if MDEBUG:
                    print("charging on")
        except PyTango.DevFailed as exc:
            self.exceptionDialog(i,exc)

    def setVoltageAttr(self,i):
        try:
            voltage = self.voltageValueSpinBox[i].value()
            self.tangoDevices[i].write_attribute("Voltage", voltage)
            if (self.checkActiveBox[i].isChecked() == False):
                self.tangoDevices[i].command_inout("ChargingOn")
                self.checkActiveBox[i].setChecked(True)
            if self.timer[i].isActive() == False:
                self.timer[i].setInterval(self.timerVal)
                self.timer[i].start(0)
            if(self.setVoltageButton[i].isDown()==True):
                if MDEBUG:
                    print("isDown")
                self.setVoltageButton[i].setDown(False)
            if MDEBUG:
                print("voltage charging on")
        except PyTango.DevFailed as exc:
            self.exceptionDialog(i,exc)

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
                if MDEBUG:
                    print("initTangoDevices: " + str(self.devices[i]))
                deviceTan = PyTango.DeviceProxy(self.devices[i])
                self.checkStatus(deviceTan,i)
                self.tangoDevices.append(deviceTan)
                if MDEBUG:
                    print("Registered devices: " + str(deviceTan))


                volt = deviceTan.get_attribute_config("Voltage")
                # volt = deviceTan.get_attribute_list()
                # volt = deviceTan.read_attribute("Voltage")
                # volt = deviceTan.attribute_list_query()
                # volt = deviceTan.state()

                self.voltageValueSpinBox[i].setMaximum(int(volt.max_value))
                self.voltageValueSpinBox[i].setMinimum(int(volt.min_value))
                self.voltageValueSpinBox[i].setSuffix("V")
                # self.voltageValueSpinBox[i].setFixedWidth(70)
                if (int(volt.max_value)>10000):
                    self.measLCD[i].setDigitCount(5)
                    self.voltageValueSpinBox[i].setSingleStep(1000)
                else:
                    self.voltageValueSpinBox[i].setSingleStep(10)
                if MDEBUG:
                    print(volt.min_value)
                    print(volt.max_value)

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
        dial = SettingsDialog(self.timerVal,self)
        dial.show()
        self.settingsButton.setEnabled(False)
        if dial.exec_():
            ntime = dial.getValue()
            self.timerVal = ntime*1000
            for i in range(0,len(self.tangoDevices)):
                if self.tangoDevices[i] != False:
                    if (self.tangoDevices[i].state() == PyTango.DevState.ON
                        or self.tangoDevices[i].state() == PyTango.DevState.RUNNING):
                        if self.timer[i].isActive() == True:
                            self.timer[i].stop()
                            self.timer[i].setInterval(self.timerVal)
                            self.timer[i].start(0)
                        else:
                            self.timer[i].setInterval(self.timerVal)
                            self.timer[i].start(0)
            # self.settingsButton.setEnabled(False)
            time.sleep(3) # for
            self.settingsButton.setEnabled(True)
            if MDEBUG:
                print("EXEC DIAL" + str(ntime))
        else:
            self.settingsButton.setEnabled(True)
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


    def exceptionDialog(self,i, exc):
        lenExc = len(tuple(exc))
        if MDEBUG:
            print("setVoltage exception")
        if self.timer[i].isActive() == True:
            self.timer[i].stop()
        self.setEnabledVoltageEdit(i,False)
        mes = QtCore.QString("<b>Exceptions:</b><br><br>")
        for k in range(0,lenExc):
            mes = mes + QtCore.QString("Exception"+str(k)+"<br>")
            mes = mes + QtCore.QString("<b>Reason</b>: " + str(exc.args[k].reason) + "<br>")
            mes = mes + QtCore.QString("<b>Description</b>: " + str(exc.args[k].desc) + "<br>")
            mes = mes + QtCore.QString("<b>Origin</b>: " + str(exc.args[k].origin) + "<br>")
            mes = mes + QtCore.QString("<br>")

        error = QtGui.QMessageBox(QtGui.QMessageBox.Critical,"Error",mes,buttons = QtGui.QMessageBox.Ok)
        error.exec_()


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

    # def getFormatedToolTip(self, cache=True):
    #     """ The tooltip should refer to the device and not the state attribute.
    #         That is why this method is being rewritten
    #     """
    #     if self.modelObj is None:
    #         return self.getNoneValue()
    #     parent = self.modelObj.getParentObj()
    #     if parent is None:
    #         return self.getNoneValue()
    #     return self.toolTipObjToStr()

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
        buttonLayout = QtGui.QHBoxLayout()
        buttonLayout.addStretch(0)
        buttonLayout.addWidget(self.buttonOk)
        vertLayout.addLayout(buttonLayout)

        # self.setLayout(vertLayout)

        self.buttonOk.clicked.connect(self.accept)

class MyQPushButton(QtGui.QPushButton):
    def __init(self, parent):
        QtGui.QPushButton.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.emit(QtCore.SIGNAL('clicked(int)'),self.iter)
        # self.emit(QtCore.SIGNAL('released(int)'),self.iter)

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
        self.emit(QtCore.SIGNAL('timeout(int)'), self.iter)

class SettingsDialog(QtGui.QDialog):
    def __init__(self, tv, parent=None):
        QtGui.QWidget.__init__(self, parent)
        vertLayout = QtGui.QVBoxLayout(self)
        layout1 = QtGui.QHBoxLayout()

        self.setFixedSize(300, 150)
        self.timerSpinBox = QtGui.QSpinBox()
        self.timerSpinBox.setMinimum(1)
        self.timerSpinBox.setMaximum(60)
        self.timerSpinBox.setValue(tv//1000)
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