import numpy as np
from time import sleep


def read_file(_filename):
	data_row = np.empty((0,6), int)
	data_col = [[], [], [], [], [], []]
	composantes = np.empty(np.empty((0,6), int))

	f = open(_filename, "r")

	lines = f.readlines()
	count = 0
	for line in lines:
		if(count > 0): #Skip the headline
			data_str = line.strip()
			data_split = data_str.split('\t')
			data_row = np.vstack([data_row, data_split])
			for i in range(6):
				data_col[i].append(float(data_split[i]))
			
		count += 1
	f.close()

	return data_col


def calculate_average(_array, _range):
	return np.convolve(_array, np.ones(_range), 'valid') / _range

def calculate_average_all_data(aX, aY, aZ, gX, gY, gZ, _range):
	aver_datas = [[], [], [], [], [], []]
	aver_data = [[], [], [], [], [], []]
	aver_data[0] = calculate_average(aX, _range)
	aver_data[1] = calculate_average(aY, _range)
	aver_data[2] = calculate_average(aZ, _range)

	aver_data[3] = calculate_average(gX, _range)
	aver_data[4] = calculate_average(gY, _range)
	aver_data[5] = calculate_average(gZ, _range)	
	sleep(0.5)
	"""
	for i in range(6):
		aver_datas[i].append(aver_data[i])
		#aver_datas = np.concatenate(aver_acc_x, aver_acc_y, aver_acc_z, aver_gyr_x, aver_gyr_y, aver_gyr_z)
	"""
	return aver_data

def generate(_full_path, _range, _data):
	if(len(_data[0]) > _range):
		aver_datas = calculate_average_all_data(_data[0], _data[1], _data[2], _data[3], _data[4], _data[5], _range)

		full_path_average = _full_path.split('.')[0] + '-average-Range-' + str(_range) + '.csv'

		data_file = open(full_path_average, "a")
		head_line = "A_X[mg]\tA_Y[mg]\tA_Z[mg]\tG_X[dps]\tG_Y[dps]\tG_Z[dps]\t\n"
		data_file.write(head_line)
		for i in range(len(aver_datas[0])):
			data_file.write(str(aver_datas[0][i]) + '\t' + 
							str(aver_datas[1][i]) + '\t' + 
							str(aver_datas[2][i]) + '\t' + 
							str(aver_datas[3][i]) + '\t' + 
							str(aver_datas[4][i]) + '\t' +
							str(aver_datas[5][i]) + '\n')
		data_file.close()

def generate_multiple(_full_paths):
	_range = [4, 8, 16]
	for full_path in _full_paths:
		try:
			data = read_file(full_path)
			for val in _range:
				generate(full_path, val, data)
				sleep(1)
			return
		except IOError:
			return