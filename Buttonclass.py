from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 



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