import sys
import threading
from numpy.lib import recfunctions as rfn
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 
from classe_line import *
from find_com import *

from chrono_class import Chrono_widget
from time import sleep



class Image_Panel(QWidget):

	def __init__(self, _rec=None, _serial = None, parent = None):
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
		self.chrono_w = Chrono_widget(self.name, _rec, self, self.ser)
		
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
			self.chrono_w.switch_w(True, False)
		else:
			msg.done(1)
			#remettre en marche le chrono
			self.chrono_w.start_chrono()

	