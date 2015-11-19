# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ps701c.ui'
#
# Created: Thu Nov 19 15:36:48 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSlot
import PyTango

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
        #MainWindow.resize(481, 250)
        MainWindow.setFixedSize(481, 250)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.statusLed = TaurusLed(self.centralwidget)
        self.statusLed.setGeometry(QtCore.QRect(380, 20, 61, 61))
        self.statusLed.setObjectName(_fromUtf8("statusLed"))
        self.voltageWheelEdit = TaurusWheelEdit(self.centralwidget)
        self.voltageWheelEdit.setGeometry(QtCore.QRect(230, 30, 58, 49))
        self.voltageWheelEdit.setProperty("integerDigits", 3)
        self.voltageWheelEdit.setProperty("decimalDigits", 0)
        self.voltageWheelEdit.setMinValue(0.0)
        self.voltageWheelEdit.setMaxValue(500.0)
        self.voltageWheelEdit.setObjectName(_fromUtf8("voltageWheelEdit"))
        self.measLabel = TaurusLabel(self.centralwidget)
        self.measLabel.setEnabled(True)
        self.measLabel.setGeometry(QtCore.QRect(30, 30, 51, 41))
        self.measLabel.setTextFormat(QtCore.Qt.AutoText)
        self.measLabel.setObjectName(_fromUtf8("measLabel"))
        self.voltageLabel = TaurusLabel(self.centralwidget)
        self.voltageLabel.setGeometry(QtCore.QRect(120, 30, 42, 49))
        self.voltageLabel.setObjectName(_fromUtf8("voltageLabel"))
        self.outputEdit = QtGui.QTextEdit(self.centralwidget)
        self.outputEdit.setGeometry(QtCore.QRect(30, 80, 411, 81))
        self.outputEdit.setReadOnly(True)
        self.outputEdit.setObjectName(_fromUtf8("outputEdit"))
        self.reconnectButton = QtGui.QPushButton(self.centralwidget)
        self.reconnectButton.setGeometry(QtCore.QRect(350, 170, 85, 27))
        self.reconnectButton.setObjectName(_fromUtf8("reconnectButton"))
        self.setButton = QtGui.QPushButton(self.centralwidget)
        self.setButton.setGeometry(QtCore.QRect(30, 170, 85, 27))
        self.setButton.setObjectName(_fromUtf8("setButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #elkin
        #self.connect(self.reconnectButton,QtCore.SIGNAL('clicked()'),self,QtCore.SLOT('testSlot()'))
        self.connect(self.reconnectButton,QtCore.SIGNAL('clicked()'),self.testSlot)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.statusLed.setLedColor(_translate("MainWindow", "green", None))
        self.measLabel.setText(_translate("MainWindow", " 99.99", None))
        self.reconnectButton.setText(_translate("MainWindow", "Reconnect", None))
        self.setButton.setText(_translate("MainWindow", "Settings", None))

    #@QtCore.pyqtSlot(object)
    @pyqtSlot()
    def testSlot(self):
        self.outputEdit.append("Signal")

from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from taurus.qt.qtgui.input import TaurusWheelEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

