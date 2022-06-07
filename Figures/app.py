
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 
from classe_line import ClassRow

class CheckableComboBox(QComboBox): 
	def __init__(self, _liste, parent = None): 
		super(CheckableComboBox, self).__init__(parent) 
		self.view().pressed.connect(self.handleItemPressed) 
		self.listeClasses = _liste
		self._createComboBox()
		self._changed = False
    
	def _createComboBox(self): 
		self.addItems(self.listeClasses) 
		for i in range(len(self.listeClasses)):
			item = self.model().item(i)
			item.setCheckState(Qt.Unchecked) 


	def add_item(self, item): 
		self.l_classesChecked.append(item.text())
		if item.text() in self.l_classesUnchecked:
			self.l_classesUnchecked.remove(item.text())
  
	def remove_item(self, item): 
		self.l_classesUnchecked.append(item.text())
		if item.text() in self.l_classesUnchecked:
			self.l_classesChecked.remove(item.text())
    
	def handleItemPressed(self, index): 
		item = self.model().itemFromIndex(index) 

		if item.checkState() == Qt.Checked: 
			item.setCheckState(Qt.Unchecked) 
			self.remove_item(item)
			self.count -= 1
		else: 
			item.setCheckState(Qt.Checked) 
			self.add_item(item)
			self.count += 1

		self._changed = True

	def hidePopup(self):
		if not self._changed:
			super(CheckableComboBox, self).hidePopup()
		self._changed = False

	def get_classesChecked(self):
		return self.l_classesChecked

	def get_classesUnchecked(self):
		return self.l_classesUnchecked

	def set_EmptyclassesUnchecked(self):
		self.l_classesUnchecked = []

	l_classes = []
	l_classesChecked = []
	l_classesUnchecked = []
	count = 0


class RecordPanel(QWidget):
	def __init__(self, _liste, parent = None):
		super(RecordPanel, self).__init__( parent )

		self.main_layout = QVBoxLayout(self)


		self.indication_text = QLabel("Please, select which classes you want to record in the scrolling menu just below.\n\tClick on the update button to update your classes.", alignment=Qt.AlignCenter)
		self.indication_text.setFixedHeight(75)

		self.comboBox_layout = QHBoxLayout(self)
		self.comboBox = CheckableComboBox(_liste)
		self.comboBox.setMaximumWidth(200)		
		self.comboBox.setFixedHeight(30)

		self.b_generateClassRow = QPushButton("Update")
		self.b_generateClassRow.setStyleSheet("background-color: orange")
		self.b_generateClassRow.setMaximumWidth(80)
		self.b_generateClassRow.setFixedHeight(30)

		self.comboBox_layout.addWidget(self.comboBox)
		self.comboBox_layout.addWidget(self.b_generateClassRow)

		self.main_layout.addWidget( self.indication_text)
		self.main_layout.addLayout(self.comboBox_layout)

		self.panel = FilePanel()
		"""
		self.panel.setStyleSheet("background-color: gray")
		self.panel.setMaximumWidth(200)		
		self.panel.setFixedHeight(500)"""

		self.b_generateClassRow.clicked.connect(lambda: self.panel.generate_rowClass(self.comboBox))
		self.main_layout.addWidget(self.panel)
		self.create_manage_all()
		self.setLayout(self.main_layout)



	def create_manage_all(self):
		self.manage_all_layout = QHBoxLayout(self)
		self.btnRecordAll = QPushButton("Record all")
		self.btnRecordAll.setStyleSheet("background-color: orange")
		self.btnRecordAll.setMaximumWidth(100)

		self.manage__right_all_layout = QHBoxLayout(self)

		self.btnSaveAll = QPushButton("Save all")
		self.btnSaveAll.setStyleSheet("background-color: green")
		self.btnSaveAll.setMaximumWidth(100)

		self.btnDeleteAll = QPushButton("Delete all")
		self.btnDeleteAll.setStyleSheet("background-color: red")
		self.btnDeleteAll.setMaximumWidth(100)

		self.manage_all_layout.addWidget(self.btnRecordAll)
		self.manage__right_all_layout.addWidget(self.btnSaveAll)
		self.manage__right_all_layout.addWidget(self.btnDeleteAll)

		self.manage_all_layout.addLayout(self.manage__right_all_layout)
		self.main_layout.addLayout(self.manage_all_layout)


class FilePanel(QWidget):
	def __init__(self, parent = None):
		super(FilePanel, self).__init__( parent )

		self.lay = QVBoxLayout(self)  
		self.setLayout(self.lay)



	def generate_rowClass(self, _comboBox):
		new_l_classesUnchecked = _comboBox.get_classesUnchecked()
		new_l_classesChecked = _comboBox.get_classesChecked()

		self.remove_items(new_l_classesUnchecked)
		self.add_items(new_l_classesChecked)
		self._comboBox.set_EmptyclassesUnchecked()

		
	def remove_items(self, _list):
		size = len(_list)
		index_to_pop = []
		for i in range(size):
			if (_list[i] in self.l_currClassesChecked):
				self.l_currClassesChecked.remove(_list[i])
				for index, item in enumerate(self.l_classRow):
					if item.get_name() == _list[i]:
						index_to_pop.append(index-1)
						break

		for i in range(len(index_to_pop)):
			self.l_classRow[index_to_pop[i]].deleteLater()
			self.l_classRow.pop(index_to_pop[i])


	def add_items(self, _list):
		size = len(_list)
		for i in range(size):
			if not (_list[i] in self.l_currClassesChecked):
				self.l_currClassesChecked.append(_list[i])
				self.l_classRow.append(ClassRow(_list[i]))
				self.lay.addWidget(self.l_classRow[-1])



	l_currClassesChecked = []
	l_classRow = []


