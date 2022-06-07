from serial.tools import list_ports
import serial
import time
import numpy as np
import threading
import sys
from time import sleep
from datetime import datetime
from file_manager import *

from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import * 
from PySide6.QtCore import * 

#test
class Serial_COM():
	def __init__(self, _file, _menuBar, parent = None):

		self.findPorts = _menuBar
		self.find_USB_devices()
		sleep(1)
		#self.find_card()
		self.RUNNING_FLAG = True
		self.current_file = _file
		find_usb_thr = threading.Thread(target=self.thread_search_cards, args=())
		is_connected = threading.Thread(target = self.find_card, args=())
		find_usb_thr.start()
		is_connected.start()

	def find_USB_devices(self):
			# Gérer SI on est sur windows ou pas 
		ports = serial.tools.list_ports.comports()
		for p in ports:
			if(not (  str(p.device) in self.list_ports )):
				self.list_ports.append(str(p.device))
				self.findPorts.addAction(self.list_ports[-1])
				self.findPorts.triggered.connect(lambda: self.change_port(self.list_ports[-1]))

	def find_card(self):
		while(1):
			for p in self.list_ports:
				ser = serial.Serial(p, self.bauds, timeout = .1)
				if ser.isOpen():
					temp = ser.readline()
					data = str(temp.decode())
					if( data.find('main >') and data.find('[INFO]')):
						self.COM = p
						self.set_serial(ser)
						#ajouter le voyant
						self.isConnected_flag = True
						print(self.isConnected_flag)
						break
					else:
						self.isConnected_flag = False
						print(self.isConnected_flag)

	def change_port(self, _port):
		if(self.COM == _port):
			return
		else:
			ser = serial.Serial(_port, self.bauds, timeout = .1)
			if ser.isOpen():
				temp = ser.readline()
				data = str(temp.decode())
				if( data.find('main >') and data.find('[INFO]')):
					self.COM = _port
					self.set_serial(ser)
					return

	def thread_search_cards(self):
		while(self.THREAD_USB_CARDS_FLAG):
			self.find_USB_devices()	#SEARCH A POTENTIAL NEW CARD


	def check_if_write_data_in_file(self, _path):
		if(self.old_flag == 1 and self.SERIAL_SAVING_FLAG == 0):
			self.old_flag = self.SERIAL_SAVING_FLAG
			for el in self.data_imu:
				self.current_file.write_data_imu(_path, str(el))
			self.set_headline_flag(False)

	def check_if_write_headline_in_file(self, _path):
		if self.SERIAL_SAVING_FLAG == 2 and not self.headline_write:
			self.old_flag = self.SERIAL_SAVING_FLAG
			self.current_file.set_current_shape(self.current_shape)
			self.current_file.write_headLine(_path)
			self.set_headline_flag(True)

	def check_if_create_flag(self):
		sleep(0.1)#le temps que le full_path se set bien
		if self.SERIAL_SAVING_FLAG == 2 and not self.headline_write:
			print("je suis là")
			self.old_flag = self.SERIAL_SAVING_FLAG
			self.current_file.set_full_path()
			


	def thread_run(self):
		self.set_headline_flag(False)
		while self.RUNNING_FLAG == 1:
			self.check_if_create_flag()
			self.check_if_write_headline_in_file(self.current_file.full_path)
			while self.SERIAL_SAVING_FLAG == 1:#LORSQUE L'ON CLIQUE SUR READY, CE FLAG PASSE A 1 JUSQU'A CE QUE CA ATTEIGNE 0 DE COMPTE A REBOURS
				start = time.time()
				if(self.old_flag == 2):
					self.start_time = time.time()
					
				
				if(time.time() - self.start_time < 60):
					self.old_flag = self.SERIAL_SAVING_FLAG
					temp = self.serial.readline()#Capture serial output as a decoded string
					data = temp.decode()
					data_str = str(data)
				
					if data_str :#Check if we have data
						data_split = data_str.split(' > ')
						if len(data_split) > 1:
							#self.data_imu.append(data_split[1])	
							self.current_file.write_data_imu(self.current_file.full_path, data_split[1])
							self.time_to_wait = time.time()-start
							sleep(abs(0.038-self.time_to_wait))	#Wait 38ms ~= 26Hz
				else:
					self.SERIAL_SAVING_FLAG = 0

			if self.SERIAL_SAVING_FLAG == 0:
				self.set_headline_flag(False)



	def thread_terminate(self):
		self.RUNNING_FLAG = False

	def set_SERIAL_SAVING_FLAG(self, _value):
		self.SERIAL_SAVING_FLAG = _value
				
	def set_headline_flag(self, _value):
		self.headline_write = _value

	def get_com(self):
		return self.COM

	def set_serial(self, _ser):
		self.serial = _ser

	def get_serial(self, _ser):
		return self.serial



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
	
	isConnected_flag = False