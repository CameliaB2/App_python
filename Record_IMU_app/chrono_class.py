from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 
from time import sleep
from find_com import *

DURATION_INT = 5

class Chrono_widget(QWidget):
    def __init__(self, name, _rec, _im, _serial, parent=None):
        QWidget.__init__(self, parent=parent)

        self.serial = _serial
        self.rec_panel = _rec
        self.img_panel = _im #ajouté pour stopper le chrono quand on clique sur stop 

        lay = QHBoxLayout(self)

        self.time_record = 60
        self.widget_counter_int = 0
        self.time_per_movement = 1
        self.counter = DURATION_INT

        self.pages_qsw = QtWidgets.QStackedWidget()

        self.chrono_label = QLabel(name, alignment=QtCore.Qt.AlignCenter)
        self.chrono_pic = QPixmap("Ressources/Images/chrono.png")
        self.chrono_pic = self.chrono_pic.scaled(60, 70, QtCore.Qt.KeepAspectRatio)
        
        self.countdown_timer = QtWidgets.QLabel(name, alignment=QtCore.Qt.AlignCenter)
        self.countdown_timer.setFont(QFont('Ressources/Fonts/Poppins', 50, QFont.Bold))
        self.countdown_timer.setStyleSheet("color: rgb(0,0,0)")
        self.chrono_label.setPixmap(self.chrono_pic)

        lay.addWidget(self.chrono_label)
        lay.addWidget(self.countdown_timer)
        lay.addWidget(self.pages_qsw) 

        self.update_gui()

    def countdown(self, txt):
        self.serial.set_SERIAL_SAVING_FLAG(2)
        self.counter = DURATION_INT
        self.FLAG_TIMER = 2
        self.time_decrement = 500 #ms
        
        self.timer_ = QtCore.QTimer(self)
        self.timer_.timeout.connect(lambda:self.timer_timeout(txt))
        self.timer_.start(self.time_decrement)

        self.update_gui()

    def timer_timeout(self, txt):
        if(self.counter > 0):
            self.counter -= self.time_decrement/1000 #to second

        elif(self.counter <= 0 and self.FLAG_TIMER == 2): 
            self.serial.set_SERIAL_SAVING_FLAG(1)
            #self.serial.INDEX_SHAPE = 0
            self.widget_counter_int = (self.widget_counter_int + 1) % 4
            self.pages_qsw.setCurrentIndex(self.widget_counter_int)
            txt.setText("Let's go !")

            self.counter = self.time_record
            self.img_panel.set_name_segment(self.serial.current_file.name_curr_shapes[(self.serial.INDEX_SHAPE+1)%len(self.serial.current_file.name_curr_shapes)])
            self.FLAG_TIMER = 1

        elif(self.counter <= 0 and self.FLAG_TIMER == 1):
            self.rec_panel.panel.l_classRow[self.ID_class].update_gui()
            self.switch_w(True, False)
            self.timer_.stop()
            self.serial.graph.set_graph_flag(0)
            sleep(0.1) #Wait until the last line is waiting
            self.serial.set_SERIAL_SAVING_FLAG(0)
            self.FLAG_TIMER = 0
            #sleep(0.2) #Wait until the last line is waiting
            self.serial.end_recording()
            self.reset_counter()

        self.update_gui()

    def reset_counter(self):
        self.counter = DURATION_INT
        self.serial.set_SERIAL_SAVING_FLAG(0)
        self.img_panel.info.setText("Please press on Ready to start the countdown. The recording will start right after.")


    def setTimeRecord(self, value):
        self.time_record = value

    def setTimeMovement(self, value):
        self.time_per_movement = value

    def update_gui(self):
        self.countdown_timer.setText(str(self.counter))
        if(self.serial.SERIAL_SAVING_FLAG == 1):    #Multiple shape manage
            #print(self.time_record, '-', self.counter, '%', self.time_per_movement, '=', (self.time_record - self.counter) % self.time_per_movement)
            if((self.time_record - self.counter) % self.time_per_movement == 0 and self.time_record != self.counter and self.counter != 0):
                self.serial.INDEX_SHAPE = (self.serial.INDEX_SHAPE+1)%len(self.serial.current_file.name_curr_shapes)
                #if(self.serial.INDEX_SHAPE == len(self.serial.current_file.name_curr_shapes)):
                    #self.serial.INDEX_SHAPE = 0
                    
                #self.img_panel.info.setText("Shape to do: " + self.serial.current_file.name_curr_shapes[self.serial.INDEX_SHAPE])
                self.img_panel.set_name_segment(self.serial.current_file.name_curr_shapes[(self.serial.INDEX_SHAPE+1)%len(self.serial.current_file.name_curr_shapes)])
            self.img_panel.set_name_(self.serial.current_file.name_curr_shapes[self.serial.INDEX_SHAPE])

        if(self.counter <= 5):
            self.countdown_timer.setStyleSheet("color: rgb(255,0,0)")
        elif(self.counter < 10):
            self.countdown_timer.setStyleSheet("color: rgb(255,127,0)")
        else:
            self.countdown_timer.setStyleSheet("color: rgb(0,0,0)")
        

    def set_id(self, ind): #créer la variable globale permet de ne pas prendre en argument img_panel
        self.ID_class = ind

    def switch_w(self, state1, state2):
        self.rec_panel.setVisible(state1)
        self.img_panel.setVisible(state2) 

    def stop_chrono(self):
        self.timer_.stop()

    def start_chrono(self):
        self.timer_.start()

    ID_class = 100 #créer la variable globale permet de ne pas prendre en argument img_panel
    FLAG_TIMER = 3
    INDEX_SHAPE = 0