class Image_Panel(QWidget):

	def __init__(self, test, parent = None):
		super(Image_Panel, self).__init__( parent )
		
		lay = QVBoxLayout(self)
		lay_ = QHBoxLayout(self)

		
		self.info = QLabel("Are you ready ?", alignment=QtCore.Qt.AlignCenter)
		self.info.setFont(QFont('Arial', 22))
		self.info.setFixedHeight(100)

		self.chrono_w = Chrono_widget(self)
		self.stop_button = QPushButton("Stop")
		self.stop_button.setStyleSheet("background-color: red")
		self.stop_button.setMaximumWidth(200)
		self.stop_button.setMinimumHeight(50)

		self.ready_button = QPushButton("Ready")
		self.ready_button.setStyleSheet("background-color: green")
		self.ready_button.setMaximumWidth(200)
		self.ready_button.setMinimumHeight(50)

		self.shape_label = QLabel(test, alignment=QtCore.Qt.AlignCenter)
		# Open the correct pic according to the tab of chosen shapes
		self.shape_pic = QPixmap("Figures/Vertical.png")

		self.shape_pic = self.shape_pic.scaled(500, 708, QtCore.Qt.KeepAspectRatio)
		self.shape_label.setPixmap(self.shape_pic)

		lay_.addWidget(self.ready_button, alignment=QtCore.Qt.AlignCenter)
		lay.addWidget(self.info)
		lay.addWidget(self.chrono_w, alignment=QtCore.Qt.AlignCenter)
		lay_.addWidget(self.stop_button, alignment=QtCore.Qt.AlignCenter)
		lay.addLayout(lay_)
		lay.addWidget(self.shape_label)
		

		self.stop_button.clicked.connect(self.close_im_panel)
		self.ready_button.clicked.connect(self.chrono_w.countdown)
		self.ready_button.clicked.connect(self.start_txt)

		self.setLayout(lay)

	def close_im_panel(self):
		self.stop_button.deleteLater()
		self.chrono_w.deleteLater()
		self.shape_label.deleteLater()
		self.info.deleteLater()
		self.ready_button.deleteLater()

	def start_txt(self):
		self.info.setText("Let's go")

class Window(QMainWindow):
	def _createActions(self):
		# Creating action using the first constructor
		self.newAction = QAction(self)
		self.newAction.setText("&New")
		# Creating actions using the second constructor
		self.openAction = QAction("&Open...", self)
		self.importAction = QAction("&Import...", self)
		self.exitAction = QAction("&Exit", self)
		self.copyAction = QAction("&Copy", self)
		self.pasteAction = QAction("&Paste", self)
		self.cutAction = QAction("C&ut", self)
		self.helpContentAction = QAction("&Help Content", self)
		self.aboutAction = QAction("&About", self)


	def _createMenuBar(self):
		menuBar = self.menuBar()
		# File menu
		fileMenu = QMenu("&File", self)
		menuBar.addMenu(fileMenu)
		fileMenu.addAction(self.newAction)
		fileMenu.addAction(self.openAction)
		fileMenu.addAction(self.importAction)
		fileMenu.addAction(self.exitAction)
		# Edit menu
		editMenu = menuBar.addMenu("&Edit")
		editMenu.addAction(self.copyAction)
		editMenu.addAction(self.pasteAction)
		editMenu.addAction(self.cutAction)
		# Help menu
		helpMenu = menuBar.addMenu("&Help")
		helpMenu.addAction(self.helpContentAction)
		helpMenu.addAction(self.aboutAction)

	def _importCSV(self):
		file1 = open('Figure/Shapes.xlsx', 'r')
		Lines = file1.readlines()
		 
		self.listeClasses = []
		self.listeImgClasses = []
		self.countClasses = 0
		# Strips the newline character
		for line in Lines:
			self.countClasses += 1
			self.listeClasses.append(line.strip().split("\t")[0])
			self.listeImgClasses.append(line.strip().split("\t")[1])

		file1.close()





	def __init__(self, parent = None):
		super(Window, self).__init__( parent )
		self.setWindowTitle("Leka - Interface d'enregistrement")
		self.resize(1280, 720)

		self._createActions()
		self._createMenuBar()
		self._importCSV()
		
		self.lay = QVBoxLayout()
		centralWidget = QWidget()
		centralWidget.setLayout(self.lay)
		self.setCentralWidget(centralWidget)
		self.lay.addWidget(RecordPanel(self.listeClasses))
		#self.lay.addWidget(FilePanel(self.listeClasses))

		self.img_panel = Image_Panel(self)
		self.file_panel = FilePanel(self)
		
		#self.lay.addWidget(file_panel)
		self.lay.addWidget(self.img_panel)


		self.img_panel.stop_button.clicked.connect(self.switch_widget)
	
	def switch_widget(self):
		self.lay.addWidget(self.file_panel)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = Window()
	win.show()
	#classe_1 = FilePanel()
	#classe_1.show()
	sys.exit(app.exec_())
