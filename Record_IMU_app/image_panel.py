from PySide6 import QtCore, QtWidgets, QtGui
from numpy.lib import recfunctions as rfn
from chrono_class import Chrono_widget
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 
from classe_line import *
from chrono_class import *
from find_com import *
from time import sleep
import threading
import sys

IMAGE_CLASSE_WIDTH = 400
IMAGE_CLASSE_HEIGHT = 400

IMAGE_NEXT_SIZE = 150

class Image_Panel(QWidget):

	def __init__(self, _rec=None, _serial = None, parent = None):
		super(Image_Panel, self).__init__( parent )
		
		self.ser = _serial

		self.main_layout = QVBoxLayout(self)
		self.button_img_layout = QHBoxLayout()

		self.name = ""
		self.chrono_w = Chrono_widget(self.name, _rec, self, self.ser)
		self.chrono_w.setFixedHeight(75)
		self.stop_button = self.create_button("Stop", 'red', 150, 50)
		self.ready_button = self.create_button("Ready", 'green', 150, 50)
		self.stop_button.setObjectName("White")
		self.ready_button.setObjectName("White")

		self.info = QLabel("Please press on Ready to start the countdown. The recording will start right after (" + str(DURATION_INT) + "s).", alignment=QtCore.Qt.AlignCenter)
		self.info.setObjectName("Title")
		#self.info.setFixedHeight(100)

		# Open the correct pic according to the tab of chosen shape		
		self.shape_label = QLabel(self.name, alignment=QtCore.Qt.AlignCenter)
		self.shape_pic = QPixmap("Ressources/Classes/Images/" + str(self.name)+ ".png")
		self.shape_pic = self.shape_pic.scaled(IMAGE_CLASSE_WIDTH, IMAGE_CLASSE_WIDTH, QtCore.Qt.KeepAspectRatio)
		self.shape_label.setPixmap(self.shape_pic)



		self.ready_button.clicked.connect(lambda:self.chrono_w.countdown(self.info))
		self.ready_button.clicked.connect(lambda:self.ready_button.setEnabled(False))
		self.ready_button.clicked.connect(self.clear_serial)

		self.stop_button.clicked.connect(self.chrono_w.stop_chrono)
		self.stop_button.clicked.connect(lambda:self.msg_box("Are you sure you want to quit ?"))
		
		#Layout manager
		#self.main_layout.addWidget(self.chrono_w, alignment=QtCore.Qt.AlignCenter)
		
		#self.graph_layout.addWidget(_serial.graph, alignment=QtCore.Qt.AlignCenter)

		self.panel_right_layout = QVBoxLayout()

		
		self.total_time_label = QLabel("Total Time: " + str(self.chrono_w.time_record) + "s")
		self.total_time_label.setObjectName("first_info")
		self.time_per_move_label = QLabel("Time per Move: " + str(self.chrono_w.time_per_movement) + "s")
		self.time_per_move_label.setObjectName("infos")
		self.odr_label = QLabel("MLC ODR: " + str(self.ser.odr_freq))
		self.odr_label.setObjectName("infos")
		self.next_line = self.setNextImage()

		self.panel_right_layout.addWidget(self.chrono_w, alignment=QtCore.Qt.AlignCenter)
		self.panel_right_layout.addWidget(self.total_time_label, alignment=QtCore.Qt.AlignCenter)
		self.panel_right_layout.addWidget(self.time_per_move_label, alignment=QtCore.Qt.AlignCenter)
		self.panel_right_layout.addWidget(self.odr_label, alignment=QtCore.Qt.AlignCenter)
		#self.panel_right_layout.addWidget(_serial.graph, alignment=QtCore.Qt.AlignCenter) 
		self.panel_right_layout.addWidget(self.next_line, alignment=QtCore.Qt.AlignCenter) 
		self.panel_right_layout.addStretch()

		
		self.button_img_layout.addWidget(self.stop_button, alignment=QtCore.Qt.AlignRight)
		#self.button_img_layout.addWidget(self.shape_label)
		self.button_img_layout.addWidget(self.ready_button, alignment=QtCore.Qt.AlignLeft)
		

		self.main_layout.addWidget(self.info)	
	
		self.lay = QHBoxLayout()
		self.lay.addWidget(self.shape_label, alignment=QtCore.Qt.AlignCenter)
		self.lay.addLayout(self.panel_right_layout)
		self.main_layout.addLayout(self.lay)
		self.main_layout.addLayout(self.button_img_layout)
		#self.main_layout.addLayout(self.panel_right_layout)

		self.setLayout(self.main_layout)

	def setNextImage(self):
		widget = QWidget()
		self.next_shape_layout = QHBoxLayout()

		self.next_mouvement = QLabel("Next Movement: ")
		self.next_mouvement.setObjectName("infos")

		self.next_label = QLabel(self.name, alignment=QtCore.Qt.AlignCenter)
		self.next_pic = QPixmap("Ressources/Classes/Images/" + str(self.name)+ ".png") #by default
		self.next_pic = self.next_pic.scaled(IMAGE_NEXT_SIZE, IMAGE_NEXT_SIZE, QtCore.Qt.KeepAspectRatio)
		self.next_label.setPixmap(self.next_pic)

		self.next_shape_layout.addWidget(self.next_mouvement, alignment=QtCore.Qt.AlignCenter)
		self.next_shape_layout.addWidget(self.next_label, alignment=QtCore.Qt.AlignCenter)
		self.next_shape_layout.addStretch()
		widget.setLayout(self.next_shape_layout)
		return widget

	def setNext(self):
		print(str(self.ser.current_file.name_curr_shapes[self.ser.INDEX_SHAPE]))
		self.next_pic = QPixmap("Ressources/Classes/Images/" + str(self.ser.current_file.name_curr_shapes[self.ser.INDEX_SHAPE])+ ".png")
		self.next_pic = self.next_pic.scaled(IMAGE_NEXT_SIZE, IMAGE_NEXT_SIZE, QtCore.Qt.KeepAspectRatio)
		self.next_label.setPixmap(self.next_pic)

	def clear_serial(self):
		self.ser.serial.flushOutput()
		self.ser.serial.flushInput()

	def create_button(self, _text, _bg, _w, _h):
		btn = QPushButton(_text)
		btn.setStyleSheet("background-color: " + _bg)
		btn.setMinimumWidth(_w)
		btn.setMinimumHeight(_h)
		btn.setFont(QFont('Ressources/Fonts/Poppins', 16, QFont.Bold))
		#btn = QPushButton(self.font)
		return btn

	def update_time_label(self):
		self.total_time_label.setText("Total Time: " + str(self.chrono_w.time_record) + "s")
		self.time_per_move_label.setText("Time per Move: " + str(self.chrono_w.time_per_movement) + "s")
		self.odr_label.setText("MLC ODR: " + self.ser.odr_freq)

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
		self.shape_pic = self.shape_pic.scaled(IMAGE_CLASSE_WIDTH, IMAGE_CLASSE_HEIGHT, QtCore.Qt.KeepAspectRatio)
		
		self.shape_label.setMinimumHeight(IMAGE_CLASSE_HEIGHT)
		self.shape_label.setMinimumWidth(IMAGE_CLASSE_WIDTH)
		self.shape_label.setPixmap(self.shape_pic)
	
		#A faire ne propre
	def set_name_segment(self, name):
		self.next_pic = QPixmap("Ressources/Classes/Images/" + str(name)+ ".png")
		self.next_pic = self.next_pic.scaled(IMAGE_NEXT_SIZE, IMAGE_NEXT_SIZE, QtCore.Qt.KeepAspectRatio)
	
		self.next_label.setPixmap(self.next_pic)