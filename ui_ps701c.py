# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ps701c.ui'
#
# Created: Wed Nov 18 12:06:41 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import PyTango
import my_ps701c

devName = "sock/pssocket/1"

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(481, 250)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.statusLed = TaurusLed(self.centralwidget)
        self.statusLed.setGeometry(QtCore.QRect(380, 20, 61, 61))
        self.statusLed.setObjectName(_fromUtf8("statusLed"))
        self.voltageWheelEdit = TaurusWheelEdit(self.centralwidget)
        self.voltageWheelEdit.setGeometry(QtCore.QRect(270, 30, 58, 49))
        self.voltageWheelEdit.setProperty("integerDigits", 3)
        self.voltageWheelEdit.setProperty("decimalDigits", 0)
        self.voltageWheelEdit.setMinValue(0.0)
        self.voltageWheelEdit.setMaxValue(500.0)
        self.voltageWheelEdit.setObjectName(_fromUtf8("voltageWheelEdit"))
        self.measLabel = TaurusLabel(self.centralwidget)
        self.measLabel.setEnabled(True)
        self.measLabel.setGeometry(QtCore.QRect(80, 30, 51, 41))
        self.measLabel.setTextFormat(QtCore.Qt.AutoText)
        self.measLabel.setObjectName(_fromUtf8("measLabel"))
        self.voltageLabel = TaurusLabel(self.centralwidget)
        self.voltageLabel.setGeometry(QtCore.QRect(200, 20, 42, 49))
        self.voltageLabel.setObjectName(_fromUtf8("voltageLabel"))
        self.outputEdit = QtGui.QTextEdit(self.centralwidget)
        self.outputEdit.setGeometry(QtCore.QRect(30, 80, 411, 81))
        self.outputEdit.setObjectName(_fromUtf8("outputEdit"))
        self.reconnectButton = TaurusCommandButton(self.centralwidget)
        self.reconnectButton.setGeometry(QtCore.QRect(330, 170, 111, 27))
        self.reconnectButton.setObjectName(_fromUtf8("reconnectButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 481, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #self.my_setup()
        #elkin
        # self.testButton = QtGui.QPushButton
        device = PyTango.DeviceProxy(devName)
        #mes2 = device.status()
        #self.outputEdit.setText(mes2)
        statt = device.state()

        if (statt==PyTango.DevState.OFF):
			mes2 = device.status()
			self.outputEdit.setText(mes2)
			#self.outputEdit.append("aaaa")
        # but = self.reconnectButton
        # but.setCommand("Status")
        # but.setModel("sock/pssocket/1")

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.statusLed.setLedColor(_translate("MainWindow", "green", None))
        self.measLabel.setText(_translate("MainWindow", " 99.99", None))
        self.reconnectButton.setText(_translate("MainWindow", "Reconnect", None))

    def checkStatus(self, MainWindow):
        device = PyTango.DeviceProxy(devName) # ??????? Debug. Get name of proxy from settings
        mes = device.state()
        mes2 = device.status()

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

