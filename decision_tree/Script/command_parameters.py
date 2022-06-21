import argparse
import logging

WINDOW_LENGTH = 50
MLC_ODR = "26 Hz"
ACCELEROMETER_ODR = "26 Hz"
ACCELEROMETER_FS = "2 g"
GYROSCOPE_FS = "2000 dps"
GYROSCOPE_ODR = "26 Hz" 
INPUT_TYPE = "accelerometer+gyroscope"

class cmd_parameters:

	def __init__(self):
		self.parser = argparse.ArgumentParser()
		self.add_args()

		#default settings
		self.window_length = WINDOW_LENGTH
		self.mlc_odr = MLC_ODR
		self.acc_odr = ACCELEROMETER_ODR
		self.acc_fs = ACCELEROMETER_FS
		self.gyr_fs = GYROSCOPE_FS
		self.gyr_odr = GYROSCOPE_ODR
		self.input_type = INPUT_TYPE
		self.name_ucf = "test"

	def add_args(self):
		self.parser.add_argument("-wl", "--Window_length", type=int, required=False, \
			help="size of the window length. Must be in the interval [1;255]")

		self.parser.add_argument("-mlc_odr", "--Mlc_odr", type=float, required=False, \
			help="Output data rate of the MLC. Must be initialized to : 12.5, 26, 52 or 104")

		self.parser.add_argument("-acc_odr", "--Accelerometer_odr", type=float, required=False, \
			help="Output data rate of the accelerometer (Hz). Must be initialized to : 12.5, 26, 52, 104, 208, 416, 833, 1666, 3332 or 6664")

		self.parser.add_argument("-acc_fs", "--Accelerometer_fs", type=int, required=False, \
			help="Linear acceleration measurement range (g). Must be initialized to : 2, 4, 8 or 16")

		self.parser.add_argument("-gyr_fs", "--Gyroscope_fs", type=int, required=False, \
			help="Angular rate measurement range (dps). Must be initialized to : 125, 250, 500, 1000 or 2000")

		self.parser.add_argument("-gyr_odr", "--Gyroscope_odr", type=float, required=False, \
			help="Output data rate of the gyroscope (Hz). Must be initialized to : 12.5, 26, 52, 104, 208, 416, 833, 1666, 3332 or 6664")

		self.parser.add_argument("-it", "--Input_type", type=int, required=False, \
			help="Change the module use for input data. Must be initialized to : 1 for the mode \"accelerometer+gyroscope\", or 2 for \"accelerometer_only\"")

		self.parser.add_argument("-n", "--Name", type=str, required=True, \
			help="Name of the .ucf and .h file")

		self.args = self.parser.parse_args()



	def init_window_length(self):
		if(int(self.args.Window_length) > 0 and int(self.args.Window_length) < 255):
			self.window_length = int(self.args.Window_length)
		else:
			logging.error("ERROR: Window_length initialized by default (\"" + str(WINDOW_LENGTH) + \
        					"\"). WL must be updated to a value in the interval [1;255]\n")

	def init_mlc_odr(self):
		mcl_odr_config = [12.5, 26, 52, 104]
		if(self.args.Mlc_odr in mcl_odr_config):
			self.mlc_odr = str(self.args.Mlc_odr) + " Hz" if self.args.Mlc_odr == 12.5 else str(int(self.args.Mlc_odr)) + " Hz" 
		else:
			logging.error("ERROR: mlc_odr initialized by default (\"" + MLC_ODR + \
							"\"). mlc_odr must be : 12.5 for (12.5 Hz), 26, 52, 104\n")

	def init_acc_odr(self):
		acc_odr_config = [12.5, 26, 52, 104, 208, 416, 833, 1666, 3332, 6664]
		if(self.args.Accelerometer_odr in acc_odr_config):
			self.acc_odr = str(self.args.Accelerometer_odr) + " Hz" if self.args.Accelerometer_odr == 12.5 else str(int(self.args.Accelerometer_odr)) + " Hz" 
		else:
			logging.error("ERROR: acc_odr initialized by default (\"" + ACCELEROMETER_ODR + \
							"\"). acc_odr must be : 12.5 for (12.5 Hz), 26, 52, 104, \
							208, 416, 833, 1666, 3332, 6664\n")

	def init_acc_fs(self):
		acc_fs_config = [2, 4, 8, 16]
		if(self.args.Accelerometer_fs in acc_fs_config):
			self.acc_fs = str(self.args.Accelerometer_fs) + " g"
		else:
			logging.error("ERROR: acc_fs initialized by default (\"" + ACCELEROMETER_FS + \
							"\"). acc_fs must be : 2 for (2 g), 4, 8, 16\n")

	def init_gyr_fs(self):
		gyr_fs_config = [125, 250, 500, 1000, 2000]
		if(self.args.Gyroscope_fs in gyr_fs_config):
			self.gyr_fs = str(self.args.Gyroscope_fs) + " dps"
		else:
			logging.error("ERROR: gyr_fs initialized by default (\"" + GYROSCOPE_FS + \
							"\"). gyr_fs must be : 125 for (125 g), 250, 500, 1000, 2000\n")

	def init_gyr_odr(self):
		gyr_odr_config = [12.5, 26, 52, 104, 208, 416, 833, 1666, 3332, 6664]
		if(self.args.Gyroscope_odr in gyr_odr_config):
			self.gyr_odr = str(self.args.Gyroscope_odr) + " Hz" if self.args.Gyroscope_odr == 12.5 else str(int(self.args.Gyroscope_odr)) + " Hz" 
		else:
			logging.error("ERROR: gyr_odr initialized by default (\"" + GYROSCOPE_ODR + \
							"\"). gyr_odr must be : 12.5 for (12.5 Hz), 26, 52, 104, \
							208, 416, 833, 1666, 3332, 6664\n")

	def init_input_type(self):
		if(self.args.Input_type == 1):
			self.input_type = "accelerometer+gyroscope"
		elif(self.args.Input_type == 2):
			self.input_type = "accelerometer_only"
		else:
			logging.error("ERROR: input_type initialized by default (\"" + INPUT_TYPE + \
							"\"). input_type must be : 1 for the mode \"accelerometer+gyroscope\", or 2 for \"accelerometer_only\"\n")

	def init_namefile(self):
		self.name_ucf = self.args.Name.strip().replace('-', '_')

		"""
		if(FileManager.is_path_exists_or_creatable(self.args.Name)):    
    		return re.sub(r'(?u)[^-\w.]', '', s) 
			self.name_ucf = self.args.Name
		else:
			logging.error("ERROR: the name is wrong")
			raise SettingInvalidException("The file seems to be invalid: %s" % self.args.Name)

"""

	def check_args_value(self):

		logging.info("\n\n\tMachine Learning Core Configuration :\n\n")

		if self.args.Window_length:
			self.init_window_length()
		if self.args.Mlc_odr:
			self.init_mlc_odr()
		if self.args.Accelerometer_odr:
			self.init_acc_odr()
		if self.args.Accelerometer_fs:
			self.init_acc_fs()
		if self.args.Gyroscope_fs:
			self.init_gyr_fs()
		if self.args.Gyroscope_odr:
			self.init_gyr_odr()
		if self.args.Input_type:
			self.init_input_type()
		self.init_namefile()

		logging.info("\n\n\tCurrent Machine Learning Core Configuration :\n")
		logging.info("window_length initialized to: \t\"" + str(self.window_length) + "\"")
		logging.info("mlc_odr initialized to: \t\t\"" + self.mlc_odr + "\"")
		logging.info("acc_odr initialized to: \t\t\"" + self.acc_odr + "\"")
		logging.info("acc_fs initialized to: \t\t\"" + self.acc_fs + "\"")
		logging.info("gyr_fs initialized to: \t\t\"" + self.gyr_fs + "\"")
		logging.info("gyr_odr initialized to: \t\t\"" + self.gyr_odr + "\"")
		logging.info("input_type initialized to: \t\"" + self.input_type + "\"\n\n")
		logging.info("ucf and h script Name will be: \t\"" + self.name_ucf + ".ucf and " + self.name_ucf + ".h\"\n\n")

		return self.window_length, self.mlc_odr, self.acc_odr, self.acc_fs, self.gyr_fs, self.gyr_odr, self.input_type


