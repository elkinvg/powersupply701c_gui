# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dial.ui'
#
# Created: Wed Nov 25 17:02:06 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialogButtonBox, QDialog, QWidget
from PyQt4.QtGui import QLineEdit, QLabel
from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QFont
from PyQt4.QtCore import Qt, QString

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

class Ui_Dialog(QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setFixedSize(400, 200)

        vertLayout = QVBoxLayout()
        layoutup = QHBoxLayout()
        layoutdown = QHBoxLayout()



        self.socketName = QLineEdit()
        self.nameOfServLabel = QLabel('Server name')

        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal
        )

        # self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        # self.buttonBox.setGeometry(QtCore.QRect(10, 200, 301, 32))
        # self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        # self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        # self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.infoLabel = QLabel();
        self.infoLabel.setFont(font)
        textLabel = "<font color = red>"
        textLabel += "Enter device name of Socket for PowerSupply "
        textLabel += "in format \"domain/family/member\" <br>"
        textLabel += "Example: socket/sock_ps701/1"
        textLabel += "<\font>"
        self.infoLabel.setWordWrap(True)
        self.infoLabel.setText(textLabel)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        layoutup.addWidget(self.nameOfServLabel)
        layoutup.addWidget(self.socketName)

        layoutdown.addStretch(1)
        layoutdown.addWidget(self.buttonBox)

        vertLayout.addWidget(self.infoLabel)
        vertLayout.addLayout(layoutup)
        vertLayout.addLayout(layoutdown)

        # self.setLayout(vertLayout)
        Dialog.setLayout(vertLayout)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))

    def getValue(self):
        getText = self.socketName.text()
        return getText

    def setDefaultValue(self,text):
        self.socketName.setText(QString(text))


# if __name__ == "__main__":
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     Dialog = QtGui.QDialog()
#     ui = Ui_Dialog()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())

