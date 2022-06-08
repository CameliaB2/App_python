from PySide6.QtWidgets import *
from random import randint
from time import sleep
import pyqtgraph as pg
import traitement as tr
import threading
import time
import numpy as np

class Graph(QWidget):
	def __init__(self, _serial, parent = None):
		super(Graph, self).__init__( parent )
		
		self.serial = _serial
		self.t = list([0])	

		#self.acc_graph = self.create_graph('w', "Acceleration", "Acceleration (mg)")

		styles = {"color": "#f00", "font-size": "10px"}

		self.acc_graph = pg.PlotWidget()   
		self.acc_graph.setBackground('w')
		self.acc_graph.setTitle("Acceleration")
		self.acc_graph.addLegend()
		self.acc_graph.setLabel("left", "Acc (mg)", **styles)
		self.acc_graph.setLabel("bottom", "Time (s)", **styles)
		self.acc_graph.setFixedHeight(200)

		self.gyr_graph = pg.PlotWidget()
		self.gyr_graph.setBackground('w')
		self.gyr_graph.setTitle("Gyroscope")
		self.gyr_graph.addLegend()
		self.gyr_graph.setLabel("left", "Gyr (dps)", **styles)
		self.gyr_graph.setLabel("bottom", "Time (s)", **styles)
		self.gyr_graph.setFixedHeight(200)

		pen = pg.mkPen(color='r')
		self.acc_line.append( self.acc_graph.plot(self.t, self.acc[0], pen=pen) )
		self.gyr_line.append( self.gyr_graph.plot(self.t, self.gyr[0], pen=pen) )
		pen = pg.mkPen(color='g')
		self.acc_line.append( self.acc_graph.plot(self.t, self.acc[1], pen=pen) )
		self.gyr_line.append( self.gyr_graph.plot(self.t, self.gyr[1], pen=pen) )
		pen = pg.mkPen(color='b')
		self.acc_line.append( self.acc_graph.plot(self.t, self.acc[2], pen=pen) )
		self.gyr_line.append( self.gyr_graph.plot(self.t, self.gyr[2], pen=pen) )


		self.lay = QHBoxLayout(self)

		self.update_graph_thr = threading.Thread(target=self.update_plot_data, args=())
		self.update_graph_thr.start()
		
		self.lay.addWidget(self.acc_graph)
		self.lay.addWidget(self.gyr_graph)

		self.setLayout(self.lay)

	def update_plot_data(self):
		while(True):
			while(self.FLAG_GRAPH == 1):
				while(self.serial.SERIAL_SAVING_FLAG == 1 and len(self.serial.data_imu)>0 ):
					start = time.time()
					with open(self.serial.current_file.full_path, "r") as fp:
						last_line = fp.readlines()[-1]
						#self.number_line_file = len(fp.readlines())

					data_str = last_line.strip()
					data_split = data_str.split('\t')

					if( len(data_split) == 6 and data_str.find("Acc") == -1 and data_str.find("Gyr") == -1):
						if(len(self.t) > 100):
							self.t = self.t[1:]  # Remove the first y element.
							self.t.append((self.t[-1] + 1))#*1/26)  # Add a new value 1 higher than the last.
						else:
							self.t.append((self.t[-1] + 1))#*1/26)  # Add a new value 1 higher than the last.

						for i in range(len(self.acc)):
							if(len(self.acc[i]) > 100):
								self.acc[i] = self.acc[i][1:]  # Remove the first
								self.acc[i].append( float(data_split[i]))  # Add a new random value.

								self.gyr[i] = self.gyr[i][1:]  # Remove the first
								self.gyr[i].append( float(data_split[i+3]))  # Add a new random value.
							else:
								self.acc[i].append( float(data_split[i]))  # Add a new random value.
								self.gyr[i].append( float(data_split[i+3]))  # Add a new random value.

							self.acc_line[i].setData(self.t, self.acc[i])  # Update the data.
							self.gyr_line[i].setData(self.t, self.gyr[i])  # Update the data.
							
						self.time_to_wait = time.time()-start
						if(self.time_to_wait < 0.038):
							sleep(0.038-self.time_to_wait)
	def reset_graph(self):
		self.t = list([0])	
		self.acc = [[0], [0], [0]]
		self.gyr = [[0], [0], [0]]

		

	def set_graph_flag(self, _value):
		self.FLAG_GRAPH = _value

	acc = [[0], [0], [0]]
	gyr = [[0], [0], [0]]
	acc_line = []
	gyr_line = []
	FLAG_GRAPH = 0