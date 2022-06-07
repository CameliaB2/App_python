import sys
import threading
from numpy.lib import recfunctions as rfn
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 
from classe_line import ClassRow
from find_com import *

from chrono_class import Chrono_widget
#from image_panel import *
from time import sleep
from file_manager import *
import pyqtgraph as pg
import datetime

#from image_panel import Image_Panel

img_panel = ""
rec_panel = ""

class Selection_classes(QWidget):
	def __init__(self, _list, _panel, parent = None):
		super(Selection_classes, self).__init__( parent )

		self.liste = _list
		self.panel = _panel

		scroll = QScrollArea(self)
		scroll.setWidgetResizable(True)
		self.content = QWidget()
		scroll.setWidget(self.content)
		self.lay = QVBoxLayout(self.content)

		self.button_list = []
		for el in _list:
			self.button_list.append(ButtonClass(el, _panel))
			self.lay.addWidget(self.button_list[-1])

		self.setStyleSheet("QScrollArea{min-width:300 px; min-height: 400px}")
		self.setWindowTitle("Classes Selection")

	def Selection_classes_show(self):
		self.show()


class ButtonClass(QWidget):
	def __init__(self, _name, _panel, parent = None):
		super(ButtonClass, self).__init__( parent )
		self.name = _name
		self.panel = _panel

		self.line_layout = QHBoxLayout()
		self.name_class = QLabel(str(self.name), alignment=Qt.AlignCenter)
		self.name_class.setFixedHeight(30)

		self.button = QPushButton("+")
		self.button.setFixedWidth(30)
		self.button.setFixedHeight(30)
		self.button.setStyleSheet("background-color: green")
		self.line_layout.addWidget(self.name_class)
		self.line_layout.addWidget(self.button)
		
		self.button.clicked.connect(lambda: self.panel.add_item(self.name))
		self.setLayout(self.line_layout)

	def set_name(self, _name):
		self.name = _name

	_name = "test"



class RecordPanel(QWidget):
	def __init__(self,_serial, _liste, _file, parent = None):
		super(RecordPanel, self).__init__( parent )

		self.main_layout = QVBoxLayout(self)
		
		self.indication_text = QLabel("Please, select which classes you want to record in the scrolling menu just below.\n\tClick on the update button to update your classes.", alignment=Qt.AlignCenter)
		self.indication_text.setMaximumHeight(75)
		self.indication_text.setFont(QFont('Arial', 15))
		
		self.comboBox_layout = QHBoxLayout(self)
		self.selectClasses_button = QPushButton("Select classes")
		self.selectClasses_button.setMaximumWidth(200)		
		self.selectClasses_button.setFixedHeight(30)


		self.btnRemoveAll = QPushButton("Remove all")
		self.btnRemoveAll.setStyleSheet("background-color: red")
		self.btnRemoveAll.setMaximumWidth(100)
		self.btnRemoveAll.setFixedHeight(35)

		self.comboBox_layout.addWidget(self.selectClasses_button)
		self.comboBox_layout.addWidget(self.btnRemoveAll)

		self.main_layout.setSpacing(15)
		self.main_layout.addWidget( self.indication_text)
		self.main_layout.addLayout(self.comboBox_layout)

		self.current_file = _file
		self._ser = _serial

		height = 50
		w = 100
		self.layGrid = QHBoxLayout(self)

		self.name = self.set_header("Name Class", 240, height)
		self.suffix = self.set_header("Suffix", 45, height)
		self.fileName = self.set_header("File Name", 300, height)
		self.recording = self.set_header("Record's Button", 250, height)
		self.status = self.set_header("Status", 95, height)
		self.clear_recording = self.set_header("Clear recording", 125, height)
		self.delete_line = self.set_header("Delete line", 120, height)

		self.layGrid.setSpacing(55) 

		self.layGrid.addWidget(self.name)
		self.layGrid.addWidget(self.suffix)
		self.layGrid.addWidget(self.fileName)
		self.layGrid.addWidget(self.recording)
		self.layGrid.addWidget(self.status)
		self.layGrid.addWidget(self.clear_recording)
		self.layGrid.addWidget(self.delete_line)
		
		self.main_layout.addLayout(self.layGrid)

		self.frame = QFrame(self)
		self.frame.setFrameShape(self.frame.Box)
		self.frame.setLineWidth(1)
		self.frame.setStyleSheet("background-color: #cfebf7")
		self.panel = FilePanel(self.frame, self._ser ,self.current_file)
		
		self.selection = Selection_classes(_liste, self.panel)		
		self.selectClasses_button.clicked.connect(self.selection.Selection_classes_show)

		self.main_layout.addWidget(self.frame)
		self.setLayout(self.main_layout)

		self.btnRemoveAll.clicked.connect(lambda:self.msg_box("Are you sure you want to remove all lines ?"))



	def set_header(self, text, width, height):
		obj = QLabel(str(text), alignment=Qt.AlignCenter)
		obj.setStyleSheet("font-weight: bold")
		obj.setFixedWidth(width)		
		obj.setFixedHeight(height)
		return obj
		

	def msg_box(self, text):
		msg = QMessageBox()
		msg.setText(text)
		msg.setIcon(QMessageBox.Question)
		msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes) # seperate buttons with "|"
		#msg.buttonClicked.connect(lambda:self.switch_widget(True, False))
		result = msg.exec_()
		if result == QMessageBox.Yes:
			self.panel.remove_all_lines()
		else:
			msg.done(1)

	
	def remove_file(self, name):
		filename = name + ".txt"
		os.remove(name)

		

