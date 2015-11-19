
import sys
#import qqq

# Taurus modules
from taurus.external.qt import Qt
from taurus.qt.qtgui.application import TaurusApplication

# PyQt4 modules
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QObject, pyqtSlot

class Taurus_Tango_Client_Widget (QtGui.QWidget): 

    def __init__(self):
        super(Taurus_Tango_Client_Widget, self).__init__()       
        self.initUI()

    @pyqtSlot()
    def foo(self):
		reply = QtGui.QMessageBox.question(self, "message", "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			QtGui.qApp.quit()
        
    def initUI(self):
		# Create layout map
		main_layout = Qt.QVBoxLayout()
		self.setLayout(main_layout)
		self.setWindowTitle(' Taurus test ')
		self.setGeometry(300, 300, 250, 150)

		x_layout_1 = QtGui.QHBoxLayout()
		main_layout.addLayout(x_layout_1)

		# Create widgets
		close_button = Qt.QPushButton('Close \n application')
		self.connect( close_button, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()') )

		dialog_button = Qt.QPushButton('test \n dialog')
		self.connect( dialog_button, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('foo()') )

		x_layout_1.addWidget( close_button )
		x_layout_1.addWidget( dialog_button )

		from taurus.qt.qtgui.display import TaurusLabel
		w = TaurusLabel()
		main_layout.addWidget(w)
		w.model = 'sys/taurustest/1/position' 	
		self.show()
		
		#qqq.foo('zzsadasdf')

      
def main():
    app = TaurusApplication(sys.argv)
    widget = Taurus_Tango_Client_Widget()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
