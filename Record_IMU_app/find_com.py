from serial.tools import list_ports
from file_manager import *
from time import sleep
from graph import *
import threading
import serial

import traitement as tr


class Serial_COM():
	def __init__(self, _file, _menuBar, parent = None):

		self.findPorts = _menuBar
		self.current_file = _file
		self.graph = Graph(self)

		self.find_USB_devices()
		sleep(1)
		#self.find_card()

		self.RUNNING_FLAG = True

		self.find_usb_thr = threading.Thread(target=self.thread_search_cards, args=())
		self.find_usb_thr.start()


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
		print("Search cards - thread terminate..")



	def check_if_write_headline_in_file(self,):
		if self.SERIAL_SAVING_FLAG == 2 and not self.headline_write:
			self.current_file.set_full_paths()
			self.current_file.write_headLine()
			self.set_headline_flag(True)
			self.graph.set_graph_flag(1)
			self.serial.flushInput()

	def end_recording(self):
		self.current_file.close_all_data_files()
		self.graph.reset_graph()
		self.set_headline_flag(False)
		tr.generate_multiple(self.current_file.full_paths)  #Ecriture du file moyenne glissante


	def thread_run(self):
		while self.RUNNING_FLAG == 1:	

			self.check_if_write_headline_in_file()

			while self.SERIAL_SAVING_FLAG == 1:#LORSQUE L'ON CLIQUE SUR READY, CE FLAG PASSE A 1 JUSQU'A CE QUE CA ATTEIGNE 0 DE COMPTE A REBOURS				
				temp = self.serial.readline()
				data = str(temp.decode())
				
				if data:	#Check if we have data
					data_split = data.split('main > ')
					if len(data_split) > 1:
						if len(data_split[1].split('\t')) == 6:
							self.data_imu = data_split[1]
							self.current_file.write_data_imu(self.INDEX_SHAPE, self.data_imu) #Write imu data
							self.serial.flushInput()
			


		print("Imu get data - thread terminate..")

		

	def get_data_imu_thread_stop(self):
		self.RUNNING_FLAG = False	

	def search_usb_thread_stop(self):
		self.THREAD_USB_CARDS_FLAG = False

	def set_headline_flag(self, _value):
		self.headline_write = _value


	def set_SERIAL_SAVING_FLAG(self, _value):
		self.SERIAL_SAVING_FLAG = _value
	
	def get_com(self):
		return self.COM

	def set_serial(self, _ser):
		self.serial = _ser

	def get_serial(self):
		return self.serial

	def get_list_ports(self):
		return self.list_ports


	data_imu = []
	SERIAL_SAVING_FLAG = 6
	INDEX_SHAPE = 0

	bauds = 115200
	headline_write = False

	THREAD_USB_CARDS_FLAG = True
	list_ports = []
	serial = ""
	COM = ""


