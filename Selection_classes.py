<<<<<<< HEAD
=======

>>>>>>> bb4e5d92446d3c0410b830ea5eca518fc6fdd09f
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 
from Buttonclass import *

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
