import find_com
from time import sleep
from datetime import datetime
import os

class File_manager():
	def __init__(self, parent=None):
		self.name_curr_shape = "test"

	def write_headLine(self, time_record):
		self.data_files = []
		for i in range(len(self.full_paths)):
			if(time_record == "YES"):
				head_line = "Day[j]\tHour[h]\tMin[min]\tSec[s]\tA_X[mg]\tA_Y[mg]\tA_Z[mg]\tG_X[dps]\tG_Y[dps]\tG_Z[dps]\t\n"
			else:
				head_line = "A_X[mg]\tA_Y[mg]\tA_Z[mg]\tG_X[dps]\tG_Y[dps]\tG_Z[dps]\t\n"

			self.data_files.append(open(self.full_paths[i], "a"))
			self.data_files[i].write(head_line)

	def write_data_imu(self, _index, _data_imu):
		if self.data_files[_index].closed == False:
			self.data_files[_index].write(str(_data_imu))
		else:
			print("File has closed.")

	def set_suffix(self, suffix):
		self.suffix_ = suffix

	def generate_date(self):
		now = datetime.now()
		date = now.strftime("%Y_%m_%d-%H_%M_%S")
		return str(date)


	def set_current_shapes(self, _data, _name):
		self.name_curr_shape = []
		self.name_curr_shapes = _data['classes'][_name]['sequence']
		print(self.name_curr_shapes)
		#self.name_curr_shapes = _name.split("_&_")
		print(self.name_curr_shapes)

	def set_full_paths(self, odr):
		self.full_paths = []
		for shape in self.name_curr_shapes:
			path = self.path_file + "/" + shape 
			isExist = os.path.exists(path)
			if not isExist:
				os.makedirs(path)
				print("The new directory is created!")

			if(self.suffix_ != ""):
				self.full_paths.append(path + "/"  + self.generate_date() + "-" + odr + "-" + shape + "-" + self.suffix_ + ".csv")
			else:
				self.full_paths.append(path + "/"  + self.generate_date() + "-" + odr + "-" + shape + ".csv")


	def set_file_path(self, _path):
		self.path_file = _path

		
	def remove_file(self):
		self.close_all_data_files()
		for i in range(len(self.data_files)):
			print(self.full_paths[i])
			if os.path.exists(self.full_paths[i]):
				os.remove(self.full_paths[i])
			else:
				print("The file does not exist") 

	def close_all_data_files(self):
		for file in self.data_files:
			file.close()

	name_curr_shape = ""
	name_curr_shapes = []
	data_files = []
	full_paths = []
	
	path_file = ""
	suffix_ = ""