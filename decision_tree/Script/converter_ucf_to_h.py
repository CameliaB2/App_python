	



def write_data(data_file, _data):
	data_file.write(str(_data) + '\n')

if __name__ == "__main__":
	
	path = "MLC_configurator.h"
	data = {'#ifndef MLC_CONFIGURATION_H',\
			'#define MLC_CONFIGURATION_H\n',\
			'#ifdef __cplusplus',\
  			'\textern "C" {',\
			'#endif'\
			}

	data_file = open(path, "a")
	for d in data:
		write_data(data_file, d)

	data_file.close()