from PyQt4 import QtGui
#from PyQt4 import QtCore, QtGui
# import PyTango
# from PyTango import Except
#from logilab.common.fileutils import lines

#from dialogParameter import SettingsDialog
# from datetime import datetime
import os.path
import ui_ps701c
import ui_ps701c_mt10

import PyTango

propertyTreeName = 'devsockets'
devicesName = list()
# def printMessageToOutputEdit(self, message):
#     dateTime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
#     outputEdit.append("<b>" + dateTime + "</b>")
#     excMes = "Exception message: " + message
#     outputEdit.append(excMes)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)

    # checkCfgFile()
    try:
        db = PyTango.Database()
        devicesProperties = db.get_object_property_list(propertyTreeName,'*')
        print len(devicesProperties)
    except:
        print "EXCEPT"

    for i in range(0,len(devicesProperties)):
        dev = db.get_property(propertyTreeName,devicesProperties[i])
        key = devicesProperties[i]
        # # print dev[devicesProperties[i]]
        # print key
        # devkey = dev.get(key)
        # print dev[key][0]
        devicesName.append(dev[key][0])
        # print devkey[0]
        # print dev[key]
        # devicesName.append(str(dev[devicesProperties[i]]))

    if len(devicesName)<11 and len(devicesName) > 0:
    # if len(devicesProperties)<11 and len(devicesProperties) > 0:
        # showDialog(MainWindow)
        # MainWindow.show()
        # ui = SettingsDialog()
        # MainWindow = QtGui.QDialog()
        # ui = tst.Ui_Dialog()
        # ui.setupUi(MainWindow)
        # MainWindow.show()

        MainWindow = QtGui.QMainWindow()
        ui = ui_ps701c.Ui_MainWindow()
        ui.setupUi(MainWindow,devicesName)
        MainWindow.show()
    elif len(devicesProperties) > 10:
        print("more than 10")
        MainWindow = QtGui.QMainWindow()
        ui = ui_ps701c_mt10.Ui_MainWindow_mt10()
        ui.setupUi(MainWindow,devicesName)
        MainWindow.show()
    else:
        print("EXIT")
        exit()
        # dist = db.get_property("/devsockets","1")
        # dist = db.get_object_list("dev*")
        # dist2 = db.get_object_property_list('devsockets','*')
        # prop = db.get_property('devsockets',dist2[3])
        # lenn = len(dist2)
        # print dist2[3]
        # print lenn
        # print prop
        # MainWindow = QtGui.QMainWindow()
        # MainWindow.show()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)

    sys.exit(app.exec_())