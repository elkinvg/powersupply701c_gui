#from PyQt4 import QtGui
from PyQt4.QtGui import QDialogButtonBox, QDialog, QWidget
from PyQt4.QtGui import QLineEdit, QLabel, QPushButton
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

class MyQPushButton(QPushButton):
    def __init(self, parent):
        QPushButton.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        self.emit(SIGNAL('clicked(int)'),self.iter)

def initTangoDevices(qobject):
    if len(qobject.devices) < 1:
        print("Devices less than 1")
        return
    # print "Number of devices: " + str(len(qobject.devices)) # for debug

    for i in range(0,len(qobject.devices)):
        try:
            # print("Device: -> " + qobject.devices[i])
            deviceTan = PyTango.DeviceProxy(qobject.devices[i])
            if deviceTan.state() == PyTango.DevState.OFF:
                # qobject.statusLed[i].setLedColor("white")
                # qobject.voltageValueSpinBox[i].setEnabled(False)
                # qobject.setVoltageButton[i].setEnabled(False)
                # setEnabledVoltageEdit(qobject,i,False)
                setEnabledVoltageEdit(qobject,i,True) # ??? test
                qobject.statusLed[i].setToolTip("TESTOFF") # ??? test
                print("TESTOFF is True now")
            elif deviceTan.state() == PyTango.DevState.FAULT:
                # qobject.statusLed[i].setLedColor("red")
                # qobject.voltageValueSpinBox[i].setEnabled(False)
                # qobject.setVoltageButton[i].setEnabled(False)
                setEnabledVoltageEdit(qobject,i,True)
                qobject.statusLed[i].setToolTip("TESTFAULT") # ??? test
                # print qobject.statusLed[i].getFormatedToolTip(True)
                print("TESTFAULT is True now")
            elif deviceTan.state() == PyTango.DevState.ON:
                # qobject.statusLed[i].setLedColor("green")
                # qobject.voltageValueSpinBox[i].setEnabled(True)
                # qobject.setVoltageButton[i].setEnabled(True)
                setEnabledVoltageEdit(qobject,i,True)
                qobject.statusLed[i].setToolTip("TESTON") # ??? test
                # print("TESTON")
            elif deviceTan.state() == PyTango.DevState.DISABLE:
                # qobject.voltageValueSpinBox[i].setEnabled(False)
                # qobject.setVoltageButton[i].setEnabled(False)
                setEnabledVoltageEdit(qobject,i,False)
                qobject.statusLed[i].setToolTip("TESTDISABLE") # ??? test
            qobject.tangoDevices.append(deviceTan)
        except PyTango.DevFailed as exc:
            qobject.statusLed[i].setLedColor("red")
            qobject.statusLed[i].setToolTip(str(exc)) # ??? test
            qobject.voltageValueSpinBox[i].setEnabled(False)
            qobject.setVoltageButton[i].setEnabled(False)
            qobject.tangoDevices.append(False)

def checkADCOutput(qobject,iter,tanDev):
    # tanDev = PyTango.DeviceProxy("ttt")
    result = tanDev.command_inout("CheckAdcOutput")
    if (result == -1):
        setEnabledVoltageEdit(qobject,iter,False)
    else:
        setEnabledVoltageEdit(qobject,iter,True)
        qobject.measLCD[iter].setProperty("intValue", result)

def setEnabledVoltageEdit(qobject,iter,isEnabled):
    qobject.voltageValueSpinBox[iter].setEnabled(isEnabled)
    qobject.setVoltageButton[iter].setEnabled(isEnabled)

def chargingOnCommand(tanDev):
    tanDev.command_inout("ChargingOn")

def chargingOffCommand(tanDev):
    tanDev.command_inout("ChargingOff")

# def setVoltageAttr(tanDev,valueOfVoltage):
#     tanDev.write_attribute("Voltage",valueOfVoltage)