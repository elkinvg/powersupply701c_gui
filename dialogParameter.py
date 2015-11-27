#from PyQt4 import QtGui
from PyQt4.QtGui import QDialogButtonBox, QDialog, QWidget
from PyQt4.QtGui import QLineEdit, QLabel
from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QFont
from PyQt4.QtCore import Qt, QString
#from mercurial.changegroup import nocompress


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        #self.setGeometry(300, 300, 350, 80)
        vertLayout = QVBoxLayout(self)
        layoutup = QHBoxLayout()
        layoutdown = QHBoxLayout()

        self.setFixedSize(400, 200)
        self.setWindowTitle('InputDialog')

        # self.buttonOk = QtGui.QPushButton('Ok', self)
        # self.buttonCancel = QtGui.QPushButton('Cancel',self)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal
        )

        self.socketName = QLineEdit()
        self.nameOfServLabel = QLabel('Server name')

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


        layoutup.addWidget(self.nameOfServLabel)
        layoutup.addWidget(self.socketName)

        layoutdown.addStretch(1)
        layoutdown.addWidget(self.buttons)

        vertLayout.addWidget(self.infoLabel)
        vertLayout.addLayout(layoutup)
        vertLayout.addLayout(layoutdown)

        # self.setModal(True)

        # self.buttons.accepted.connect(self.getValue)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        #self.button.clicked.connect(self.getValue)


    def getValue(self):
        getText = self.socketName.text()
        return getText

    def setDefaultValue(self,text):
        self.socketName.setText(QString(text))