#from PyQt4 import QtGui
from PyQt4.QtGui import QDialogButtonBox, QDialog, QWidget
from PyQt4.QtGui import QLineEdit, QLabel
from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, QFont
from PyQt4.QtCore import Qt, QString, SIGNAL

import PyTango

from taurus.qt.qtgui.display import TaurusLed
#from mercurial.changegroup import nocompress


class SettingsDialog(QDialog):
    def __init__(self,name, parent=None):
        QWidget.__init__(self, parent)
        #self.setGeometry(300, 300, 350, 80)


        self.setFixedSize(400, 200)
        self.setWindowTitle(name)

        # self.buttonOk = QtGui.QPushButton('Ok', self)
        # self.buttonCancel = QtGui.QPushButton('Cancel',self)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal
        )

        # self.socketName = QLineEdit()
        # self.nameOfServLabel = QLabel('Server name')
        #
        # font = QFont()
        # font.setPointSize(10)
        # font.setBold(True)
        # self.infoLabel = QLabel();
        # self.infoLabel.setFont(font)
        # textLabel = "<font color = red>"
        # textLabel += "Enter device name of Socket for PowerSupply "
        # textLabel += "in format \"domain/family/member\" <br>"
        # textLabel += "Example: socket/sock_ps701/1"
        # textLabel += "<\font>"
        # self.infoLabel.setWordWrap(True)
        # self.infoLabel.setText(textLabel)



        # layoutup.addWidget(self.nameOfServLabel)
        # layoutup.addWidget(self.socketName)

        vertLayout = QVBoxLayout(self)
        layoutup = QHBoxLayout()
        layoutdown = QHBoxLayout()

        layoutdown.addStretch(1)
        layoutdown.addWidget(self.buttons)

        # vertLayout.addWidget(self.infoLabel)


        self.statusLed = TaurusLed(self)
        self.statusLed.setModel(name + "/State")

        layoutup.addWidget(self.statusLed)


        vertLayout.addLayout(layoutup)
        vertLayout.addLayout(layoutdown)

        self.setModal(True)

        # self.buttons.accepted.connect(self.getValue)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        #self.button.clicked.connect(self.getValue)

    def setDevice(self,device):
        self.device = device

        vertLayout = QVBoxLayout(self)
        layoutup = QHBoxLayout()
        layoutdown = QHBoxLayout()

        layoutdown.addStretch(1)
        layoutdown.addWidget(self.buttons)

        # vertLayout.addWidget(self.infoLabel)


        self.statusLed = TaurusLed(self)
        self.statusLed.setModel(str(self.devices) + "/State")

        layoutup.addWidget(self.statusLed)


        vertLayout.addLayout(layoutup)
        vertLayout.addLayout(layoutdown)



    def getValue(self):
        getText = self.socketName.text()
        return getText

    def setDefaultValue(self,text):
        self.socketName.setText(QString(text))



class ExtendedQLabel(QLabel):

    def __init(self, parent):
        QLabel.__init__(self, parent)

    def deviceNameF(self,name):
        self.deviceName = name

    def mouseReleaseEvent(self, ev):
        self.emit(SIGNAL('clicked(QString)'),self.deviceName)


def setCommonProp(self):
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
