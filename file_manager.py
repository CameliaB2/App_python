import find_com
from time import sleep
from datetime import datetime
import os

class File_manager():
	def __init__(self, parent=None):
		self.name_curr_shape = "test"

	def write_headLine(self, _path):
		head_line = "A_X[mg]\tA_Y[mg]\tA_Z[mg]\tG_X[dps]\tG_Y[dps]\tG_Z[dps]\t\n"

		data_file = open(_path, "a")
		data_file.write(head_line)
		data_file.close()

	def write_data_imu(self, _path, _data_imu):
		data_file = open(_path, "a")
		data_file.write(str(_data_imu))
		data_file.close()

	def set_suffix(self, suffix):
		self.suffix_ = suffix

	def generate_date(self):
		#today = date.today()
		now = datetime.now()
		date = now.strftime("%Y_%m_%d-%H_%M_%S-")
		return str(date)

	def set_current_shape(self, _name):
		self.name_curr_shape = _name

	def set_full_path(self):
		self.full_path = self.path_file + "/"  + self.generate_date() + self.name_curr_shape + "-" + self.suffix_ + ".csv"
		print("self full_path : ", self.full_path)
		self.full_path_average = self.path_file + "/"  + self.generate_date() + self.name_curr_shape + "-" + self.suffix_ + "-average.csv"


	def set_file_path(self, _path):
		self.path_file = _path
		print("self path : ", self.path_file)

		

	def remove_file(self):
		print(self.full_path)
		if os.path.exists(self.full_path):
  			os.remove(self.full_path)
		else:
			print("The file does not exist") 

	name_curr_shape = ""
	full_path = ""
	full_path_average = ""
	
	path_file = ""
	suffix_ = ""