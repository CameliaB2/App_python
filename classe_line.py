from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QGuiApplication
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtNetwork import (QAbstractSocket, QHostAddress, QTcpServer,
                               QTcpSocket)

from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 
from find_com import *

img_panel = ''
rec_panel = ''

class ClassRow(QWidget):
    def __init__(self, _name=None, _serial=None, _id=None, _file=None, parent=None):
        super(ClassRow, self).__init__( parent )

        lay = QHBoxLayout(self)  

        global img_panel, rec_panel
        
        """self.img_pan = ""
        self.rec_pan = """""

        self.id = _id

        self.class_name_text = QLabel(_name, alignment=QtCore.Qt.AlignCenter)

        self.record_button = QPushButton("REC")        
        self.record_button.setIcon(QIcon('Figures/logo.png'))
        self.record_filename_text = QLabel("Unregistered", alignment=QtCore.Qt.AlignCenter)

        self.status_button = QPushButton("")
        self.status_button.setStyleSheet("background-color: lightgray")
        self.status_button.setIcon(QIcon('Figures/check.png'))

        self.clear_recording_button = QPushButton("")
        self.clear_recording_button.setStyleSheet("background-color: blue")
        self.clear_recording_button.setIcon(QIcon('Figures/restart.png'))
        self.clear_recording_button.setToolTip('This button is for deleting the following recording and start another one')
        

        self.delete_line_button = QPushButton("")
        self.delete_line_button.setIcon(QIcon('Figures/cross.png'))
        self.setStyleSheet(" QToolTip{ border: 1px solid white; background-color: white ; color: k ; font: 12pt}")
        self.delete_line_button.setToolTip('This button is for deleting this line')
        self.delete_line_button.setStyleSheet("background-color: red")
        
        self.name = _name
        self.file = _file
        self._ser = _serial

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(40,40)

        self.suffix = ""


        lay.setSpacing(70)        
        lay.addWidget(self.set_size(self.class_name_text,160,30))
        lay.addWidget(self.set_size(self.textbox,65,30))
        lay.addWidget(self.set_size(self.record_filename_text, 300, 30))
        lay.addWidget(self.set_size(self.record_button, 150, 30))
        lay.addWidget(self.set_size(self.status_button,70, 30))
        lay.addWidget(self.set_size(self.clear_recording_button, 70, 30))
        lay.addWidget(self.set_size(self.delete_line_button, 70, 30))

        self.record_button.clicked.connect(self._record_button_clicked)

        self.delete_line_button.clicked.connect(lambda:self.msg_box("Are you sure you want to delete this line ?", self.id))
        
        self.clear_recording_button.clicked.connect(self._clear_recording_button_clicked)
        
        
    def _record_button_clicked(self):
        self.record_button.setEnabled(False)
        self.set_name()
        img_panel.chrono_w.set_id(self.id)
        self.get_suffix()
        self.switch_w(False,True)
        self.file.set_current_shape(self.name)
        self.update_name()
        img_panel.ready_button.setEnabled(True)
        

    def _clear_recording_button_clicked(self):
        self.record_button.setEnabled(True)
        self.status_button.setStyleSheet("background-color: lightgray")
        self.get_suffix()
        self.file.set_current_shape(self.name)
        self.file.remove_file()
        self._ser.set_SERIAL_SAVING_FLAG(0)
        self._ser.set_headline_flag(False)
        #print(self._ser.headline_write) 

    def get_suffix(self):
        self.suffix = self.textbox.text()
        #print(self.suffix)
        self.file.set_suffix(self.suffix)


    def set_size(self, obj, width, height):
        obj.setFixedWidth(width)		
        obj.setFixedHeight(height)
        return obj


    def set_name(self):
        img_panel.set_name_(self.name)
        

    def switch_w(self, state1, state2):
        rec_panel.setVisible(state1)
        img_panel.setVisible(state2)
    
    def update_name(self):
        file_name_ = self.generate_date() + self.name + "-" + self.suffix + ".csv"
        self.record_filename_text.setText(file_name_)


    def msg_box(self, text, _id):
        msg = QMessageBox()
        msg.setText(text)
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes) # seperate buttons with "|"
        result = msg.exec_()
        if result == QMessageBox.Yes:
            #Supprimer la ligne
            rec_panel.panel.remove_line(_id)
        else:
            msg.done(1)


    def update_gui(self):
        self.status_button.setStyleSheet("background-color: green")

    def generate_date(self):
        now = datetime.now()
        date = now.strftime("%Y_%m_%d-%H_%M_%S-")
        return str(date)

    
def set_img_panel(val):
    global img_panel
    img_panel = val
    print(img_panel)

def set_rec_panel(val):
    global rec_panel
    rec_panel = val
    print(rec_panel)