from PyQt4 import QtCore, QtGui
import PyTango
from taurus.qt.qtgui.display import TaurusLed

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

class Ui_MainWindow_mt10(QtGui.QMainWindow):
    def setupUi(self, MainWindow,devices):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))

        self.devices = devices
        self.tangoDevices = list() # list of tango-devices

        self.deviceNameLabel = list()
        self.statusLed = list()

        self.horSize = 6

        j = k = 0
        for i in range(0,len(self.devices)):
            self.deviceNameLabel.append(QtGui.QLabel())
            textLabel = "<font color = red> <b>"
            textLabel += QtCore.QString(self.devices[i])
            textLabel += "<\b><\font>"

            self.deviceNameLabel[i].setText(textLabel)
            self.deviceNameLabel[i].setFixedWidth(150)

            self.statusLed.append(TaurusLed(self))
            self.statusLed[i].setModel(str(self.devices[i]) + "/State")

            k = k + 1
            if k >= self.horSize:
                j = j + 1
                k = 0



        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        MainWindow.setCentralWidget(self.centralwidget)

        vertWinSize = (j+1)*50
        horWinSize = self.horSize*200
        MainWindow.setFixedSize(horWinSize,vertWinSize)

        self.layouts(MainWindow)

        self.centerOnScreen(MainWindow)
        self.initDevices()


    def layouts(self, MainWindow):
        mainLayout = QtGui.QGridLayout()

        gridLayouts = list()

        j = k = 0
        for i in range(0,len(self.devices)):
            gridLayouts.append(QtGui.QHBoxLayout())
            gridLayouts[i].addWidget(self.statusLed[i])
            gridLayouts[i].addWidget(self.deviceNameLabel[i])


            mainLayout.addLayout(gridLayouts[i],j,k)
            k = k + 1
            if k >= self.horSize:
                j = j + 1
                k = 0

        centralWidget = MainWindow.centralWidget()
        centralWidget.setLayout(mainLayout)

    def initDevices(self):

        for i in range(0,len(self.devices)):
            try:
                print("Device: -> " + self.devices[i])
                deviceTan = PyTango.DeviceProxy(self.devices[i])
                if deviceTan.state() == PyTango.DevState.OFF:
                    # self.statusLed[i].setLedColor("white")
                    self.statusLed[i].setToolTip("TESTOFF") # ??? test
                    print("TESTOFF")
                elif deviceTan.state() == PyTango.DevState.FAULT:
                    # self.statusLed[i].setLedColor("red")
                    self.statusLed[i].setToolTip("TESTFAULT") # ??? test
                    print self.statusLed[i].getFormatedToolTip(True)
                    print("TESTFAULT")
                elif deviceTan.state() == PyTango.DevState.ON:
                    # self.statusLed[i].setLedColor("green")
                    self.statusLed[i].setToolTip("TESTON") # ??? test
                    print("TESTON")
                self.tangoDevices.append(deviceTan)
            except PyTango.DevFailed as exc:
                self.statusLed[i].setLedColor("red")
                self.statusLed[i].setToolTip(str(exc)) # ??? test

    def centerOnScreen (self,MainWindow):
        resolution = QtGui.QDesktopWidget().screenGeometry()
        MainWindow.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))
