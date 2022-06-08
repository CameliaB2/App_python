from PySide6.QtWidgets import *
import numpy as np
from file_panel import *
from Selection_classes import *
from Serial import Serial as parent


class RecordPanel(QWidget):
	def __init__(self, _serial = None, _liste=None, _file=None, parent = None):
		super(RecordPanel, self).__init__(parent)

		self.main_layout = QVBoxLayout(self)
		
		self.indication_text = QLabel("Please, select which classes you want to record in the scrolling menu just below.\n\tClick on the update button to update your classes.", alignment=Qt.AlignCenter)
		self.indication_text.setMaximumHeight(75)
		self.indication_text.setFont(QFont('Arial', 15))
		
		self.comboBox_layout = QHBoxLayout(self)
		self.selectClasses_button = QPushButton("Select classes")
		self.selectClasses_button.setMaximumWidth(200)		
		self.selectClasses_button.setFixedHeight(30)


		self.btnRemoveAll = QPushButton("Remove all")
		self.btnRemoveAll.setStyleSheet("background-color: red")
		self.btnRemoveAll.setMaximumWidth(100)
		self.btnRemoveAll.setFixedHeight(35)

		self.comboBox_layout.addWidget(self.selectClasses_button)
		self.comboBox_layout.addWidget(self.btnRemoveAll)

		self.main_layout.setSpacing(15)
		self.main_layout.addWidget( self.indication_text)
		self.main_layout.addLayout(self.comboBox_layout)

		self.current_file = _file
		self._ser = _serial

		height = 50
		w = 100
		self.layGrid = QHBoxLayout(self)

		self.name = self.set_header("Name Class", 240, height)
		self.suffix = self.set_header("Suffix", 45, height)
		self.fileName = self.set_header("File Name", 300, height)
		self.recording = self.set_header("Record's Button", 250, height)
		self.status = self.set_header("Status", 95, height)
		self.clear_recording = self.set_header("Clear recording", 125, height)
		self.delete_line = self.set_header("Delete line", 120, height)

		self.layGrid.setSpacing(55) 

		self.layGrid.addWidget(self.name)
		self.layGrid.addWidget(self.suffix)
		self.layGrid.addWidget(self.fileName)
		self.layGrid.addWidget(self.recording)
		self.layGrid.addWidget(self.status)
		self.layGrid.addWidget(self.clear_recording)
		self.layGrid.addWidget(self.delete_line)
		
		self.main_layout.addLayout(self.layGrid)

		self.frame = QFrame(self)
		self.frame.setFrameShape(self.frame.Box)
		self.frame.setLineWidth(1)
		self.frame.setStyleSheet("background-color: #cfebf7")
		self.panel = FilePanel(self.frame, self._ser ,self.current_file)
		
		self.selection = Selection_classes(_liste, self.panel)		
		self.selectClasses_button.clicked.connect(self.selection.Selection_classes_show)

		self.main_layout.addWidget(self.frame)
		self.setLayout(self.main_layout)

		self.btnRemoveAll.clicked.connect(lambda:self.msg_box("Are you sure you want to remove all lines ?"))



	def set_header(self, text, width, height):
		obj = QLabel(str(text), alignment=Qt.AlignCenter)
		obj.setStyleSheet("font-weight: bold")
		obj.setFixedWidth(width)		
		obj.setFixedHeight(height)
		return obj
		

	def msg_box(self, text):
		msg = QMessageBox()
		msg.setText(text)
		msg.setIcon(QMessageBox.Question)
		msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes) # seperate buttons with "|"
		#msg.buttonClicked.connect(lambda:self.switch_widget(True, False))
		result = msg.exec_()
		if result == QMessageBox.Yes:
			self.panel.remove_all_lines()
		else:
			msg.done(1)

	
	def remove_file(self, name):
		filename = name + ".txt"
		os.remove(name)
