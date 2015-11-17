# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ps701c.ui'
#
# Created: Tue Nov 17 15:22:42 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        MainWindow.resize(466, 254)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.taurusLed = TaurusLed(self.centralwidget)
        self.taurusLed.setGeometry(QtCore.QRect(390, 0, 61, 61))
        self.taurusLed.setObjectName(_fromUtf8("taurusLed"))
        self.taurusWheelEdit = TaurusWheelEdit(self.centralwidget)
        self.taurusWheelEdit.setGeometry(QtCore.QRect(190, 40, 58, 49))
        self.taurusWheelEdit.setProperty("integerDigits", 3)
        self.taurusWheelEdit.setProperty("decimalDigits", 0)
        self.taurusWheelEdit.setMinValue(0.0)
        self.taurusWheelEdit.setMaxValue(500.0)
        self.taurusWheelEdit.setObjectName(_fromUtf8("taurusWheelEdit"))
        self.measLabel = TaurusLabel(self.centralwidget)
        self.measLabel.setEnabled(True)
        self.measLabel.setGeometry(QtCore.QRect(30, 50, 81, 41))
        self.measLabel.setTextFormat(QtCore.Qt.AutoText)
        self.measLabel.setObjectName(_fromUtf8("measLabel"))
        self.taurusLabel = TaurusLabel(self.centralwidget)
        self.taurusLabel.setGeometry(QtCore.QRect(120, 40, 42, 49))
        self.taurusLabel.setObjectName(_fromUtf8("taurusLabel"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 466, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.taurusLed.setLedColor(_translate("MainWindow", "green", None))
        self.measLabel.setText(_translate("MainWindow", " 99.99", None))

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

