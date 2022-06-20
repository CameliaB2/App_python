
from PySide6 import QtCore, QtWidgets, QtGui
from numpy.lib import recfunctions as rfn
from chrono_class import Chrono_widget
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 
from classe_line import *
from find_com import *
from time import sleep
import threading
import sys




class Image_Panel(QWidget):

	def __init__(self, _rec=None, _serial = None, parent = None):
		super(Image_Panel, self).__init__( parent )
		
		self.ser = _serial

		self.main_layout = QVBoxLayout(self)
		self.button_img_layout = QHBoxLayout()
		self.graph_layout = QHBoxLayout()

		self.info = QLabel("Please press on Ready to start the countdown. The recording will start right after.", alignment=QtCore.Qt.AlignCenter)
		self.info.setFont(QFont('Arial', 22))
		#self.info.setFixedHeight(100)
		
		
		self.name = ""
		self.chrono_w = Chrono_widget(self.name, _rec, self, self.ser)
		
		self.stop_button = self.create_button("Stop", 'red', 150, 50)
		self.ready_button = self.create_button("Ready", 'green', 150, 50)

		# Open the correct pic according to the tab of chosen shape		
		self.shape_label = QLabel(self.name, alignment=QtCore.Qt.AlignCenter)
		self.shape_pic = QPixmap("Ressources/Classes/Images/" + str(self.name)+ ".png")
		self.shape_pic = self.shape_pic.scaled(250, 354, QtCore.Qt.KeepAspectRatio)
		self.shape_label.setPixmap(self.shape_pic)



		self.ready_button.clicked.connect(lambda:self.chrono_w.countdown(self.info))
		self.ready_button.clicked.connect(lambda:self.ready_button.setEnabled(False))

		self.stop_button.clicked.connect(self.chrono_w.stop_chrono)
		self.stop_button.clicked.connect(lambda:self.msg_box("Are you sure you want to quit ?"))
		
			#Layout manager
		self.main_layout.addWidget(self.info)	
		self.main_layout.addWidget(self.chrono_w, alignment=QtCore.Qt.AlignCenter)

		self.button_img_layout.addWidget(self.stop_button, alignment=QtCore.Qt.AlignCenter)
		self.button_img_layout.addWidget(self.shape_label)
		self.button_img_layout.addWidget(self.ready_button, alignment=QtCore.Qt.AlignCenter)

		self.graph_layout.addWidget(_serial.graph, alignment=QtCore.Qt.AlignCenter)
		
		self.main_layout.addLayout(self.button_img_layout)
		self.main_layout.addLayout(self.graph_layout)
		self.setLayout(self.main_layout)


	def create_button(self, _text, _bg, _w, _h):
		btn = QPushButton(_text)
		btn.setStyleSheet("background-color: " + _bg)
		#btn.setFixedWidth(_w)
		#btn.setFixedHeight(_h)
		btn.setFont(QFont('Ressources/Fonts/Poppins', 16, QFont.Bold))
		#btn = QPushButton(self.font)
		return btn

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

	
	def set_name_(self, n):
		self.name = n
		self.shape_pic = QPixmap("Ressources/Classes/Images/" + str(self.name)+ ".png")
		self.shape_pic = self.shape_pic.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
		self.shape_label.setPixmap(self.shape_pic)
	
