from PySide6.QtWidgets import *
import numpy as np
from file_panel import *
from PySide6 import QtCore, QtWidgets, QtGui


class RecordPanel(QWidget):
	def __init__(self, _serial = None, _data = None, _file=None, parent = None):
		super(RecordPanel, self).__init__(parent)

		self.current_file = _file
		self._ser = _serial
		self.data = _data

		
		self.indication_text = QLabel("Please, select which classes you want to record in the toolbar just above.", alignment=Qt.AlignCenter)
		self.indication_text.setObjectName("Title")		

		self.panel = FilePanel(self._ser ,self.current_file, self.data)
  

		scroll = QtWidgets.QScrollArea()
		scroll.setWidget(self.panel)
		scroll.setWidgetResizable(True)
		scroll.setFixedHeight(400)
		scroll.setStyleSheet("background-color: lightgray;")


		self.btnRemoveAll = self.create_button("Remove all lines", 'red', 150, 30)
		self.btnRemoveAll.setObjectName("White")
		self.btnRemoveAll.clicked.connect(lambda:self.msg_box("Are you sure you want to remove all lines ?"))


		#self.comboBox_layout = QHBoxLayout()
		#self.comboBox_layout.addWidget(self.btnRemoveAll)


		self.layGrid = self.create_panel_header()
		self.layGrid.setObjectName("Header")

		
		self.vertical_layout_main = QVBoxLayout()
		self.vertical_layout_main.addWidget(scroll)

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setSpacing(15)
		self.main_layout.addWidget( self.indication_text)
		self.main_layout.addLayout(self.layGrid)
		self.main_layout.addLayout(self.vertical_layout_main)
		self.main_layout.addWidget(self.btnRemoveAll, alignment=Qt.AlignRight)
		self.main_layout.addStretch()
		self.setLayout(self.main_layout)

	def get_layout(self):
		return self.main_layout
	def create_button(self, _text, _bg, _w, _h):
		btn = QPushButton(_text)
		btn.setStyleSheet('QPushButton {background-color: ' + _bg + ';}')
		btn.setFixedWidth(_w)
		btn.setFixedHeight(_h)
		return btn

	def set_header(self, _text, _width, _height):
		obj = QLabel(str(_text), alignment=Qt.AlignCenter)
		obj.setObjectName("Header")
		obj.setStyleSheet("font-weight: bold")
		obj.setFixedWidth(_width)		
		obj.setFixedHeight(_height)
		return obj
		
	def create_panel_header(self):
		height = 50
		w = 100
		name = self.set_header("Name Class", 240, height)
		suffix = self.set_header("Suffix", 45, height)
		fileName = self.set_header("File Name", 300, height)
		recording = self.set_header("Record's Button", 250, height)
		status = self.set_header("Status", 95, height)
		clear_recording = self.set_header("Clear recording", 125, height)
		delete_line = self.set_header("Delete line", 120, height)

		layGrid = QHBoxLayout()
		layGrid.setSpacing(55) 
		layGrid.addWidget(name)
		layGrid.addWidget(suffix)
		layGrid.addWidget(fileName)
		layGrid.addWidget(recording)
		layGrid.addWidget(status)
		layGrid.addWidget(clear_recording)
		layGrid.addWidget(delete_line)

		return layGrid

	def msg_box(self, _text):
		msg = QMessageBox()
		msg.setText(_text)
		msg.setIcon(QMessageBox.Question)
		msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes) # seperate buttons with "|"
		#msg.buttonClicked.connect(lambda:self.switch_widget(True, False))
		result = msg.exec_()
		if result == QMessageBox.Yes:
			self.panel.remove_all_lines()
		else:
			msg.done(1)

	
	def remove_file(self, _name):
		filename = _name + ".csv"
		os.remove(_name)