class FilePanel(QWidget):
	def __init__(self, _frame, _ser, _file, parent = None):
		super(FilePanel, self).__init__( parent )

		self.lay = QVBoxLayout(_frame)  
		self.lay.setAlignment(Qt.AlignTop)

		self.file = _file
		self.ser = _ser
		self.id = 0
		self.classR = ''


	def add_item(self, _name):
		self.classR = ClassRow(_name, self.ser, self.id, self.file, img_panel, rec_panel)
		self.l_classRow.append(self.classR)
		self.lay.addWidget(self.l_classRow[-1])
		self.id += 1

	def remove_line(self, _id):
		self.l_classRow[_id].deleteLater()
	
	def remove_all_lines(self):
		self.tab = self.l_classRow
		for i in range(len(self.tab)):
			self.tab[i].deleteLater()


	l_classRow = []
	tab = []
	_name = ''
	

class Image_Panel(QWidget):

	def __init__(self, _serial, parent = None):
		super(Image_Panel, self).__init__( parent )
		
		self.lay = QVBoxLayout(self)
		self.lay_ = QHBoxLayout(self)
		self._lay = QHBoxLayout(self)

		self.info = QLabel("Please press on Ready to start the countdown. The recording will start right after.", alignment=QtCore.Qt.AlignCenter)
		self.info.setFont(QFont('Arial', 22))
		self.info.setFixedHeight(100)
		
		self.ser = _serial
		
		#self.graph = Graph(self.ser)
		self.name = ""
		self.chrono_w = Chrono_widget(self.name, self.ser, rec_panel, self)

		self.stop_button = QPushButton("Stop")
		self.stop_button.setStyleSheet("background-color: red")
		self.stop_button.setMaximumWidth(250)
		self.stop_button.setMinimumHeight(100)

		#self.font_ = QFont('Arial', 50)
		#self.ready_button = QPushButton(self.font_)
		self.ready_button = QPushButton("Ready")
		self.ready_button.setStyleSheet("background-color: green")
		self.ready_button.setMaximumWidth(250)
		self.ready_button.setMinimumHeight(100)

		self.shape_label = QLabel(self.name, alignment=QtCore.Qt.AlignCenter)
		# Open the correct pic according to the tab of chosen shape		
		self.shape_pic = QPixmap("Figures/"+ str(self.name)+ ".png")
		self.shape_pic = self.shape_pic.scaled(250, 354, QtCore.Qt.KeepAspectRatio)
		self.shape_label.setPixmap(self.shape_pic)


		self.lay.addWidget(self.info)	
		self.lay.addWidget(self.chrono_w, alignment=QtCore.Qt.AlignCenter)
		#self._lay.addWidget(self.graph, alignment=QtCore.Qt.AlignRight)	#JE SAIS PAS OU LES METTRE 
		self._lay.addWidget(self.shape_label)
		self.lay_.addWidget(self.stop_button, alignment=QtCore.Qt.AlignCenter)
		self.lay_.addWidget(self.ready_button, alignment=QtCore.Qt.AlignCenter)
		self.lay.addLayout(self._lay)
		self.lay.addLayout(self.lay_)
		
		self.ready_button.clicked.connect(lambda:self.chrono_w.countdown(self.info))
		self.ready_button.clicked.connect(lambda:self.ready_button.setEnabled(False))
		#self.ready_button.clicked.connect(self.print_)
		
		self.stop_button.clicked.connect(self.chrono_w.stop_chrono)
		self.stop_button.clicked.connect(lambda:self.msg_box("Are you sure you want to quit ?"))
		

		self.setLayout(self.lay)


	def set_name_(self, n):
		self.name = n
		self.shape_pic = QPixmap("Figures/"+ str(self.name)+ ".png")
		self.shape_pic = self.shape_pic.scaled(250, 354, QtCore.Qt.KeepAspectRatio)
		self.shape_label.setPixmap(self.shape_pic)


	def msg_box(self, text):
		msg = QMessageBox()
		msg.setText(text)
		msg.setIcon(QMessageBox.Question)
		msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes) # seperate buttons with "|"
		#msg.buttonClicked.connect(lambda:self.switch_widget(True, False))
		result = msg.exec_()
		if result == QMessageBox.Yes:
			switch_widget(True, False)
		else:
			msg.done(1)
			#remettre en marche le chrono
			self.chrono_w.start_chrono()

	def print_(self):
		print(self.ser.SERIAL_SAVING_FLAG)
		print(self.ser.headline_write)
		print(self.ser.RUNNING_FLAG)

