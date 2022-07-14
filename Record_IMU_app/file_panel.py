from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 

from classe_line import ClassRow


class FilePanel(QWidget):
    def __init__(self, _ser, _file, _data, parent = None):
        super(FilePanel, self).__init__( parent )

        self.lay = QVBoxLayout()  
        self.lay.setAlignment(Qt.AlignTop)

        self.file = _file
        self.ser = _ser
        self.id = 0
        self.classR = ''
        self.data = _data
    

        self.setLayout(self.lay)


    def add_item(self, _name):
        self.classR = ClassRow(self.data, _name, self.ser, self.id, self.file)
        self.l_classRow.append(self.classR)
        self.lay.addWidget(self.l_classRow[-1])
        self.id += 1

    def remove_line(self, _id):
        self.l_classRow[_id].deleteLater()

    def remove_all_lines(self):
        self.tab = self.l_classRow
        for i in range(len(self.tab)):
            self.tab[i].deleteLater()


    l_classRow = []
    tab = []
    _name = ''