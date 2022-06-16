from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QGuiApplication
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtNetwork import (QAbstractSocket, QHostAddress, QTcpServer, QTcpSocket)
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 
from file_manager import *
from find_com import *

DURATION_INT = 10
TIME_RECORD = 60

class Chrono_widget(QWidget):
    def __init__(self, name, _rec, _im, _serial, parent=None):
        QWidget.__init__(self, parent=parent)

        lay = QVBoxLayout(self)

        self.widget_counter_int = 0
        self.first_counter = DURATION_INT
        self.second_counter = TIME_RECORD

        self.pages_qsw = QtWidgets.QStackedWidget()
        self.time_passed_qll = QtWidgets.QLabel(name, alignment=QtCore.Qt.AlignCenter)

        self.serial = _serial
        self.serial_flag = _serial.SERIAL_SAVING_FLAG
        self.rec_panel = _rec
        self.img_panel = _im #ajouté pour stopper le chrono quand on clique sur stop 
        
        self.chrono_label = QLabel(name, alignment=QtCore.Qt.AlignCenter)
        self.chrono_pic = QPixmap("Figures/index_.png")
        self.chrono_pic = self.chrono_pic.scaled(100, 121, QtCore.Qt.KeepAspectRatio)
       
        self.time_passed_qll.setFont(QFont('Arial', 22))
        self.chrono_label.setPixmap(self.chrono_pic)

        lay.addWidget(self.chrono_label)
        lay.addWidget(self.time_passed_qll)
        lay.addWidget(self.pages_qsw) 

        self.update_gui()

    def countdown(self, txt):
        self.serial.set_SERIAL_SAVING_FLAG(2)
        self.first_counter = DURATION_INT

        self.timer_ = QtCore.QTimer(self)
        self.timer_.timeout.connect(lambda:self.timer_timeout(txt))
        self.timer_.start(1000)

        self.update_gui()

    def timer_timeout(self, txt):
        if(self.first_counter > 0):
            self.first_counter -= 1

<<<<<<< HEAD
        #mode manuel
=======
>>>>>>> bb4e5d92446d3c0410b830ea5eca518fc6fdd09f
        elif(self.first_counter == 0 and self.FLAG_TIMER == 0): 
            self.serial.set_FLAG_RECORD(1)
            self.serial.set_SERIAL_SAVING_FLAG(1)
            self.widget_counter_int = (self.widget_counter_int + 1) % 4
            self.pages_qsw.setCurrentIndex(self.widget_counter_int)
            txt.setText("Let's go !")

            self.first_counter = TIME_RECORD
            self.FLAG_TIMER = 1
<<<<<<< HEAD
        
=======

>>>>>>> bb4e5d92446d3c0410b830ea5eca518fc6fdd09f
        elif(self.first_counter == 0 and self.FLAG_TIMER == 1):
            self.rec_panel.panel.l_classRow[self.ID_class].update_gui()
            self.switch_w(True, False)
            self.timer_.stop()
            self.serial.set_FLAG_RECORD(0)
            self.serial.graph.set_graph_flag(0)
            self.serial.set_SERIAL_SAVING_FLAG(0)
            self.serial_flag = self.serial.SERIAL_SAVING_FLAG #il vaut bien 0
            self.FLAG_TIMER = 0

        self.update_gui()

<<<<<<< HEAD
    def update_gui(self):
        self.time_passed_qll.setText(str(self.first_counter))

    def get_id(self, ind): #créer la variable globale permet de ne pas prendre en argument img_panel
=======

    def update_gui(self):
        self.time_passed_qll.setText(str(self.first_counter))

    def set_id(self, ind): #créer la variable globale permet de ne pas prendre en argument img_panel
>>>>>>> bb4e5d92446d3c0410b830ea5eca518fc6fdd09f
        self.ID_class = ind

    def switch_w(self, state1, state2):
        self.rec_panel.setVisible(state1)
        self.img_panel.setVisible(state2) 

    def stop_chrono(self):
        self.timer_.stop()
<<<<<<< HEAD
        

    file = "" 
    ID_class = 100 #créer la variable globale permet de ne pas prendre en argument img_panel
    FLAG_TIMER = 0
    
    
=======

    def start_chrono(self):
        self.timer_.start()

    file = "" 
    ID_class = 100 #créer la variable globale permet de ne pas prendre en argument img_panel
    FLAG_TIMER = 0
>>>>>>> bb4e5d92446d3c0410b830ea5eca518fc6fdd09f
