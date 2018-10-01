import osc_gui          #Custom module  (Qt designer ui file transformed)
from PyQt5 import QtWidgets, QtSerialPort, QtCore, QtGui                #Official module
from collections import deque           #Official module
import array, pyqtgraph            # Official module

class OscMainWindow(QtWidgets.QMainWindow):
        def __init__(self):
                super().__init__()
                self.initUI()
                self.initVariables()
                self.initSerialPort()
                self.initSerialPlotTimer()
                self.connectSignalsWithSlots()
                self.show()

        def initUI(self):
                self.ui = osc_gui.Ui_MainWindow()               #Setup UI using "ui" file made from Qt Designer
                self.ui.setupUi(self)
                self.showMaximized()            #Following: MainWindow and dock widgets states configure
                self.tabifyDockWidget(self.ui.dockWidget_control, self.ui.dockWidget_measure)
                self.tabifyDockWidget(self.ui.dockWidget_measure, self.ui.dockWidget_control)
                self.getAvailableSerialPortInfoAndPutOntoUI()           #Attain Serial Port Info
                self.ui.splitter.setStretchFactor(1,1)          #Following: Set initial splitter position
                self.ui.splitter_4.setSizes([400,150])
                self.ui.pushButton_preview_view.setChecked(False)               #Following: UI state initialization
                self.ui.comboBox_16.setCurrentIndex(3)
                self.ui.actionDock_Source.setChecked(True)
                self.ui.dockWidget_measure.setHidden(True)
                self.ui.dockWidget_quick_set.setHidden(True)
                self.ui.dockWidget_control.setHidden(True)
                self.ui.widget_serial_text.setHidden(True)
                self.ui.graphicsView_wave.showGrid(x=True, y=True)        # Show x, y grids by default

        def initVariables(self):
                self.serial_port_name = self.ui.comboBox_15.currentText()
                self.serial_baudrate = int(self.ui.comboBox_16.currentText())
                self.serial_data_bits = int(self.ui.comboBox_17.currentText())
                if self.ui.comboBox_18.currentText() == 'None':         #Use attributes from QSerial class to set the serial_parity with the comboxbox's current text
                        self.serial_parity = QtSerialPort.QSerialPort.NoParity
                elif self.ui.comboBox_18.currentText() == 'Even':
                        self.serial_parity = QtSerialPort.QSerialPort.EvenParity
                elif self.ui.comboBox_18.currentText() == 'Odd':
                        self.serial_parity = QtSerialPort.QSerialPort.OddParity
                self.serial_stop_bits = int(self.ui.comboBox_19.currentText())
                self.serial_received_data = str()
                self.serial_received_data_one_time = str()
                self.temp_serial_str = str()
                self.serial_to_send = str()
                initial_temp_list = list()
                for i in range(0, 1000):
                    initial_temp_list.append(0)
                self.plot_data_array = array.array('i', initial_temp_list)           #Transform list to an array for actual plotting curves
                self.curve = self.ui.graphicsView_wave.plot(pen='r')            # Inititate curve using pyqtgraph module, the graphicsView_wave has been propmoted from QGraphicsView to PlotWidget     (which comes from pyqtgraph)

        def initSerialPort(self):
                self.serial_instance = QtSerialPort.QSerialPort()
                self.serial_instance.setPortName(self.serial_port_name)
                self.serial_instance.setBaudRate(self.serial_baudrate)
                self.serial_instance.setDataBits(self.serial_data_bits)
                self.serial_instance.setParity(self.serial_parity)
                self.serial_instance.setStopBits(self.serial_stop_bits)

        def initSerialPlotTimer(self):
                self.serial_plot_timer = QtCore.QTimer()
                self.serial_plot_timer.timeout.connect(self.plotSerialData)
                self.serial_plot_timer.start(30)

        def connectSignalsWithSlots(self):              #Manually connect slots which cannot be done in Qt Designer
                self.ui.pushButton_meas_dock.clicked.connect(lambda: self.controlDockFloating('meas'))          #Connect 'dock' pushbutton with 'floating control' function
                self.ui.pushButton_ctrl_dock.clicked.connect(lambda: self.controlDockFloating('ctrl'))
                self.ui.pushButton_source_dock.clicked.connect(lambda: self.controlDockFloating('source'))
                self.ui.pushButton_quick_set_dock.clicked.connect(lambda: self.controlDockFloating('quick_set'))                #Use 'lambda' for passing arguments to the connected function
                self.ui.comboBox_15.currentIndexChanged['int'].connect(self.comboBoxSerialPortCurrentIndexChanged)              #If combobox current index changed,then correspondingly change the variables
                self.ui.comboBox_16.currentIndexChanged.connect(self.comboBoxSerialBaudrateCurrentIndexChanged)
                self.ui.comboBox_17.currentIndexChanged.connect(self.comboBoxSerialDataBitCurrentIndexChanged)
                self.ui.comboBox_18.currentIndexChanged.connect(self.comboBoxSerialParityCurrentIndexChanged)
                self.ui.comboBox_19.currentIndexChanged.connect(self.comboBoxSerialStopBitCurrentIndexChanged)
                self.ui.pushButton_17.clicked.connect(lambda: self.openSerialPort(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.WriteOnly))
                self.ui.pushButton_18.clicked.connect(lambda: self.closeSerialPort())
                self.serial_instance.readyRead.connect(self.serialReadData)

        def controlDockFloating(self, choice):          #Control dock widgets floating states with user's choice
                if choice == 'meas':
                        if self.ui.dockWidget_measure.isFloating() == True:
                                self.ui.dockWidget_measure.setFloating(False)
                        else:
                                self.ui.dockWidget_measure.setFloating(True)
                elif choice == 'quick_set':
                        if self.ui.dockWidget_quick_set.isFloating() == True:
                                self.ui.dockWidget_quick_set.setFloating(False)
                        else:
                                self.ui.dockWidget_quick_set.setFloating(True)
                elif choice == 'source':
                        if self.ui.dockWidget_source.isFloating() == True:
                                self.ui.dockWidget_source.setFloating(False)
                        else:
                                self.ui.dockWidget_source.setFloating(True)
                elif choice == 'ctrl':  
                        if self.ui.dockWidget_control.isFloating() == True:
                                self.ui.dockWidget_control.setFloating(False)
                        else:
                                self.ui.dockWidget_control.setFloating(True)

        def comboBoxSerialPortCurrentIndexChanged(self, combobox_current_index):                #Corresponding while user change combobox_port index 
                self.serial_port_name = self.ui.comboBox_15.currentText()               #Changing current port
                self.ui.label_16.setText(self.available_port_description[combobox_current_index])               #Changing current description

        def comboBoxSerialBaudrateCurrentIndexChanged(self):            #combobox_current_index isn't passed because this function doesn't need index to change other label text
                self.serial_baudrate = int(self.ui.comboBox_16.currentText())

        def comboBoxSerialDataBitCurrentIndexChanged(self):
                self.serial_baudrate = int(self.ui.comboBox_17.currentText())

        def comboBoxSerialParityCurrentIndexChanged(self):              #Use attributes from QSerial class to set the serial_parity
                if self.ui.comboBox_18.currentText() == 'None':
                        self.serial_parity = QtSerialPort.QSerialPort.NoParity
                elif self.ui.comboBox_18.currentText() == 'Even':
                        self.serial_parity = QtSerialPort.QSerialPort.EvenParity
                elif self.ui.comboBox_18.currentText() == 'Odd':
                        self.serial_parity = QtSerialPort.QSerialPort.OddParity

        def comboBoxSerialStopBitCurrentIndexChanged(self):
                self.serial_stop_bits = int(self.ui.comboBox_19.currentText())

        def getAvailableSerialPortInfoAndPutOntoUI(self):
                available_ports = QtSerialPort.QSerialPortInfo.availablePorts()         #Get available port info
                available_port_description = self.getAvailableSerialPortDescription()
                available_port_name = list()
                for item in available_ports:
                        if item.portName() != 'ttyS0' and item.portName() != 'ttyS1' \
                        and item.portName() != 'ttyS2':
                                available_port_name.append(item.portName())             #Append port names to a list except the linux ttySx port
                for num in range(len(available_port_name)):             #The length of port name should equal to port description
                        self.ui.comboBox_15.addItem(available_port_name[num])           #Add port name and description in combo box
                        self.ui.label_16.setText(available_port_description[num])

        def getAvailableSerialPortDescription(self):
                available_ports = QtSerialPort.QSerialPortInfo.availablePorts()         #Get available port info
                available_port_description = list()
                for item in available_ports:
                        if item.portName() != 'ttyS0' and item.portName() != 'ttyS1' \
                        and item.portName() != 'ttyS2':
                                available_port_description.append(item.description())           #Append port descriptions to a list except the linux ttySx port
                return available_port_description

        def openSerialPort(self, open_mode):
                value = self.serial_instance.open(open_mode)
                if value == True:
                        print('Port ' + self.serial_instance.portName() + ' opened successful.')
                else:
                        print('Port openning failed!')
                
        def closeSerialPort(self):
                self.serial_instance.clear()            #Discards all characters from the output or input buffer
                self.serial_instance.close()

        def serialReadData(self):
                '''
                self.serial_received_data_one_time = str()              #Use serial_received_data_one_time and serial_raw_data_once to store and then add in text browser
                serial_received_raw_data_one_time = self.serial_instance.readAll()
                try:    
                        for elem in serial_received_raw_data_one_time:
                                self.serial_received_data_one_time += elem
                except:
                        pass
                self.serial_received_data += self.serial_received_data_one_time
                self.setSerialTextBrowser()
                self.parseSerialData()
                
                temp_char = self.serial_instance.read(1).decode()
                if temp_char != '$':
                    self.temp_serial_str += temp_char
                    #print(self.temp_serial_str)
                else:
                    print(self.temp_serial_str)
                    temp_str = self.temp_serial_str
                    self.temp_serial_str = ''
                    self.plot_data_array.append(int(temp_str))       # Add item to the rightest
                    self.plot_data_array.pop(0)      # Remove leftest item
                '''
                temp_byte = array.array('B')
                temp_byte.frombytes(self.serial_instance.read(1))
                self.plot_data_array.append(temp_byte[0])
                self.plot_data_array.pop(0)


        def parseSerialData(self):
                temp_string_0 = str()
                '''if self.serial_received_data_one_time != '$':
                        temp_string_0 += str(self.serial_received_data_one_time)
                else:
                        self.plot_data_deque.popleft()          #Remove leftest element
                        self.plot_data_deque.append(int(temp_string_0))         # Add a element at rightest position
                        self.plot_data_array = array.array('b', self.plot_data_deque)'''
                print(self.serial_received_data_one_time)

        def setSerialTextBrowser(self):
                self.ui.textBrowser_3.setPlainText(self.serial_received_data)
                self.ui.textBrowser_3.moveCursor(QtGui.QTextCursor.End)

        def plotSerialData(self):
                self.curve.setData(self.plot_data_array)
