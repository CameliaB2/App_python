import numpy as np
from mlc_script_log import *

class Arff_generator:

    def __init__(self):
        self.means_data_features = [[], [], [], [], [], []]
        self.min_data_features = [[], [], [], [], [], []]
        self.max_data_features = [[], [], [], [], [], []]
        self.peakToPeak_data_features = [[], [], [], [], [], []]
        self.variance_data_features = [[], [], [], [], [], []]
        self.energy_data_features = [[], [], [], [], [], []]
        self.classes_data_features = []


        self.composantes = ['Acc_X', 'Acc_Y', 'Acc_Z', 'Gyr_X', 'Gyr_Y', 'Gyr_Z']
        self.features = ['MEAN', 'MAXIMUM', 'MINIMUM', 'PEAK_TO_PEAK', 'VARIANCE', 'ENERGY']
        
        self.features_composante = [] #Exemple MEAN_Acc_X
        self.features_fonction_composante = [] #Exemple F1_MEAN_on_Acc_X
        self.features_used_for_tree = []
        self.start_composante = 0

    def set_datalogs(self, datalogs):
        self.datalogs = datalogs

    def set_results(self, results):
        self.results = results

    def set_composantes(self, _composantes):
        self.composantes = _composantes


    def read_file(self, _filename):
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

        return data_col, count-1

    def calculate_data_features(self, window_length):    

        for i in range(len(self.datalogs)):
            if os.path.isfile(self.datalogs[i]):
                data, number_data_file = self.read_file(self.datalogs[i])        
            else:
                logging.error("\nERROR: The following file does not exist: " + self.datalogs[i])
            
            self.number_windows = number_data_file/window_length

            for j in range(self.start_composante, len(self.composantes)):
                for k in range (0, int(self.number_windows)):
                    if('MEAN' in self.features):
                        self.means_data_features[j].append(convert_value(j, mean_feature(data, j, k*window_length, window_length)))
                    if('MINIMUM' in self.features):    
                        self.min_data_features[j].append(convert_value(j, min_feature(data, j, k*window_length, window_length)))
                    if('MAXIMUM' in self.features):
                        self.max_data_features[j].append(convert_value(j, max_feature(data, j, k*window_length, window_length)))
                    if('PEAK_TO_PEAK' in self.features):                        
                        self.peakToPeak_data_features[j].append(convert_value(j, peak_to_peak_feature(data, j, k*window_length, window_length)))
                    if('VARIANCE' in self.features):                        
                        self.variance_data_features[j].append(convert_value(j, variance_feature(data, j, k*window_length, window_length)))
                    if('ENERGY' in self.features):                        
                        self.energy_data_features[j].append(convert_value(j, energy_feature(data, j, k*window_length, window_length)))
                        
            
            for j in range(int(self.number_windows)):
                self.classes_data_features.append(self.results[i])

        self.write_data_arff_file()
        self.close_arff_file()



    def create_arff_file(self, arff_filename):
        self.arff_filename = arff_filename

        self.data_file = open(self.arff_filename, "w")

        self.data_file.write("@relation \'MLC\'\n\n")

        count = 0
        for i in range(self.start_composante, len(self.composantes)):
            for j in range(0, len(self.features)):
                
                name_feature_composante = self.features[j] + '_' +  self.composantes[i] #Exemple MEAN_Acc_X
                self.features_composante.append(name_feature_composante)

                name_fonction_feature_composante = 'F' + str(count+1) + '_' + self.features[j] + '_on_' + self.composantes[i] #Exemple F1_MEAN_on_Acc_X
                self.features_fonction_composante.append(name_fonction_feature_composante)
                
                self.data_file.write("@attribute " + name_fonction_feature_composante + ' numeric\n')
                count += 1

        _classes = ''
        _classes_list = []

        for res in self.results:
            isPresent = False
            if(len(_classes_list) == 0):
                _classes_list.append(res)
                _classes += res
            else:
                for classe in _classes_list:
                    if res == classe:
                        isPresent = True
                if not isPresent:
                    _classes_list.append(res)
                    _classes += (', ' + res)

        self.data_file.write("@attribute class {" + _classes + '}\n\n')

    def write_data_arff_file(self):
        self.data_file.write("@data\n")
        for i in range(len(self.classes_data_features)): #Number of lines
            val = ''
            for j in range(self.start_composante, len(self.composantes)):                 
                if('MEAN' in self.features):
                    val += str(round(self.means_data_features[j][i], 7)) + ', '
                if('MINIMUM' in self.features):    
                    val += str(round(self.min_data_features[j][i], 7)) + ', '
                if('MAXIMUM' in self.features):
                    val += str(round(self.max_data_features[j][i], 7)) + ', '
                if('PEAK_TO_PEAK' in self.features):                        
                    val += str(round(self.peakToPeak_data_features[j][i], 7)) + ', '               
                if('VARIANCE' in self.features):           
                    val += str(round(self.variance_data_features[j][i], 7)) + ', '                 
                if('ENERGY' in self.features):           
                    val += str(round(self.energy_data_features[j][i], 7)) + ', '
                
            self.data_file.write(str(val) + str(self.classes_data_features[i]) + '\n')

    def close_arff_file(self):
        self.data_file.close()
        logging.info("\nARFF generated successfully: " + self.arff_filename)


    def write_arff_generation_txt(self,
                                arff_filename_txt,
                                device_name,
                                mlc_odr,
                                input_type,
                                accelerometer_fs,
                                accelerometer_odr,
                                gyroscope_fs,
                                gyroscope_odr,
                                n_decision_trees,
                                window_length):
        with open(arff_filename_txt, "w") as f:
            for i in range(len(self.datalogs)):
                if os.path.isfile(self.datalogs[i]):
                    f.write("%d,0,%s,%s\n" % (i, self.results[i], self.datalogs[i]))
                else:
                    logging.error("\nERROR: The following file does not exist: " + self.datalogs[i])

            f.write("configurationStarted\n")
            f.write(device_name + "\n")
            f.write(mlc_odr + "\n")
            f.write("<input_type>" + input_type + ",") 

            # accelerometer settings
            f.write(accelerometer_fs +",")  
            f.write(accelerometer_odr + ",") 

            # gyroscope settings
            if "gyroscope" in input_type:
                f.write(gyroscope_fs + ",")  
                f.write(gyroscope_odr + ",")

            f.write('\n')
            f.write('%d\n' % (n_decision_trees))  ## Number of decision trees
            f.write('%d\n' % (window_length))  ## Window length (supported values: from 1 to 255)

            # Filters
            """
            for i in range(len(filters_list)):
                if filters_list[i].name not in mlc_configurator.get_filter_names(input_type):
                    logging.error("ERROR: filter \"" + filters_list[i].name + "\" not supported")
                    return
                f.write("<"+ filters_list[i].filter_id +">" + filters_list[i].name + "\n")
                if "BP" in filters_list[i].name:
                    f.write("<coefficients>" + 
                            str(filters_list[i].coef_a2) + "," + 
                            str(filters_list[i].coef_a3) + "," + 
                            str(filters_list[i].coef_gain) + "\n")
                elif "IIR1" in filters_list[i].name:
                    f.write("<coefficients>" + 
                            str(filters_list[i].coef_b1) + "," + 
                            str(filters_list[i].coef_b2) + "," + 
                            str(filters_list[i].coef_a2) + "\n")
                elif "IIR2" in filters_list[i].name:
                    f.write("<coefficients>" + 
                            str(filters_list[i].coef_b1) + "," + 
                            str(filters_list[i].coef_b2) + "," + 
                            str(filters_list[i].coef_b3) + "," + 
                            str(filters_list[i].coef_a2) + "," + 
                            str(filters_list[i].coef_a3) + "\n")
            """
            f.write("<filter>" + "END_FILTERS" + "\n") 

            # Features
            for i in range(len(self.composantes)):
                for j in range(len(self.features)):
                    f.write("<feature>" + self.features[j] + "_" + self.composantes[i] + "\n")
            f.write("<feature>" + "END_FEATURES" + "\n") 
            f.write(self.arff_filename + "\n")
            f.write("EXIT_APP")
            f.close()




