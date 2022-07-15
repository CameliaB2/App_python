import sys

from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import *
import pyqtgraph as pg
import file_manager as fm



class Graph(QWidget):
	def __init__(self, 
				 type_data_to_show,
				 data, 
				 checkbox_data_obj,
				 parent = None):
		super(Graph, self).__init__( parent )

		self.data = data
		self.type_data_to_show = type_data_to_show
		self.checkbox_data_obj = checkbox_data_obj
		self.curves = [None for i in range(len(self.type_data_to_show))]
		self.create_graph()

	def create_graph(self):
		self.graph_layout = QVBoxLayout()
		self.graph = self.set_graph_parameters('w', "Acceleration", "Acc (mg)", "Time (*1/26 s)", 720, 400)

		colors = ['b', 'r', 'g', 'violet', 'orange']
		_time = list([0])  
		_data = [0]

		self.legend = pg.LegendItem(offset=(0.4, .7), colCount=5)
		self.legend.setParentItem(self.graph.graphicsItem())
		for i in range(len(self.type_data_to_show)):
			pen = pg.mkPen(color=colors[i], width=2) 
			self.curves[i] = self.graph.plot(_time, _data, name = str(self.type_data_to_show[i]), pen=pen)
			self.legend.addItem(self.curves[i], str(self.type_data_to_show[i]))

		self.graph_layout.addWidget(self.graph)
		self.setLayout(self.graph_layout)

	def set_graph_parameters(self, _bg, _title, _abs, _ord, _width, _height):
		self.styles = {"color": "#222", "font-size": "15px"}
		graph = pg.PlotWidget()   
		graph.setBackground(_bg)
		graph.setTitle(_title)
		legend = pg.LegendItem()
		legend.setParentItem(graph.graphicsItem())
		graph.setLabel("left", _abs, **self.styles)
		graph.setLabel("bottom", _ord, **self.styles)
		graph.showGrid(x=True, y=True)
		graph.setMinimumWidth(_width)
		graph.setMinimumHeight(_height)
		return graph


	def update_graph_parameters(self, _title, _abs, _ord):      
		self.graph.setTitle(_title)  
		self.graph.setLabel("left", _abs, **self.styles)
		self.graph.setLabel("bottom", _ord, **self.styles)


	def add_graph(self, type_data, current_composante):
		self._time = list([0])  

		for i in range(len(self.data[type_data][current_composante])-1):
			self._time.append((self._time[-1] + 1))
   
		self.curves[type_data].setData(self._time, self.data[type_data][current_composante])  # Update the data.

	def update_graph(self, index, current_composante):
		if(self.checkbox_data_obj[index].isChecked()):
			self.add_graph(index, current_composante)
		else:
			self.curves[index].clear()
			self.reset_graph(index)
	        
	def reset_graph(self, type_data):
		_time = list([0])  
		_data = [0]
		self.curves[type_data].setData(_time, _data)

	def reset_view(self):
		self.graph.enableAutoRange(axis='x')
		self.graph.setAutoVisible(x=True)
		self.graph.enableAutoRange(axis='y')
		self.graph.setAutoVisible(y=True)