class Preferences(QWidget):
	def __init__(self, _file, parent = None):
		super(Preferences, self).__init__( parent )
		self.title = 'Preferences'
		self.left = 100
		self.top = 100
		self.width = 640
		self.height = 100
		self.file = _file

		self.path_lineEdit = QLineEdit("Recordings")
		self.file.set_file_path(self.get_path())

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.create_recording_path()

	def create_recording_path(self):
		self.browser_lay = QVBoxLayout()
		self.browser_line = QHBoxLayout()

		self.indication_text = QLabel("Recording path :", alignment=Qt.AlignLeft)		
		self.indication_text.setStyleSheet("font-weight: bold")

		self.browser_button = QPushButton("Browse")
		self.browser_button.clicked.connect(self.search_directory)

		self.browser_line.addWidget(self.path_lineEdit)
		self.browser_line.addWidget(self.browser_button)

		self.browser_lay.addWidget(self.indication_text)
		self.browser_lay.addLayout(self.browser_line)

		self.setLayout(self.browser_lay)

	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;CSV Files (*.py);; TXT Files(*.txt)", options=options)
		if fileName:
			print(fileName)

	def search_directory(self):
		directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		if(directory != ""):
			self.path_lineEdit.setText(directory)
			self.file.set_file_path(self.get_path())

	def get_path(self):
		return self.path_lineEdit.text()

	def show_preferences(self):
		self.initUI()
		self.show()