def sum_for_features(_array, _composante, _start_index, _window_length):
    sum_ = 0
    for i in range(_start_index, _start_index + _window_length):
        sum_ += _array[_composante][i]
    return sum_

def energy_feature(_array, _composante, _start_index, _window_length):
    energy = 0
    for i in range(_start_index, _start_index + _window_length):
        energy += _array[_composante][i] ** 2

    if(_composante == 0 or _composante == 1 or _composante == 2):
        return energy/1000
    else:
        return conversion_dps_to_rads(energy)

def mean_feature(_array, _composante, _start_index, _window_length):
    sum_ = sum_for_features(_array, _composante, _start_index, _window_length)
    return sum_/_window_length #mean

def variance_feature(_array, _composante, _start_index, _window_length):
    energy = energy_feature(_array, _composante, _start_index, _window_length)
    mean = mean_feature(_array, _composante, _start_index, _window_length)

    if(_composante == 0 or _composante == 1 or _composante == 2):
        variance = (energy*1000)/_window_length - mean ** 2
        return conversion_mg_to_g(variance)
    else:
        variance = energy/(2*np.pi)*360/_window_length - mean ** 2
        return conversion_dps_to_rads(variance)

def max_feature(_array, _composante, _start_index, _window_length):
    max_ = -100000
    for i in range(_start_index, _start_index + _window_length):
        if(_array[_composante][i] > max_):
            max_ = _array[_composante][i]
    return max_

def min_feature(_array, _composante, _start_index, _window_length):
    min_ = 100000
    for i in range(_start_index, _start_index + _window_length):
        if(_array[_composante][i] < min_):
            min_ = _array[_composante][i]
    return min_ 

def peak_to_peak_feature(_array, _composante, _start_index, _window_length):
    min_ = min_feature(_array, _composante, _start_index, _window_length)
    max_ = max_feature(_array, _composante, _start_index, _window_length)

    peak_to_peak = max_ - min_
    
    return peak_to_peak

def convert_value(_composante, _value):
    if(_composante == 0 or _composante == 1 or _composante == 2):
        return conversion_mg_to_g(_value)
    elif(_composante == 3 or _composante == 4 or _composante == 5):
        return conversion_dps_to_rads(_value)

def conversion_mg_to_g(_value):
    return _value/1000

def conversion_dps_to_rads(_value):
    return _value*2*np.pi/360