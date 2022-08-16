from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 
from find_com import *

img_panel = ''
rec_panel = ''

class ClassRow(QWidget):
    def __init__(self, _data=None, _name=None, serial=None, _id=None, _file=None, parent=None):
        super(ClassRow, self).__init__( parent )

        lay = QHBoxLayout(self)  

        global img_panel, rec_panel
        
        self.id = _id
        self.name = _name
        self.file = _file
        self.ser = serial
        self.suffix = ""
        self.data = _data

        self.class_name_text = self.create_className(self.name, 'The name of the class to record', 'white')
        self.textbox = self.create_inputField('white', 'Write a suffix which will be added at the end of the filename')

        self.record_filename_text = QLabel("Unregistered", alignment=QtCore.Qt.AlignCenter)
        self.record_filename_text.setToolTip("Name will be : 'Date-Shape-suffix.csv'")
        
        self.record_button = self.create_button('REC', 'Ressources/Images/rec_logo.png', 'white', 'Press the button to launch the recording', 'Icon')
        self.status_button = self.create_button('', 'Ressources/Images/check.png', 'lightgray', 'Pass to the color green if the recording is successfull', '')
        self.clear_recording_button = self.create_button('', 'Ressources/Images/restart.png', 'blue', 'This button is for deleting the following recording and start another one', 'Icon')
        self.delete_line_button = self.create_button('', 'Ressources/Images/cross.png', 'red', 'This button is for deleting this line', 'Icon')


        lay.setSpacing(70)        
        lay.addWidget(self.set_size(self.class_name_text,160,30))
        lay.addWidget(self.set_size(self.textbox,65,30))
        lay.addWidget(self.set_size(self.record_filename_text, 350, 30))
        lay.addWidget(self.set_size(self.record_button, 150, 30))
        lay.addWidget(self.set_size(self.status_button,70, 30))
        lay.addWidget(self.set_size(self.clear_recording_button, 70, 30))
        lay.addWidget(self.set_size(self.delete_line_button, 70, 30))

        self.record_button.clicked.connect(self._record_button_clicked)
        self.delete_line_button.clicked.connect(lambda:self.msg_box("Are you sure you want to delete this line ?", self.id))        
        self.clear_recording_button.clicked.connect(self._clear_recording_button_clicked)
        

    def create_className(self, _text, _text_info, _bg):
        label = QLabel(_text, alignment=QtCore.Qt.AlignCenter)
        label.setToolTip(_text_info)
        #label.setStyleSheet("background-color: " + _bg)
        return label

    def create_button(self, _text, _icon, _bg, _text_info, _id):
        btn = QPushButton(_text)
        btn.setIcon(QIcon(_icon))
        btn.setToolTip(_text_info)
        btn.setObjectName(_id)
        btn.setStyleSheet("background-color: " + _bg)
        return btn

    def create_inputField(self, _bg, _text_info):
        inputField = QLineEdit(self)
        inputField.move(20, 20)
        inputField.resize(40,40)
        inputField.setStyleSheet("background-color: " + _bg)
        inputField.setToolTip(_text_info)
        return inputField

    def _record_button_clicked(self):
        self.record_button.setEnabled(False)
        img_panel.chrono_w.set_id(self.id)
        self.switch_w(False,True)
        self.get_suffix()
        self.set_name()
        #appel de la fonction set_current_shapes uniquement si la shape est composite True
        self.file.set_current_shapes(self.data, self.name)
        files_name = self.generate_files_name()
        self.record_filename_text.setText(files_name)

        img_panel.ready_button.setEnabled(True)
        img_panel.setNext()

    def generate_files_name(self):
        size = len(self.file.name_curr_shapes)
        files_name = ''
        for i in range(size):
            if(size == 1):
                files_name += self.get_name_file(self.file.name_curr_shapes[0])
            elif(i == size-1):
                files_name += self.get_name_file(self.file.name_curr_shapes[i])
            else:
                files_name += self.get_name_file(self.file.name_curr_shapes[i]) + "\n"
        return files_name

    def _clear_recording_button_clicked(self):
        self.record_button.setEnabled(True)
        self.record_filename_text.setText('Unregistered')
        self.status_button.setStyleSheet("background-color: lightgray")
        #self.get_suffix()
        #self.file.set_current_shapes(self.name) #Pourquoi on utilise ça
        self.file.remove_file()
        self.ser.set_SERIAL_SAVING_FLAG(0)
        self.ser.set_headline_flag(False)

    def get_suffix(self):
        self.suffix = self.textbox.text()
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

        #Doublon avec file_manager, à refaire
    def get_name_file(self, _name):
        if(self.suffix != ""):
            file_name_ = self.generate_date() + "-"  + self.ser.odr_freq + "-" + _name + "-" + self.suffix + ".csv"
        else:
            file_name_ = self.generate_date() + "-"  + self.ser.odr_freq + "-" + _name + ".csv"
        return file_name_


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
        date = now.strftime("%Y_%m_%d-%H_%M_%S")
        return str(date)

    
def set_img_panel(val):
    global img_panel
    img_panel = val

def set_rec_panel(val):
    global rec_panel
    rec_panel = val