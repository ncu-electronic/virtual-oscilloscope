from PyQt5 import QtSerialPort
from PyQt5 import QtCore


def getAvailablePortName():
	available_ports = QtSerialPort.QSerialPortInfo.availablePorts()		#Get available port info
	available_port_name = list()
	for item in available_ports:
		if item.portName() != 'ttyS0' and item.portName() != 'ttyS1' \
		and item.portName() != 'ttyS2':
			available_port_name.append(item.portName())		#Append port names to a list except the linux ttySx port
	return available_port_name

def getAvailablePortDescription():
	available_ports = QtSerialPort.QSerialPortInfo.availablePorts()		#Get available port info
	available_port_description = list()
	for item in available_ports:
		if item.portName() != 'ttyS0' and item.portName() != 'ttyS1' \
		and item.portName() != 'ttyS2':
			available_port_description.append(item.description())		#Append port descriptions to a list except the linux ttySx port
	return available_port_description

def openPort(serial_instance, open_mode):
	value = serial_instance.open(open_mode)
	if value == True:
		print('Port ' + serial_instance.portName() + ' opened successful.')
	else:
		print('Port openning failed!')
		
def closePort(serial_instance):
	serial_instance.close()
