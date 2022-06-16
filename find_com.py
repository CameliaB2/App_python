from serial.tools import list_ports
from file_manager import *
from time import sleep
from graph import *
import numpy as np
import threading
import serial
import time
import sys


class Serial_COM():
	def __init__(self, _file, _menuBar, parent = None):

		self.findPorts = _menuBar
		self.current_file = _file
		self.graph = Graph(self)

		self.find_USB_devices()
		sleep(1)
		self.find_card()

		self.RUNNING_FLAG = True

		find_usb_thr = threading.Thread(target=self.thread_search_cards, args=())
		find_usb_thr.start()


	def find_USB_devices(self):
			# Gérer SI on est sur windows ou pas 
		ports = serial.tools.list_ports.comports()
		ports_device = []
		diff_before_after = []
		for p in ports:
			ports_device.append(p.device)
			if( not str(p.device) in self.list_ports ):
				self.list_ports.append( str(p.device ))

		diff_before_after = list(set(self.list_ports) - set(ports_device))
		if(len(diff_before_after) > 0):
			for e in diff_before_after:
				self.list_ports.remove(e)

	def find_card(self):
		for port in self.list_ports:
			self.serial_verification(port)


	def change_port(self, _port):
		if( self.COM == _port ):
			return
		else:
			self.serial_verification(_port)

	def serial_verification(self, _port):
		ser = serial.Serial(_port, self.bauds, timeout = .038)
		if ser.isOpen():
			temp = ser.readline()
			data = str(temp.decode())
			if( data.find('main > ') and data.find('[INFO]')):
				self.COM = _port
				self.set_serial(ser)

				self.findPorts.setTitle('PORT: ' + str(self.COM))
				return

	def thread_search_cards(self):
		while(self.THREAD_USB_CARDS_FLAG):
			self.find_USB_devices()	#SEARCH A POTENTIAL NEW CARD


	def check_if_create_flag(self):
		sleep(1)
		if self.SERIAL_SAVING_FLAG == 2 and not self.headline_write:
			self.old_flag = self.SERIAL_SAVING_FLAG
			#self.current_file.set_current_shape(self.current_shape)
			self.graph.reset_graph()
			self.current_file.set_full_path()

	def check_if_write_headline_in_file(self, _path):
		if self.SERIAL_SAVING_FLAG == 2 and not self.headline_write:
			self.current_file.write_headLine(_path)
			self.set_headline_flag(True)
			self.graph.set_graph_flag(1)

	def check_if_write_data_in_file(self, _path): # To use if we want to save all the line in one time, not in real time
		if( self.old_flag == 1 and self.SERIAL_SAVING_FLAG == 0 ):
			self.old_flag = self.SERIAL_SAVING_FLAG
			for el in self.data_imu:
				self.current_file.write_data_imu(_path, str(el))
			self.set_headline_flag(False)

	def thread_run(self):
		while self.RUNNING_FLAG == 1:	
			#self.check_if_write_data_in_file()	# To use if we want to save all the line in one time, not in real time
			self.check_if_create_flag()
			self.check_if_write_headline_in_file(self.current_file.full_path)

			while self.SERIAL_SAVING_FLAG == 1:#LORSQUE L'ON CLIQUE SUR READY, CE FLAG PASSE A 1 JUSQU'A CE QUE CA ATTEIGNE 0 DE COMPTE A REBOURS
	
				if(self.old_flag == 2):
					self.start_time = time.time()

				if(self.FLAG_RECORD == 1):
					self.old_flag = self.SERIAL_SAVING_FLAG
					
					temp = self.serial.readline()
					data = str(temp.decode())
					
					if data:	#Check if we have data
						data_split = data.split('main > ')
						if len(data_split) > 1:
							#self.data_imu.append(data_split[1])	

							self.data_imu = data_split[1]
							self.current_file.write_data_imu(self.current_file.full_path, self.data_imu) #Write imu data

							#self.time_to_wait = time.time()-start
							#if(self.time_to_wait < self.RECORD_PERIOD):
							#	sleep( self.RECORD_PERIOD - self.time_to_wait )	#Wait 38ms ~= 26Hz
						
				else:
					self.set_SERIAL_SAVING_FLAG(0)

			if(self.SERIAL_SAVING_FLAG == 0):
				self.set_headline_flag(False)

	def thread_terminate():
		self.RUNNING_FLAG = False

	def set_headline_flag(self, _value):
		self.headline_write = _value

	def set_SERIAL_SAVING_FLAG(self, _value):
		self.SERIAL_SAVING_FLAG = _value
				
	def set_FLAG_RECORD(self, _value):
		self.FLAG_RECORD = _value
	
	def get_com(self):
		return self.COM

	def set_serial(self, _ser):
		self.serial = _ser

	def get_serial(self):
		return self.serial

	def get_list_ports(self):
		return self.list_ports

	time_to_wait = 0
	start_time = 0
	old_flag = 0
	data_imu = []
	path_file = ""
	SERIAL_SAVING_FLAG = 6
	current_shape = ""
	bauds = 115200
	headline_write = False

	THREAD_USB_CARDS_FLAG = 1
	list_ports = []
	serial = ""
	COM = ""

	RECORD_TIME = 60
	RECORD_PERIOD = 0.038
	FLAG_RECORD = 0

