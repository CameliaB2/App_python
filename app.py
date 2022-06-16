import sys
import threading
from numpy.lib import recfunctions as rfn
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import *

from classe_line import *
from classe_line import set_img_panel
from classe_line import set_rec_panel
from find_com import *
from Selection_classes import *

from chrono_class import Chrono_widget
from time import sleep
from file_manager import *
from record_panel import *
from file_panel import *
from image_panel import *
from preferences import *

import pyqtgraph as pg
import traitement as tr
import numpy as np
from random import randint


<<<<<<< HEAD
#from image_panel import Image_Panel

img_panel = ""
rec_panel = ""



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
		#self.comboBox_layout.addWidget(self.b_generateClassRow)
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

		#self.b_generateClassRow.clicked.connect(lambda: self.panel.generate_rowClass(self.comboBox))
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

		self.info = QLabel("Are you ready ?", alignment=QtCore.Qt.AlignCenter)
		self.info.setFont(QFont('Arial', 22))
		self.info.setFixedHeight(50)
		

		self.name = ""
		self.chrono_w = Chrono_widget(self.name, _serial, rec_panel, self)

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


		#self.lay_.addWidget(self.graph, alignment=QtCore.Qt.AlignRight)	#JE SAIS PAS OU LES METTRE 
		self.lay.addWidget(self.info)	
		self.lay.addWidget(self.chrono_w, alignment=QtCore.Qt.AlignCenter)
		self.lay_.addWidget(self.stop_button, alignment=QtCore.Qt.AlignCenter)
		self.lay_.addWidget(self.shape_label, alignment=QtCore.Qt.AlignCenter)
		self.lay_.addWidget(self.ready_button, alignment=QtCore.Qt.AlignCenter)
		self.lay.addLayout(self.lay_)
		self.lay.addWidget(_serial.graph, alignment=QtCore.Qt.AlignCenter)
		
		self.ready_button.clicked.connect(lambda:self.chrono_w.countdown(self.info))
		self.ready_button.clicked.connect(lambda:self.ready_button.setEnabled(False))
		self.ready_button.clicked.connect(lambda:self.info.setText("Record will begin in :"))
		#self.stop_button.clicked.connect(self.chrono_w.stop_chrono)

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




=======
>>>>>>> bb4e5d92446d3c0410b830ea5eca518fc6fdd09f
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

		#Thread de serial
		self.ser.set_SERIAL_SAVING_FLAG(0) #initialisation à 0 obligatoire ?
		x = threading.Thread(target=self.ser.thread_run, args=())
		x.start()
		
		self.rec_pan = RecordPanel(self.ser, self.listeClasses, self.current_file)
		self.img_pan = Image_Panel(self.rec_pan, self.ser)
		#Pour contrer le str object has no attribute blabla dans classRow
		set_img_panel(self.img_pan)
		set_rec_panel(self.rec_pan)
		
		

		self.lay = QVBoxLayout()
		centralWidget = QWidget()
		centralWidget.setLayout(self.lay)
		self.setCentralWidget(centralWidget)

		
		self.lay.setSpacing(0) 

		self.lay.addWidget(self.logo_label)
		self.lay.addWidget(self.img_pan)
		self.lay.addWidget(self.rec_pan)
		self.rec_pan.setVisible(True)
		self.img_pan.setVisible(False)
	

	def update_port_menu(self):
		self.findPorts.clear()
		for row, port in enumerate(self.ser.get_list_ports(), 1):
			recent_action = self.findPorts.addAction('&{}. {}'.format(
				row, port))
			recent_action.setData(port)
			recent_action.triggered.connect(lambda x=1, n=port: self.ser.change_port(n))

	def _createActions(self):
		# Creating action using the first constructor
		# Creating actions using the second constructor
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
		self.findPorts = toolsMenu.addMenu("PORT:")
		self.findPorts.setStatusTip('Choose the card\'s port')

		self.findPorts.aboutToShow.connect(self.update_port_menu)
		self.settings = {}

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
	self.rec_pan.setVisible(state1)
	self.img_pan.setVisible(state2)
	if(state1):
		self.img_pan.ready_button.setEnabled(True)



if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = Window()
	win.show()
	sys.exit(app.exec())