"""class Graph(QWidget):
	def __init__(self, _serial, parent = None):
		super(Graph, self).__init__( parent )
		
		self.serial = _serial

		self.acc_graph = self.create_graph('w', "Acceleration", "Acceleration (mg)")
		self.gyr_graph = self.create_graph('w', "Gyroscope", "Gyroscope (dps)")

		self.lay = QVBoxLayout(self)

		self.init_plot()

		getData_thr = threading.Thread(target=self.run_thread, args=())
		getData_thr.start()

		self.lay.addWidget(self.acc_graph)
		self.lay.addWidget(self.gyr_graph)

		self.setLayout(self.lay)
		#self.show()

	def create_graph(self, bg_color, title, label_y):
		styles = {"color": "#f00", "font-size": "20px"}
		graph = pg.PlotWidget()
		graph.setBackground(bg_color)
		graph.setTitle(title)
		graph.addLegend()
		graph.setLabel("left", label_y, **styles)
		graph.setLabel("bottom", "Time (s)", **styles)
		graph.setFixedHeight(300)
		return graph

	def run_thread(self):
		while True:
			if self.serial.SERIAL_SAVING_FLAG == 2:
				self.start_time = datetime.datetime.now()
			while self.serial.SERIAL_SAVING_FLAG == 1: 
				print("Zero")
				temp = self.serial.serial.readline() #Capture serial output as a decoded stringata = temp.decode()
				data = temp.decode()
				data_str = str(data)
				print("Zero bis")

				if data_str :#Check if we have data
					print("First")
					data_split_ch = data_str.split(' > ')
					if len(data_split_ch) > 1:
						print("Second")
						data_split_tab = data_str.split('\t')
						if len(data_split_tab) == 6:
							print("Third")
							self.acc[0].append(data_split_tab[0])
							self.acc[1].append(data_split_tab[1])
							self.acc[2].append(data_split_tab[2])

							self.gyr[0].append(data_split_tab[3])
							self.gyr[1].append(data_split_tab[4])
							self.gyr[2].append(data_split_tab[5])
							curr_time = datetime.datetime.now()
							
							print(data_split_tab)
							self.t.append(curr_time - self.start_time)
							self.update_all_plot(self.t, self.acc[0], self.acc[1], self.acc[2], self.gyr[0], self.gyr[1], self.gyr[2])

				#sleep(0.038)
	def init_plot(self):

		self.acc_x_line = self.acc_plot("Acc_X", 'r')
		self.acc_y_line = self.acc_plot("Acc_Y", 'g')
		self.acc_z_line = self.acc_plot("Acc_Z", 'b')

		self.gyr_x_line = self.gyr_plot("Gyr_X", 'r')
		self.gyr_y_line = self.gyr_plot("Gyr_Y", 'g')
		self.gyr_z_line = self.gyr_plot("Gyr_Z", 'b')

	def acc_plot(self, plotname, color):
		pen = pg.mkPen(color=color)
		return self.acc_graph.plot(name=plotname, pen=pen)

	def gyr_plot(self, plotname, color):
		pen = pg.mkPen(color=color)
		return self.gyr_graph.plot(name=plotname, pen=pen)

	def update_set_data(self, plot_line, x, y):
		plot_line.setData(x, y)
		#plot_line.plot(x,y)

	def update_all_plot(self, t, acc_X, acc_Y, acc_Z, gyr_X, gyr_Y, gyr_Z):
		self.update_set_data(self.acc_x_line, t, acc_X)
		self.update_set_data(self.acc_y_line, t, acc_Y)
		self.update_set_data(self.acc_z_line, t, acc_Z)

		self.update_set_data(self.gyr_x_line, t, gyr_X)
		self.update_set_data(self.gyr_y_line, t, gyr_Y)
		self.update_set_data(self.gyr_z_line, t, gyr_Z)
	
	acc = [[0], [0], [0]]
	gyr = [[0], [0], [0]]
	start_time = 0
	t = [0]
"""




