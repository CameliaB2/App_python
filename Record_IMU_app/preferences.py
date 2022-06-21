from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 

import os


class Preferences(QWidget):
	def __init__(self, _file, parent = None):
		super(Preferences, self).__init__( parent )
		self.title = 'Preferences'
		self.left = 100
		self.top = 100
		self.width = 640
		self.height = 100
		self.file = _file

		self.path_lineEdit = QLineEdit()
		self.path_lineEdit.setMaxLength(3000)
		f = open("config.json", "r")
		if(f.read() == 'to_define'):
			str_desktop_path = os.path.realpath(__file__)
			str_desktop_path = str_desktop_path.replace('preferences.py', 'Logs')
			self.write_path_file(str_desktop_path)
			f.close()
		
		f = open("config.json", "r")
		self.path_lineEdit.setText(str(f.read()))
		f.close()

		self.file.set_file_path(self.get_path())
		self.create_recording_path()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)

	def create_recording_path(self):
		self.browser_lay = QVBoxLayout()
		self.browser_line = QHBoxLayout()

		self.indication_text = QLabel("Logs path :", alignment=Qt.AlignLeft)		
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
			print("FileName: ", fileName)

	def search_directory(self):
		directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		if(directory != ""):
			self.file.set_file_path(directory)
			self.path_lineEdit.setText(str(directory))
			self.write_path_file(directory)

	def write_path_file(self, _dir):
		f = open("config.json", "w")
		f.write(_dir)
		f.close()

	def get_path(self):
		return self.path_lineEdit.text()

	def show_preferences(self):
		self.initUI()
		self.show()
	
	def close_preferences(self):
		self.close()


