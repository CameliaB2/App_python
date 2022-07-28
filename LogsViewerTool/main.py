import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import *
from page_graph import *

VERSION = 'V-1.1.0'


class Status_bar(QMainWindow):
   def __init__(self, parent = None):
      super(Status_bar, self).__init__(parent)
        
      self.statusBar = QStatusBar()
      self.setStatusBar(self.statusBar)


class Window(QMainWindow):
    def __init__(self, parent = None):
        super(Window, self).__init__( parent )
        self.setWindowTitle("Leka - Logs Viewer Tool")

        self.tabs = QTabWidget()
        self.nbr_tabs = 1

        self.tab_array = []

        self.add_tab_button = QPushButton("Add page")     
        self.add_tab_button.setObjectName("Add_button")  
        self.add_tab_button.setToolTip("Add a page where you can import a file") 
        self.add_tab_button.clicked.connect(self.add_tab)
        self.tabs.setCornerWidget(self.add_tab_button)

        self._createActions()
        self._createMenuBar()
        self.exitAction.triggered.connect(self.closeAll)
        self.statusBar().showMessage(VERSION)
        self.setCentralWidget(self.tabs)

        self.add_tab()

    def add_tab(self):
        self.tab_array.append(QWidget())

        interface = Page_graph(self.tabs, self.tab_array, self.nbr_tabs)
        self.tab_array[-1].id = self.nbr_tabs
        self.tab_array[-1].setLayout(interface.main_layout)

        self.tabs.addTab(self.tab_array[-1], "Page " + str(self.nbr_tabs))
        self.nbr_tabs += 1

    def _createActions(self):
        #self.preferences = QAction("&Preferences...", self)
        self.exitAction = QAction("&Exit", self)

        #self.helpContentAction = QAction("&Help Content", self)
        #self.aboutAction = QAction("&About", self)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # File menu
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        #fileMenu.addAction(self.preferences)
        fileMenu.addAction(self.exitAction)

        # Help menu
        """
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)
        """
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.closeAll()

    def closeEvent(self, event):
        if self.closeAll():
            event.Accept()
        else:
            event.ignore()

    def closeAll(self):
        close = QMessageBox.question(self, "QUIT", "Are you sure want to stop process ?\nYou will lose you current analyzes.", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            quit()
            return True
        return False



CSS = """
QMainWindow {
    background-color: white;
}
QMessageBox {
    background-color: white;
}
QMessageBox QPushButton{
    color: black;
}
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
    background-color: #F08E20;
    color: white;
    border: solid 3px black;
    border-radius: 5px;
    height: 30px;
}
QPushButton#Delete {
    background-color: #EB1B6B;
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
    background-color: #ADCC36;
    color: white;
    border: solid 3px black;
    border-radius: 5px;
    height: 30px;
    margin-top: 30px;
}
QPushButton#Add_button{
    background-color: #56ADD4;
    color: white;
}
QCheckBox{
    color: black;
    margin-left: 15%;
}
QComboBox{
    color: black;
}
QListView{
    background-color: white;
}

QTabBar::tab{
    color: black;
}
"""

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    app.setStyleSheet(CSS)
    win.show()
    sys.exit(app.exec())