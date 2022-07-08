import numpy as np

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

def search_directory():
    directory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
    if(directory != ""):
        self.path_qlineEdit.setText(directory)
        self.write_path_file(directory)
        return