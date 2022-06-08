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
	

	def _createActions(self):
		# Creating action using the first constructor
		# Creating actions using the second constructor
		self.preferences = QAction("&Preferences...", self)

		self.exitAction = QAction("&Exit", self)
		self.copyAction = QAction("&Copy", self)
		self.pasteAction = QAction("&Paste", self)
		self.cutAction = QAction("C&ut", self)
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
	sys.exit(app.exec_())
