import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import *
import pyqtgraph as pg
import file_manager as fm
from graph import *



class Status_bar(QMainWindow):
   def __init__(self, parent = None):
      super(Status_bar, self).__init__(parent)
        
      self.statusBar = QStatusBar()
      self.setStatusBar(self.statusBar)

class Tabs(QWidget):
    def __init__(self, parent = None):
        super(Tabs, self).__init__(parent)


        self.composantes_to_show = ["Acc_X", "Acc_Y", "Acc_Z", "Gyr_X", "Gyr_Y", "Gyr_Z"]
        self.type_data_to_show = ["Raw_Data", "Average_4_Data", "Average_8_Data", "Average_16_Data", "Delta_Data"]
        self.data = [[], [], [], [], []]
        self.current_composante = 0

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

        self.setLayout(self.main_layout)



    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "CSV Files (*.csv);; TXT Files(*.txt)", options=options)
        if fileName:
            self.file_name_lineE.setText("File name: " + fileName.split("/")[-1])
            self.data[0] = fm.read_file(fileName)

            fileName = fileName.replace('.csv', '-average-Range_4.csv')
            self.data[1] = fm.read_file(fileName)

            for i in range(6):  
                for j in range(3):  self.data[1][i].insert(0, 0)

            fileName = fileName.replace('4.csv', '8.csv')
            self.data[2] = fm.read_file(fileName)
            for i in range(6):  
                for j in range(7):  self.data[2][i].insert(0, 0)

            fileName = fileName.replace('8.csv', '16.csv')
            self.data[3] = fm.read_file(fileName)
            for i in range(4):  
                for j in range(15):  self.data[3][i].insert(0, 0)

            self.init_infos()

    def init_infos(self):
        self.checkbox_data_obj[0].setChecked(True) #Raw Data True by default
        for obj in self.checkbox_data_obj:
            obj.setEnabled(True)

        self.create_bottom_bar()     
        self.main_layout.addLayout(self.toolbar_bot_layout)

    def create_title_line(self):
        self.title_layout = QHBoxLayout()

        self.title = QLabel("Données de l'IMU LSM6DSOX", alignment=Qt.AlignCenter)
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
        self.reset_view_button.setObjectName("Reset_view")

        self.layout_left_panel.addWidget(self.composantes_lineE)
        self.layout_left_panel.addWidget(self.combo_composantes)
        self.layout_left_panel.addLayout(self.checkbox_layout)
        self.layout_left_panel.addWidget(self.reset_view_button)


    def create_import_line(self):
        self.layout_import = QHBoxLayout()
        self.import_button = QPushButton("Import")
        self.import_button.setObjectName("Import")
        self.import_button.setMaximumWidth(75)
        self.file_name_lineE = QLabel("File name: No_File")
        self.file_name_lineE.setMaximumWidth(400)
        self.file_name_lineE.setObjectName("Info")
        self.import_button.clicked.connect(self.openFileNameDialog)

        self.layout_import.addWidget(self.import_button)
        self.layout_import.addWidget(self.file_name_lineE)


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

    def create_bottom_bar(self):
        self.toolbar_bot_layout = QHBoxLayout()
        nbr_samples = len(self.data[0][self.current_composante]) #0 because raw data is the first file reading
        self.sample_nbr_lineE = QLabel("Samples number: " + str(nbr_samples), alignment=Qt.AlignCenter) 
        self.time_record_lineE = QLabel("Time Recording: " + str(round(nbr_samples*1/26,2)) + "s", alignment=Qt.AlignCenter) 
        self.ODR_lineE = QLabel("ODR Recording: " + "26Hz", alignment=Qt.AlignCenter) 
        self.sample_nbr_lineE.setObjectName("Info")
        self.time_record_lineE.setObjectName("Info")
        self.ODR_lineE.setObjectName("Info")
        self.toolbar_bot_layout.addWidget(self.sample_nbr_lineE)
        self.toolbar_bot_layout.addWidget(self.time_record_lineE)
        self.toolbar_bot_layout.addWidget(self.ODR_lineE)

    def set_current_composante(self):
            self.current_composante = self.combo_composantes.currentIndex()
            if(self.current_composante < 3):
                self.graph.update_graph_parameters("Acceleration", "Acceleration (mg)", "Time (*1/26 s)")
            else:
                self.graph.update_graph_parameters("Gyroscope", "Angular Velocity (dps)", "Time (*1/26 s)")

            for i in range(len(self.type_data_to_show)):
                self.graph.update_graph(i, self.current_composante)
    


    

class Window(QMainWindow):


    def __init__(self, parent = None):
        super(Window, self).__init__( parent )
        self.setWindowTitle("Leka - Outil de visualisation des Logs")

        self.table_widget = Tabs(self)
        self.setCentralWidget(self.table_widget)
        self._createActions()
        self._createMenuBar()
        self.exitAction.triggered.connect(self.closeAll)
        self.statusBar().showMessage('V-1.0.0')
        
        self.show()

    def _createActions(self):
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

        # Help menu
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.closeAll()

    def closeEvent(self, event):
        if self.closeAll():
            event.Accept()
        else:
            event.ignore()

    def closeAll(self):
        close = QMessageBox.question(self, "QUIT", "Are you sure want to stop process?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            quit()
            return true
        return False



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
    margin: 25px;
}   
QLabel#Subtitle {
    color: black;
    font-weight: bold;
    font-size: 16px;
    max-height: 35px;
    border-radius: 5px;
    margin-top: 30px;
}  
QLabel#Info {
    color: black;
    font-weight: bold;
}  
QPushButton {
    font-family: Ressources/Fonts/Poppins;
}

QPushButton#Import {
    background-color: orange;
    color: white;
    border: solid 3px black;
    border-radius: 5px;
    height: 30px;

}
QPushButton#Icon {
    color: black;
    border-radius: 5px;
}
QPushButton#Reset_view{
    background-color: green;
    color: white;
    border: solid 3px black;
    border-radius: 5px;
    height: 30px;
    margin-top: 30px;
}

QCheckBox{
    color: black;
    margin-left: 15%;
}
QComboBox{
    color: black;
    margin-left: 15%;
}
QComboBox::drop-down{
    margin-right: 30%;
}
QLabel, QComboBox, QLineEdit
{
   background-position: center;
}
"""

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    app.setStyleSheet(CSS)
    win.showMaximized()
    sys.exit(app.exec())