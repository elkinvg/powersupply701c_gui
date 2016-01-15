#!/usr/bin/env python
from PyQt4 import QtGui
import ui_ps701c
import PyTango

# propertyTreeName = 'devsockets'
propertyTreeName = 'ps701_devices2'
# propertyTreeName = 'devintango2'

devicesName = list()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)

    try:
        db = PyTango.Database()
        devicesProperties = db.get_object_property_list(propertyTreeName,'*')
    except:
        print "EXCEPT"

    for i in range(0,len(devicesProperties)):
        dev = db.get_property(propertyTreeName,devicesProperties[i])
        key = devicesProperties[i]
        devicesName.append(dev[key][0])

    if len(devicesName) < 21 and len(devicesName) > 0:
        MainWindow = QtGui.QMainWindow()
        ui = ui_ps701c.Ui_MainWindow()
        ui.setupUi(MainWindow,devicesName)
        MainWindow.show()
    # elif len(devicesProperties) > 20:
    #     print("more than 10")
    #     MainWindow = QtGui.QMainWindow()
    #     ui = ui_ps701c_mt10.Ui_MainWindow_mt10()
    #     ui.setupUi(MainWindow,devicesName)
    #     MainWindow.show()
    else:
        print("EXIT")
        exit()

    sys.exit(app.exec_())