import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from mercurial.changegroup import nocompress


class SettingsDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        #self.setGeometry(300, 300, 350, 80)
        self.setFixedSize(300, 300)
        self.setWindowTitle('InputDialog')
        self.button = QtGui.QPushButton('Dialog', self)
        self.socketName = QtGui.QLineEdit()
        self.nameOfServLabel = QtGui.QLabel('Server name')
        #self.nameOfServLabel.text('Server name')
        #self.socketName = QtGui.QTextLine()
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)

        self.layoutup = QtGui.QHBoxLayout(self)
        self.layoutup.addWidget(self.nameOfServLabel)
        self.layoutup.addWidget(self.socketName)

        self.layoutdown = QtGui.QHBoxLayout(self)
        self.layoutdown.addWidget(self.button)

        self.vertLayout = QtGui.QVBoxLayout(self)
        self.vertLayout.addLayout(self.layoutup)
        self.vertLayout.addLayout(self.layoutdown)

        self.setModal(True)
        self.button.clicked.connect(self.getValue)
        # self.connect(self.button, QtCore.SIGNAL('clicked()'), self.getValue)

    def getValue(self):
        self.accept()
        print("ssss")
        #self.close()
        getText = self.socketName.text()
        noText = "dfdf"

        # list = []
        # list.append(getText)
        # list.append('qqq')
        # list.append('zzz')
        return getText,noText


# class InputDialog(QtGui.QWidget):
#     def __init__(self, parent=None):
#         QtGui.QWidget.__init__(self, parent)
#
#         self.setGeometry(300, 300, 350, 80)
#         self.setWindowTitle('InputDialog')
#
#         self.button = QtGui.QPushButton('Dialog', self)
#         self.button.setFocusPolicy(QtCore.Qt.NoFocus)
#
#         self.button.move(20, 20)
#         self.connect(self.button, QtCore.SIGNAL('clicked()'), self.showDialog)
#         self.setFocus()
#
#         self.label = QtGui.QLineEdit(self)
#         self.label.move(130, 22)
#
#
#     def showDialog(self):
#         text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
#
#         if ok:
#             self.label.setText(unicode(text))
#
# app = QtGui.QApplication(sys.argv)
# icon = InputDialog()
# icon.show()
# app.exec_()