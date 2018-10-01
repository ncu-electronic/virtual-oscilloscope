from PyQt5 import QtWidgets		#Official Library
from qt_main_window import OscMainWindow		#Custom Library
import sys		#Official Library


def main():
	app = QtWidgets.QApplication(sys.argv)
	osc_main_window = OscMainWindow()		#Instanitate a OscMainWindow class
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
