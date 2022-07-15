import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from graph import *
import os.path

class Page_graph(QWidget):
    def __init__(self, _tabs, _tab_array, _id, parent = None):
        super(Page_graph, self).__init__(parent)
        self.tab_array = _tab_array
        self.id = _id
        self.tabs = _tabs

        self.composantes_to_show = ["Acc_X", "Acc_Y", "Acc_Z", "Gyr_X", "Gyr_Y", "Gyr_Z"]
        self.type_data_to_show = ["Raw_Data", "Average_4_Data", "Average_8_Data", "Average_16_Data", "Delta_Data"]
        self.data = [[] for i in range(len(self.composantes_to_show))]
        self.is_file_exist = [False for i in range(len(self.type_data_to_show))]
        self.current_composante = 0
        self.name_tab = "Page " + str(_id)

        self.create_title_line()
        self.create_left_panel()
        self.create_import_line()
        self.graph = Graph(type_data_to_show = self.type_data_to_show, 
                           data = self.data,
                           checkbox_data_obj = self.checkbox_data_obj)

        self.reset_view_button.clicked.connect(self.graph.reset_view)

        self.main_layout = QVBoxLayout()       
        self.main_layout.addLayout(self.title_layout)
        self.main_layout.addLayout(self.layout_import)
        self.panel = QHBoxLayout()
        self.panel.addLayout(self.layout_left_panel)
        self.panel.addWidget(self.graph)
        self.main_layout.addLayout(self.panel)
        self.create_bottom_bar()     
        self.main_layout.addLayout(self.toolbar_bot_layout)

        self.setLayout(self.main_layout)


    def set_tab_id(self, _id):
        self.id = _id

    def openFileNameDialog(self):
        path = self.read_preferences_path()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", path, "CSV Files (*.csv);; TXT Files(*.txt)", options=options)
        if fileName:
            self.reset_file_exist()
            self.file_name_lineE.setText("File name: " + fileName.split("/")[-1])
            self.write_path_file(fileName.replace(fileName.split("/")[-1], ''))
            self.data[0] = fm.read_file(fileName)
            self.is_file_exist[0] = True
            self.set_tab_name(fileName)

            fileName = fileName.replace('.csv', '-average-Range_4.csv')
            if(os.path.exists(fileName)):
                self.data[1] = fm.read_file(fileName)
                self.is_file_exist[1] = True
                for i in range(6):  
                    for j in range(3):  self.data[1][i].insert(0, 0)

            fileName = fileName.replace('4.csv', '8.csv')
            if(os.path.exists(fileName)):
                self.data[2] = fm.read_file(fileName)
                self.is_file_exist[2] = True
                for i in range(6):  
                    for j in range(7):  self.data[2][i].insert(0, 0)

            fileName = fileName.replace('8.csv', '16.csv')
            if(os.path.exists(fileName)):
                self.data[3] = fm.read_file(fileName)
                self.is_file_exist[3] = True
                for i in range(4):  
                    for j in range(15):  self.data[3][i].insert(0, 0)

            self.init_infos()
            self.set_current_composante()

    def read_preferences_path(self):
        f = open("config.json", "r")
        if(f.read() == 'to_define'):
            str_desktop_path = os.path.realpath(__file__)
            str_desktop_path = str_desktop_path.replace('page_graph.py', 'Logs')
            self.write_path_file(str_desktop_path)
            f.close()
        f = open("config.json", "r")
        path = f.read()
        f.close()
        return path

    def write_path_file(self, _dir):
        f = open("config.json", "w")
        f.write(_dir)
        f.close()

    def reset_file_exist(self):
        self.is_file_exist = [False for i in range(len(self.type_data_to_show))]

    def set_tab_name(self, fileName):
        fn_split = fileName.split('-')
        if(len(fn_split) > 2):
            for i in range(len(self.tab_array)):
                if(self.tab_array[i].id == self.id):
                    if(isinstance(fn_split[2], str)):
                        if(isinstance(fn_split[3], str)):
                            self.name_tab = fn_split[2] + '-' + fn_split[3]
                        else:
                            self.name_tab = fn_split[2]
                        self.tabs.setTabText(i, self.name_tab)

    def remove_tab(self):
        if(len(self.tab_array)>1):
            for i in range(len(self.tab_array)):
                if(self.tab_array[i].id == self.id):
                    close = QMessageBox.question(self, "Remove Page", \
                                "Are you sure want to remove the page entitled: " + self.name_tab + " ?"\
                                , QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    if close == QtWidgets.QMessageBox.Yes:
                        self.tabs.removeTab(i)
                        self.tab_array.pop(i)
                        return True
                    return False
        close = QMessageBox.information(self, "Remove Page", "You can't remove this page if you have juste one page.", QtWidgets.QMessageBox.Ok)


    def init_infos(self):
        self.checkbox_data_obj[0].setChecked(True) #Raw Data True by default
        for obj in self.checkbox_data_obj:
            obj.setEnabled(True)

        self.update_bottom_bar()
        self.set_checkbox_state() 

    def create_title_line(self):
        self.title_layout = QHBoxLayout()

        self.title = QLabel("IMU LSM6DSOX - Data Logs", alignment=Qt.AlignCenter)
        self.title.setObjectName("Title")
        self.title_layout.addWidget(self.title)


    def create_left_panel(self):
        self.layout_left_panel = QVBoxLayout()
        self.layout_left_panel.setAlignment(Qt.AlignCenter)
        self.layout_left_panel.setObjectName("Left_panel")

        self.composantes_lineE = QLabel("Composantes", alignment=Qt.AlignLeft)
        self.composantes_lineE.setObjectName("Subtitle")
        self.combo_composantes = QComboBox(self)
        self.combo_composantes.setFixedWidth(100)


        for composante in self.composantes_to_show:
            self.combo_composantes.addItem(composante)

        self.combo_composantes.activated.connect(self.set_current_composante)

        self.create_data_to_show_checkbox()

        self.reset_view_button = QPushButton("Reset Graph View")        
        self.reset_view_button.setToolTip("Reset the graph's view")

        self.reset_view_button.setObjectName("Reset_view")

        self.rm_tab_button = QPushButton("Remove Page")
        self.rm_tab_button.setToolTip("Remove the current page")
        self.rm_tab_button.setObjectName("Delete")
        self.rm_tab_button.clicked.connect(self.remove_tab)

        self.layout_left_panel.addWidget(self.composantes_lineE)
        self.layout_left_panel.addWidget(self.combo_composantes)
        self.layout_left_panel.addLayout(self.checkbox_layout)
        self.layout_left_panel.addWidget(self.reset_view_button)
        self.layout_left_panel.addWidget(self.rm_tab_button)


    def create_import_line(self):
        self.layout_import = QHBoxLayout()
        self.import_button = QPushButton("Import")
        self.import_button.setToolTip("Import the file to show")
        self.import_button.setObjectName("Import")
        self.import_button.setMinimumWidth(100)
        self.file_name_lineE = QLabel("File name: No_File")
        self.file_name_lineE.setMinimumWidth(400)
        self.file_name_lineE.setObjectName("Info")
        self.import_button.clicked.connect(self.openFileNameDialog)

        self.layout_import.addWidget(self.import_button, alignment=Qt.AlignRight)
        self.layout_import.addWidget(self.file_name_lineE, alignment=Qt.AlignLeft)


    def create_data_to_show_checkbox(self):
        self.checkbox_layout = QVBoxLayout()
        self.dataType_lineE = QLabel("Type Data", alignment=Qt.AlignLeft)
        self.dataType_lineE.setObjectName("Subtitle")
        self.checkbox_layout.addWidget(self.dataType_lineE)

        checkbox_name = ["Raw Data", "Average 4", "Average 8", "Average 16", "Delta"]
        self.checkbox_data_obj = []
        for i in range(len(checkbox_name)):
            self.checkbox_data_obj.append(QCheckBox(checkbox_name[i]))
            self.checkbox_data_obj[-1].stateChanged.connect(lambda x=1, n=i: self.graph.update_graph(n, self.current_composante)) 
            self.checkbox_data_obj[-1].setEnabled(False)
            self.checkbox_layout.addWidget(self.checkbox_data_obj[-1])

    def set_checkbox_state(self):
        for i in range(len(self.checkbox_data_obj)):
            self.checkbox_data_obj[i].setEnabled(self.is_file_exist[i])

        
    def create_bottom_bar(self):
        self.toolbar_bot_layout = QHBoxLayout()
        self.sample_nbr_lineE = QLabel("Samples number: ", alignment=Qt.AlignCenter) 
        self.time_record_lineE = QLabel("Time Recording: 0s", alignment=Qt.AlignCenter) 
        self.ODR_lineE = QLabel("ODR Recording: 0Hz", alignment=Qt.AlignCenter) 
        self.sample_nbr_lineE.setObjectName("Info")
        self.time_record_lineE.setObjectName("Info")
        self.ODR_lineE.setObjectName("Info")

        self.toolbar_bot_layout.addWidget(self.sample_nbr_lineE)
        self.toolbar_bot_layout.addWidget(self.time_record_lineE)
        self.toolbar_bot_layout.addWidget(self.ODR_lineE)

    def update_bottom_bar(self):
        nbr_samples = len(self.data[0][self.current_composante]) #0 because raw data is the first file reading
        self.sample_nbr_lineE.setText("Samples number: " + str(nbr_samples))
        self.time_record_lineE.setText("Time Recording: " + str(round(nbr_samples*1/26,2)) + "s")
        self.ODR_lineE.setText("ODR Recording: " + "26Hz") 

    def set_current_composante(self):
            self.current_composante = self.combo_composantes.currentIndex()
            if(self.current_composante < 3):
                self.graph.update_graph_parameters("Acceleration", "Acceleration (mg)", "Time (*1/26 s)")
            else:
                self.graph.update_graph_parameters("Gyroscope", "Angular Velocity (dps)", "Time (*1/26 s)")

            for i in range(len(self.type_data_to_show)):
                self.graph.update_graph(i, self.current_composante)
    