from PySide6.QtWidgets import *
import numpy as np
from file_panel import *
from Selection_classes import *
from PySide6 import QtCore, QtWidgets, QtGui


class RecordPanel(QWidget):
	def __init__(self, _serial = None, _liste=None, _file=None, parent = None):
		super(RecordPanel, self).__init__(parent)

		self.current_file = _file
		self._ser = _serial

		
		self.indication_text = QLabel("Please, select which classes you want to record in the toolbar just above.", alignment=Qt.AlignCenter)
		self.indication_text.setMaximumHeight(75)
		self.indication_text.setFont(QFont('Arial', 15))
		

		self.panel = FilePanel(self._ser ,self.current_file)
  

		scroll = QtWidgets.QScrollArea()
		scroll.setWidget(self.panel)
		scroll.setWidgetResizable(True)
		scroll.setFixedHeight(400)
		scroll.setStyleSheet("background-color: lightgray;")


		self.btnRemoveAll = self.create_button("Remove all lines", 'red', 150, 30)
		self.btnRemoveAll.clicked.connect(lambda:self.msg_box("Are you sure you want to remove all lines ?"))


		#self.comboBox_layout = QHBoxLayout()
		#self.comboBox_layout.addWidget(self.btnRemoveAll)


		height = 50
		w = 100
		self.name = self.set_header("Name Class", 240, height)
		self.suffix = self.set_header("Suffix", 45, height)
		self.fileName = self.set_header("File Name", 300, height)
		self.recording = self.set_header("Record's Button", 250, height)
		self.status = self.set_header("Status", 95, height)
		self.clear_recording = self.set_header("Clear recording", 125, height)
		self.delete_line = self.set_header("Delete line", 120, height)

		

		self.layGrid = QHBoxLayout()
		self.layGrid.setSpacing(55) 
		self.layGrid.addWidget(self.name)
		self.layGrid.addWidget(self.suffix)
		self.layGrid.addWidget(self.fileName)
		self.layGrid.addWidget(self.recording)
		self.layGrid.addWidget(self.status)
		self.layGrid.addWidget(self.clear_recording)
		self.layGrid.addWidget(self.delete_line)
		
		self.vertical_layout_main = QVBoxLayout()
		self.vertical_layout_main.addWidget(scroll)

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setSpacing(15)
		self.main_layout.addWidget( self.indication_text)
		self.main_layout.addLayout(self.layGrid)
		self.main_layout.addLayout(self.vertical_layout_main)
		self.main_layout.addWidget(self.btnRemoveAll, alignment=Qt.AlignRight)

		self.setLayout(self.main_layout)


	def create_button(self, _text, _bg, _w, _h):
		btn = QPushButton(_text)
		btn.setStyleSheet('QPushButton {background-color: ' + _bg + '; color: white;}')
		btn.setFixedWidth(_w)
		btn.setFixedHeight(_h)
		return btn

	def set_header(self, _text, _width, _height):
		obj = QLabel(str(_text), alignment=Qt.AlignCenter)
		obj.setStyleSheet("font-weight: bold")
		obj.setFixedWidth(_width)		
		obj.setFixedHeight(_height)
		return obj
		

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
		filename = _name + ".txt"
		os.remove(_name)
