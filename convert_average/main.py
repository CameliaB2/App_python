from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 
import sys
import os
from os import path

import traitement as tr
import numpy as np



class Search_bar(QWidget):
	def __init__(self, _title, _ID, parent=None):
		QWidget.__init__(self, parent=parent)

		self.vertical_lay = QVBoxLayout()

		self.indication_text = QLabel(_title, alignment=Qt.AlignLeft)		
		self.indication_text.setStyleSheet("font-weight: bold")

		self.browser_line_lay = QHBoxLayout()
		self.path_qlineEdit = QLineEdit("")
		self.path_qlineEdit.setMinimumWidth(460)
		self.browser_button = QPushButton("Browse")
		self.browser_button.setFixedWidth(150)

		if (_ID == 'X42'):
			self.browser_button.clicked.connect(self.openFileNameDialog)
		if (_ID == 'X70'):
			self.browser_button.clicked.connect(self.search_directory)
			f = open("config.json", "r")
			if(f.read() == 'to_define'):
				str_desktop_path = os.path.realpath(__file__)
				str_desktop_path = str_desktop_path.replace('main.py', 'Outputs')
				self.write_path_file(str_desktop_path)
				f.close()
		
			f = open("config.json", "r")
			self.path_qlineEdit.setText(str(f.read()))
			f.close()

		self.vertical_lay.addWidget(self.indication_text)
		self.browser_line_lay.addWidget(self.path_qlineEdit)
		self.browser_line_lay.addWidget(self.browser_button)
		self.vertical_lay.addLayout(self.browser_line_lay)

		self.setLayout(self.vertical_lay)

	def write_path_file(self, _dir):
		f = open("config.json", "w")
		f.write(_dir)
		f.close()


	def search_directory(self, ):
		directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		if(directory != ""):
			self.path_qlineEdit.setText(directory)
			self.write_path_file(directory)
			return

	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "CSV Files (*.csv);; TXT Files(*.txt)", options=options)
		if fileName:
			self.path_qlineEdit.setText(fileName)


class Window(QMainWindow):
	def __init__(self, parent = None):
		super(Window, self).__init__( parent )
		self.setWindowTitle("Leka - COnvertisseur moyenne glissante")


		self.browser_lay = QVBoxLayout()
		

		self.range_line_lay = QHBoxLayout()
		self.range_text = QLabel("Range:")	
		self.range_text.setStyleSheet("font-weight: bold")
		self.range_qlineEdit = QLineEdit("4")
		self.range_qlineEdit.setFixedWidth(40)
		self.range_line_lay.addWidget(self.range_text)
		self.range_line_lay.addWidget(self.range_qlineEdit)

		self.file_to_transform = Search_bar('File to tranform', 'X42')
		self.path_file_to_reg = Search_bar('Path where the file will be registered', 'X70')


		self.generate_button  = self.create_button("Generate", "green")
		self.generate_button.clicked.connect(lambda: self.generate(int(self.range_qlineEdit.text())))

		self.generate_multiple_button  = self.create_button("Generate [sample - 4/8/16]", "orange")
		self.generate_multiple_button.clicked.connect(self.generate_multiple)

		self.indication_text = QLabel("File created successfully !", alignment=Qt.AlignCenter)

		self.browser_lay.addLayout(self.range_line_lay)
		self.browser_lay.addWidget(self.file_to_transform)
		self.browser_lay.addWidget(self.path_file_to_reg)
		self.browser_lay.addWidget(self.generate_button)
		self.browser_lay.addWidget(self.generate_multiple_button)


		centralWidget = QWidget()
		centralWidget.setLayout(self.browser_lay)




		self.setCentralWidget(centralWidget)

	def create_button(self, _title, _color):

		button = QPushButton(_title)
		button.setFixedHeight(30)
		button.setStyleSheet("background-color: " + _color)
		return button

	def generate_multiple(self):
		_range = [4, 8, 16]
		for val in _range:
			self.generate(val)

	def generate(self, _range):
		if(self.file_to_transform.path_qlineEdit.text() != '' and self.path_file_to_reg.path_qlineEdit.text() != '' ):
			if( path.exists(self.file_to_transform.path_qlineEdit.text()) and path.exists(self.path_file_to_reg.path_qlineEdit.text())):

				self.data = tr.read_file(self.file_to_transform.path_qlineEdit.text())
				self.aver_datas = tr.calculate_average_all_data(self.data[0], self.data[1], self.data[2], self.data[3], self.data[4], self.data[5], _range)

				self.set_name(_range)
				_path =  self.path_file_to_reg.path_qlineEdit.text() + '/' + self.name_file

				data_file = open(_path, "a")
				head_line = "AccX[mg]\tAccY[mg]\tAccZ[mg]\tGyrX[dps]\tGyrY[dps]\tGyrZ[dps]\t\n"
				data_file.write(head_line)
				for i in range(len(self.aver_datas[0])):
					data_file.write(str(self.aver_datas[0][i]) + '\t' + 
									str(self.aver_datas[1][i]) + '\t' + 
									str(self.aver_datas[2][i]) + '\t' + 
									str(self.aver_datas[3][i]) + '\t' + 
									str(self.aver_datas[4][i]) + '\t' +
									str(self.aver_datas[5][i]) + '\n')
				data_file.close()
				self.set_indication_label('File created successfully!', 'green')

			else:
				self.set_indication_label('File not created, path not found !', 'red')

		else:
			self.set_indication_label('File not created, empty path !', 'red')

	def set_indication_label(self, _text, _color):
		self.indication_text.setText(_text)
		self.indication_text.setStyleSheet("color: " + _color)
		self.browser_lay.addWidget(self.indication_text)

	def set_name(self, _range):
		self.name_file = self.file_to_transform.path_qlineEdit.text().split('/')[-1].split('.')[0] + '-average-Range_' + str(_range) + '.csv'
	
	name_file = ""
	data = []
	aver_datas = []

"""
		f = open("config.json", "r")
		if(f.read() == 'to_define'):
			str_desktop_path = os.path.realpath(__file__)
			str_desktop_path = str_desktop_path.replace('app.py', 'Recordings')
			self.write_path_file(str_desktop_path)
			f.close()
		
		f = open("config.json", "r")
		self.path_lineEdit.setText(str(f.read()))
		f.close()

		self.file.set_file_path(self.get_path())
		self.create_recording_path()

"""

if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = Window()
	win.show()
	sys.exit(app.exec_())
