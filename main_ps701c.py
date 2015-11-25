from PyQt4 import QtGui
#from PyQt4 import QtCore, QtGui
# import PyTango
# from PyTango import Except
#from logilab.common.fileutils import lines

#from dialogParameter import SettingsDialog
# from datetime import datetime
import os.path
import ui_ps701c

fileCfg = "devsockets.cfg"

devices= list()

def checkCfgFile():
        #isCorrect = True
        if os.path.exists(fileCfg):
            try:
                file = open(fileCfg,"r")
                lines = file.readlines()
                file.close()
                print "Lines: " + str(len(lines)) # ??? debug
                if len(lines) > 0:
                    for line in lines:
                        lineDevName = line # ??? debug if lenth >1
                        splitLine = lineDevName.split("=")
                        if len(splitLine) >3: # ???
                            #isCorrect = False
                            continue
                            #self.printMessageToOutputEdit("Incorrect format of configfile")

                        else:
                            if (splitLine[0]=="[sock]"):
                                devices.append(splitLine[1])

            except IOError as e:
                #printMessageToOutputEdit(str(e))
                print("IOERROR")
        # else:
        #     showDialog()

def addDeviceToCfgFile(devName): # ??? for many devices
    with open(fileCfg,"w") as fileWrite:
            fileWrite.write(str("[sock]=" +devName+"="))

# def printMessageToOutputEdit(self, message):
#     dateTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
#     outputEdit.append("<b>" + dateTime + "</b>")
#     excMes = "Exception message: " + message
#     outputEdit.append(excMes)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)

    checkCfgFile()
    if len(devices)<11:
        # showDialog(MainWindow)
        # MainWindow.show()
        # ui = SettingsDialog()
        # MainWindow = QtGui.QDialog()
        # ui = tst.Ui_Dialog()
        # ui.setupUi(MainWindow)
        # MainWindow.show()

        MainWindow = QtGui.QMainWindow()
        ui = ui_ps701c.Ui_MainWindow()
        ui.setupUi(MainWindow,devices)
        MainWindow.show()
    else:
        print("more than 10")
        MainWindow = QtGui.QMainWindow()
        # ui = ui_ps701c.Ui_MainWindow()
        # ui.setupUi(MainWindow,devices)
        MainWindow.show()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)

    sys.exit(app.exec_())