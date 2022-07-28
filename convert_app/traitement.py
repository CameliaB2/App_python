import numpy as np
from time import sleep


def read_file(_filename):
	data_row = np.empty((0,6), int)
	data_col = [[], [], [], [], [], []]

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
	aver_data = [[], [], [], [], [], []]
	aver_data[0] = calculate_average(aX, _range)
	aver_data[1] = calculate_average(aY, _range)
	aver_data[2] = calculate_average(aZ, _range)

	aver_data[3] = calculate_average(gX, _range)
	aver_data[4] = calculate_average(gY, _range)
	aver_data[5] = calculate_average(gZ, _range)	
	sleep(0.5)
	
	return aver_data


def calculate_delta(_array):
	delta = []
	for i in range(len(_array)-1):
		delta.append(_array[i+1] -  _array[i])
	return delta

def calculate_delta_all_data(aX, aY, aZ, gX, gY, gZ):
	delta_data = [[], [], [], [], [], []]
	delta_data[0] = calculate_delta(aX)
	delta_data[1] = calculate_delta(aY)
	delta_data[2] = calculate_delta(aZ)

	delta_data[3] = calculate_delta(gX)
	delta_data[4] = calculate_delta(gY)
	delta_data[5] = calculate_delta(gZ)	
	sleep(0.5)
	
	return delta_data	