class Window(QMainWindow):
	def __init__(self, parent = None):
		super(Window, self).__init__( parent )
		self.setWindowTitle("Leka - Interface d'enregistrement")
		self.resize(1280, 720)

		self.logo_label = QLabel("Logo_label", alignment=QtCore.Qt.AlignRight)
		self.logo_pic = QPixmap("Figures/leka_logo.png")
		self.logo_pic = self.logo_pic.scaled(100, 72, QtCore.Qt.KeepAspectRatio)
		self.logo_label.setPixmap(self.logo_pic)
		self.logo_label.setFixedHeight(100)

		
		
		self.current_file = File_manager()

		self._createActions()
		self._createMenuBar()
		self._importCSV()
		
		self.ser = Serial_COM(self.current_file, self.findPorts)

		self.preference_onglet = Preferences(self.current_file)
		self.preferences.triggered.connect(self.preference_onglet.show_preferences)

		self.isConnected = QLabel("Connected", alignment=QtCore.Qt.AlignCenter)
		self.isConnected.setFixedWidth(100)
		self.isConnected.setStyleSheet("border: 3px; border-radius: 5px; min-height:40px; min-width:40px; background-color: gray")
		self.isConnected.setFixedHeight(20)
		


		#Thread de serial
		self.x = threading.Thread(target=self.ser.thread_run, args=())
		self.x.start()

		self.lay = QVBoxLayout()
		self.lay_ = QHBoxLayout()
		centralWidget = QWidget()
		centralWidget.setLayout(self.lay)
		self.setCentralWidget(centralWidget)

		global img_panel, rec_panel

		
		rec_panel = RecordPanel(self.ser, self.listeClasses, self.current_file)
		img_panel = Image_Panel(self.ser)

		self.lay_.setSpacing(200)
		self.lay.setSpacing(0) 

		self.lay_.addWidget(self.isConnected)
		self.lay_.addWidget(self.logo_label)
		
		self.lay.addLayout(self.lay_)
		self.lay.addWidget(img_panel)
		self.lay.addWidget(rec_panel)
		rec_panel.setVisible(True)
		img_panel.setVisible(False)


		if(self.ser.isConnected_flag == True):
			self.isConnected.setStyleSheet("border: 3px; border-radius: 5px; min-height:40px; min-width:40px; background: #c7ea46")
		else:
			self.isConnected.setStyleSheet("border: 3px; border-radius: 5px; min-height:40px; min-width:40px; background-color: gray")
		

		#app.aboutToQuit.connect(self.closeEvent)
	

		
	"""def closeEvent(self):
		#Your desired functionality here
		print('Close button pressed')
		self.ser.thread_terminate()
		sys.exit(0)"""
		

	def _createActions(self):
		# Creating action using the first constructor
		self.newAction = QAction(self)
		self.newAction.setText("&New")
		# Creating actions using the second constructor
		self.openAction = QAction("&Open...", self)
		self.importAction = QAction("&Import...", self)
		self.preferences = QAction("&Preferences...", self)

		self.exitAction = QAction("&Exit", self)
		self.copyAction = QAction("&Copy", self)
		self.pasteAction = QAction("&Paste", self)
		self.cutAction = QAction("&Cut", self)
		self.helpContentAction = QAction("&Help Content", self)
		self.aboutAction = QAction("&About", self)


	def _createMenuBar(self):
		menuBar = self.menuBar()
		# File menu
		fileMenu = QMenu("&File", self)
		menuBar.addMenu(fileMenu)
		fileMenu.addAction(self.preferences)
		fileMenu.addAction(self.exitAction)
		
		# Edit menu
		toolsMenu = menuBar.addMenu("&Tools")
		#editMenu.addAction(self.copyAction)
		# Find and Replace submenu in the Edit menu
		self.findPorts = toolsMenu.addMenu("PORT:")
		self.findPorts.setStatusTip('Choose the card\'s port')

		# Help menu
		helpMenu = menuBar.addMenu("&Help")
		helpMenu.addAction(self.helpContentAction)
		helpMenu.addAction(self.aboutAction)



	def _importCSV(self):
		file1 = open('Figures/class_list.csv', 'r')
		Lines = file1.readlines()
		 
		self.listeClasses = []
		self.listeImgClasses = []
		self.countClasses = 0
		# Strips the newline character
		for line in Lines:
			self.countClasses += 1
			self.listeClasses.append(line.strip().split("\t")[0])
			#self.listeImgClasses.append(line.strip().split("\t")[1])

		file1.close()

	
	def msg_box(self, text):
		msg = QMessageBox()
		msg.setText(text)
		msg.setIcon(QMessageBox.Question)
		msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes) # seperate buttons with "|"
		#msg.buttonClicked.connect(lambda:self.switch_widget(True, False))
		result = msg.exec_()
		if result == QMessageBox.Yes:
			switch_widget(True, False)
		else:
			msg.done(1)
	

def switch_widget(state1, state2):
	rec_panel.setVisible(state1)
	img_panel.setVisible(state2)
	if(state1):
		img_panel.ready_button.setEnabled(True)



if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = Window()
	win.show()
	sys.exit(app.exec_())
