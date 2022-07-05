import sys
import threading
#from numpy.lib import recfunctions as rfn

from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import *
import yaml
from yaml.loader import SafeLoader

from classe_line import *
from find_com import *

from file_manager import *
from record_panel import *
from file_panel import *
from image_panel import *
from preferences import *


class Window(QMainWindow):
	def __init__(self, parent = None):
		super(Window, self).__init__( parent )
		self.setWindowTitle("Leka - Interface d'enregistrement")

		"""
		self.logo_label = QLabel("Logo_label", alignment=QtCore.Qt.AlignRight)
		self.logo_pic = QPixmap("Ressources/Images/leka_logo.png")
		self.logo_pic = self.logo_pic.scaled(100, 72, QtCore.Qt.KeepAspectRatio)
		self.logo_label.setPixmap(self.logo_pic)
		self.logo_label.setFixedHeight(100)
		"""
		self.current_file = File_manager()

		self._createActions()
		self._createMenuBar()
		#self._importCSV()
		self._importYAML()
		self.ser = Serial_COM(self.current_file, self.findPorts)
		
		self.preference_onglet = Preferences(self.current_file)
		self.preferences.triggered.connect(self.preference_onglet.show_preferences)
		self.exitAction.triggered.connect(self.closeAll)


		#Thread de serial
		self.ser.set_SERIAL_SAVING_FLAG(0) #initialisation à 0 obligatoire ?
		
		self.imu_data_thr = threading.Thread(target=self.ser.thread_run, args=())
		self.imu_data_thr.start()
		
		self.rec_pan = RecordPanel(self.ser, self.listeAllClasses, self.current_file)
		self.img_pan = Image_Panel(self.rec_pan, self.ser)
		#Pour contrer le str object has no attribute blabla dans classRow
		set_img_panel(self.img_pan)
		set_rec_panel(self.rec_pan)
		
		

		self.lay = QVBoxLayout()
		centralWidget = QWidget()
		centralWidget.setLayout(self.lay)
		self.setCentralWidget(centralWidget)

		
		self.lay.setSpacing(0) 
		#self.lay.addWidget(self.logo_label)
		self.lay.addWidget(self.img_pan)
		self.lay.addWidget(self.rec_pan)
		self.rec_pan.setVisible(True)
		self.img_pan.setVisible(False)
		self.generate_classes()
	

	def update_port_menu(self):
		self.findPorts.clear()
		for row, port in enumerate(self.ser.get_list_ports(), 1):
			recent_action = self.findPorts.addAction('&{}. {}'.format(
				row, port))
			recent_action.setData(port)
			recent_action.triggered.connect(lambda x=1, n=port: self.ser.change_port(n))

	def _createActions(self):
		# Creating action using the first constructor
		# Creating actions using the second constructor
		self.preferences = QAction("&Preferences...", self)
		self.exitAction = QAction("&Exit", self)

		self.helpContentAction = QAction("&Help Content", self)
		self.aboutAction = QAction("&About", self)


	def _createMenuBar(self):
		menuBar = self.menuBar()
		# File menu
		fileMenu = QMenu("&File", self)
		menuBar.addMenu(fileMenu)
		fileMenu.addAction(self.preferences)
		fileMenu.addAction(self.exitAction)
		# Edit menu
		toolsMenu = menuBar.addMenu("&Tools")
		self.findPorts = toolsMenu.addMenu("PORT:")
		self.findPorts.setStatusTip('Choose the card\'s port')

		self.findPorts.aboutToShow.connect(self.update_port_menu)
		self.settings = {}

		# Help menu
		helpMenu = menuBar.addMenu("&Help")
		helpMenu.addAction(self.helpContentAction)
		helpMenu.addAction(self.aboutAction)

	def generate_classes(self):
		self.formatbar = QToolBar(self)
		self.addToolBar(Qt.TopToolBarArea, self.formatbar)

		for e in self.listeAllClasses:
			toolButton = QToolButton(self)
			toolButton.setIcon(QtGui.QIcon('Ressources/Classes/Images/' + e + '.png'))
			toolButton.setToolTip(e)
			toolButton.clicked.connect(lambda x=1, n=e: self.rec_pan.panel.add_item(n))
			self.formatbar.addWidget(toolButton)


	def _importCSV(self):
		file1 = open('Ressources/Classes/class_list.csv', 'r')
		Lines = file1.readlines()
		 
		self.listeClasses = []
		self.listeImgClasses = []
		self.countClasses = 0
		# Strips the newline character
		for line in Lines:
			self.countClasses += 1
			self.listeClasses.append(line.strip().split("\t")[0])
			print(self.listeClasses)
			
		file1.close()


	def _importYAML(self):
		file1 = open('Ressources/Classes/class_list.yml', 'r')
		data = yaml.load(file1, Loader=SafeLoader)
		self.listePureClasses = []
		self.listeComplexClasses = []
		self.listeAllClasses = []
		self.listeImgClasses = []
		self.countClasses = 0

		for line in data['Classes']:
			self.countClasses += 1
			if(data['Classes'][line]['composite'] is False):
				self.listePureClasses.append(line)
				
			else :
				self.listeComplexClasses.append(line)
		self.listeAllClasses = self.listePureClasses + self.listeComplexClasses
		print("Pure classes")
		print(self.listePureClasses)
		print("Complex classes")
		print(self.listeComplexClasses)
		print("All classes")
		print(self.listeAllClasses)
		
			

		file1.close()

		


	def msg_box(self, text):
		msg = QMessageBox()
		msg.setText(text)
		msg.setIcon(QMessageBox.Question)
		msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes) # seperate buttons with "|"
		#msg.buttonClicked.connect(lambda:self.switch_widget(True, False))
		result = msg.exec_()
		if result == QMessageBox.Yes:
			switch_widget(True, False)
		else:
			msg.done(1)


	def keyPressEvent(self, e):
		if e.key() == Qt.Key_Escape:
			self.closeAll()

	def closeEvent(self, event):
		if self.closeAll():
			#Stop all threads
			event.Accept()
		else:
			event.ignore()

	def closeAll(self):
		close = QtWidgets.QMessageBox.question(self, "QUIT", "Are you sure want to stop process?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if close == QtWidgets.QMessageBox.Yes:
			self.close_thread_app()
			self.close_windows()	
			quit()
			return true
		return False

	def close_thread_app(self):
		self.ser.get_data_imu_thread_stop()
		self.ser.search_usb_thread_stop()
		self.ser.graph.update_graph_thread_stop()
	
	def close_windows(self):
		self.preference_onglet.close_preferences()

def switch_widget(state1, state2):
	self.rec_pan.setVisible(state1)
	self.formatbar.setVisible(state1)
	self.img_pan.setVisible(state2)
	if(state1):
		self.img_pan.ready_button.setEnabled(True)

CSS = """
QLabel {
	color: black;
	font-family: Ressources/Fonts/Poppins;
}
QLabel#Title {
	color: white;
	font-size: 22px;
	border: 3px ridge #6da026 ;
	max-height: 35px;
	border-radius: 5px;
	background: #75B222;
	margin: 50px;
}	
QPushButton {
	font-family: Ressources/Fonts/Poppins;
}

QPushButton#White {
	color: white;
	border: solid 3px black;
	border-radius: 5px;
}
QPushButton#Icon {
	color: black;
	border-radius: 5px;
}
#Header {
	background: black;
}

"""

if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = Window()
	app.setStyleSheet(CSS)
	win.showMaximized()
	sys.exit(app.exec())
