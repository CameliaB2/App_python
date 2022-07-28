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

		self.acc_graph = self.create_graph('w', "Acceleration", "Acc (mg)", "Time (s)", 400, 120)
		#self.gyr_graph = self.create_graph('w', "Gyroscope", "Gyr (dps)", "Time (s)", 400, 120)

		self.curves = ["Acc X", "Acc Y", "Acc Z", "Gyr X", "Gyr Y", "Gyr Z"]
		self.colors = ['r', 'g', 'b']
		self.curves_acc = [None for i in range(3)]
		#self.curves_gyr = [None for i in range(3)]
		for i in range(3):
			pen = pg.mkPen(color=self.colors[i])
			self.curves_acc[i] = self.acc_graph.plot(self.t, self.acc[i], pen=pen, name=self.curves[i])
			#self.curves_gyr[i] = self.gyr_graph.plot(self.t, self.gyr[i], pen=pen, name=self.curves[i+3])


		self.lay = QVBoxLayout(self)

		self.update_graph_thr = threading.Thread(target=self.update_plot_data, args=())
		#self.update_graph_thr.start()

		self.lay.addWidget(self.acc_graph)
		#self.lay.addWidget(self.gyr_graph)

		self.setLayout(self.lay)

	def create_graph(self, _bg, _title, _abs, _ord, _width, _height):
		styles = {"color": "#f00", "font-size": "10px"}
		graph = pg.PlotWidget()   
		graph.setBackground(_bg)
		graph.setTitle(_title)
		graph.addLegend()
		graph.setLabel("left", _abs, **styles)
		graph.setLabel("bottom", _ord, **styles)
		graph.setFixedWidth(_width)
		graph.setFixedHeight(_height)
		return graph

	def update_plot_data(self):
		data_prec = []
		while(self.UPDATE_GRAPH_FLAG):
			while(self.FLAG_GRAPH == 1):
				while(self.serial.SERIAL_SAVING_FLAG == 1 and len(self.serial.data_imu)>0 ):
					start = time.time()
					#with open(self.serial.current_file.full_path, "r") as fp:
					#	last_line = fp.readlines()[-1]
						#self.number_line_file = len(fp.readlines())

					#data_str = last_line.strip()
					data_split = self.serial.data_imu.split('\t')
					if(data_split != data_prec):
						data_prec = data_split
					
						if( len(data_split) == 6 and self.serial.data_imu.find("A") == -1 and self.serial.data_imu.find("G") == -1):
							if(len(self.t) > 99):
								self.t.pop(0)  # Remove the first y element.
								self.t.append((self.t[-1] + 1))#*1/26)  # Add a new value 1 higher than the last.
							else:
								self.t.append((self.t[-1] + 1))#*1/26)  # Add a new value 1 higher than the last.

							for i in range(len(self.acc)):
								if(len(self.acc[i]) > 99):
									self.acc[i] = self.acc[i][1:]  # Remove the first
									self.acc[i].append( float(data_split[i]))  # Add a new random value.

									#self.gyr[i] = self.gyr[i][1:]  # Remove the first
									#self.gyr[i].append( float(data_split[i+3]))  # Add a new random value.
								else:
									self.acc[i].append( float(data_split[i]))  # Add a new random value.
									#self.gyr[i].append( float(data_split[i+3]))  # Add a new random value.
								self.curves_acc[i].setData(self.acc[i])  # Update the data.
								#self.curves_gyr[i].setData(self.t, self.gyr[i])  # Update the data.
							"""
							self.time_to_wait = time.time()-start
							if(self.time_to_wait < self.TIME_ODR):
								print("ici")
								sleep(self.TIME_ODR-self.time_to_wait)
							"""
						sleep(0.01)
					
		print("Update graphs - thread terminate..")

	def reset_graph(self):
		self.t = list([0])	
		self.acc = [[0], [0], [0]]
		#self.gyr = [[0], [0], [0]]
		for i in range(3):
			self.curves_acc[i].setData(self.t, self.acc[i])  # Update the data.
			#self.curves_gyr[i].setData(self.t, self.gyr[i])  # Update the data.
		
		

	def set_graph_flag(self, _value):
		self.FLAG_GRAPH = _value

	def update_graph_thread_stop(self):
		self.set_graph_flag(0)
		self.UPDATE_GRAPH_FLAG = False	

	acc = [[0], [0], [0]]
	gyr = [[0], [0], [0]]
	acc_line = []
	gyr_line = []
	FLAG_GRAPH = 0
	TIME_ODR = 0.038
	UPDATE_GRAPH_FLAG = True
