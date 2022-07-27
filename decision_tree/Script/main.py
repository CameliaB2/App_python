import os, datetime
from ucf_converter import *

from command_parameters import *

current_directory = os.getcwd().replace('Script', 'Trees')
current_directory = os.path.join(current_directory, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
os.makedirs(current_directory)

from mlc_script_log import *
logger = Logger(current_directory, "")
logging.info("Current directory: " + current_directory)


arff_filename = os.path.join(current_directory, "features.arff")

# private import:
import mlc_configurator
from mlc_configurator import *
import decision_tree_generator
from decision_tree_generator import generateDecisionTree
from decision_tree_generator import generate_subset_of_ARFF
import mlc_test
from mlc_test import *    
from arff_generator import *

device_name = "LSM6DSOX"    ## list of supported devices available with mlc_configurator.get_devices()

# device settings
#mlc_odr = "26 Hz"                        ## list of allowed values available with mlc_configurator.get_mlc_odr(device_name)
#input_type = "accelerometer+gyroscope"   ## list of allowed values available with mlc_configurator.get_mlc_input_type(device_name)
#accelerometer_fs = "2 g"                 ## list of allowed values available with mlc_configurator.get_accelerometer_fs(device_name)
#accelerometer_odr = "26 Hz"              ## list of allowed values available with mlc_configurator.get_accelerometer_odr(device_name)
#gyroscope_fs = "2000 dps"                ## list of allowed values available with mlc_configurator.get_gyroscope_fs(device_name)
#gyroscope_odr = "26 Hz"                  ## list of allowed values available with mlc_configurator.get_gyroscope_odr(device_name)            
#window_length = 39                       ## Window length (supported values: from 1 to 255)



#####
# ARGUMENTS MANAGE
# Parsing argument
cmd_checking = cmd_parameters()
window_length, mlc_odr, accelerometer_odr, accelerometer_fs, gyroscope_fs, gyroscope_odr, input_type, _name = cmd_checking.check_args_value()


#############################
ucf_filename = os.path.join(current_directory, _name +".ucf")
h_filename = os.path.join(current_directory, _name +".h")



result_names  = [] # leave empty here
result_values = [] # leave empty here
datalog_results = [] # leave empty here


# Load class names (folder names) from Logs folder
direct = os.listdir("../Logs/")
print ("available classes = ", direct)

#filenames = next(os.walk(direct), (None, None, []))[1] # 2: Get all files | 1: Get all directories
class_names = list(filter(lambda file: not("DS_Store") in file, direct))


# For each class (folder), load all data (files in the folder)
datalogs = []
datalogs_split_by_class = []
for class_name in class_names:
    datalogs_i = os.listdir("../Logs/" + class_name +"/")
    print(class_name, " --> data logs: ", datalogs_i)
    datalogs_split_by_class.append(datalogs_i)
    for datalog_i in datalogs_i:
        datalogs.append("../Logs/" + class_name + "/" + datalog_i)
        datalog_results.append(class_name);
print("All data logs: ", datalogs)
print("All data logs 0: ", datalogs[0])

# Assign results and values for decision tree 1:
result_names.append(  class_names )
result_values.append( list(range(0, len(class_names), 1)) )
# Assign results and values for decision tree 2:
result_names.append(  [] )
result_values.append( [] )
# Assign results and values for decision tree 3:
result_names.append(  [] )
result_values.append( [] )
# Assign results and values for decision tree 4:
result_names.append(  [] )
result_values.append( [] )
# Assign results and values for decision tree 5:
result_names.append(  [] )
result_values.append( [] )
# Assign results and values for decision tree 6:
result_names.append(  [] )
result_values.append( [] )
# Assign results and values for decision tree 7:
result_names.append(  [] )
result_values.append( [] )
# Assign results and values for decision tree 8:
result_names.append(  [] )
result_values.append( [] )



dectree_filenames = []
for i in range(0,8): 
    if not result_names[i]:
        break
    else: 
        dectree_filenames.append(os.path.join(current_directory, "dectree{}.txt".format(i+1)))
n_decision_trees = i
logging.info('n_decision_trees = %d' % (n_decision_trees))


############


# filters configuration
# the list of available filters can be obtained with mlc_configurator.get_filter_names(input_type)
filters_list = []   
#filters_list.append(mlc_configurator.mlc_filter("filter_1", "HP_Acc_XYZ"))
#filters_list.append(mlc_configurator.mlc_filter("filter_2", "BP_Acc_V", coef_a2=-0.5, coef_a3=0.5, coef_gain=1))
#filters_list.append(mlc_configurator.mlc_filter("filter_3", "IIR1_Acc_V", coef_b1=1, coef_b2=0.25, coef_a2=0.75))
#filters_list.append(mlc_configurator.mlc_filter("filter_4", "IIR2_Acc_V", coef_b1=0.59, coef_b2=1.19, coef_b3=0.59, coef_a2=-1.01, coef_a3=0.36))

# features configuration
# full list of available features can be obtained with mlc_configurator.get_feature_names()
# full list of available inputs can be obtained with   mlc_configurator.get_mlc_inputs(device_name, input_type)
features_list = []

arff_calculus = Arff_generator()

composantes = ["Acc_X", "Acc_Y", "Acc_Z", "Gyr_X", "Gyr_Y", "Gyr_Z"]
if input_type == 'accelerometer_only':
    composantes = ["Acc_X", "Acc_Y", "Acc_Z"]
arff_calculus.set_composantes(composantes)


for c in composantes:
  features_list.append(mlc_configurator.mlc_feature("MEAN", c))
  #features_list.append(mlc_configurator.mlc_feature("MINIMUM", c))
  #features_list.append(mlc_configurator.mlc_feature("MAXIMUM", c))
  #features_list.append(mlc_configurator.mlc_feature("PEAK_TO_PEAK", c))
  #features_list.append(mlc_configurator.mlc_feature("VARIANCE", c))
  #features_list.append(mlc_configurator.mlc_feature("ENERGY", c))

"""
features_list.append(mlc_configurator.mlc_feature("ZERO_CROSSING", "Acc_V", 0.5))
features_list.append(mlc_configurator.mlc_feature("POSITIVE_ZERO_CROSSING", "Acc_V", 0.5))
features_list.append(mlc_configurator.mlc_feature("NEGATIVE_ZERO_CROSSING", "Acc_V", 0.5))
features_list.append(mlc_configurator.mlc_feature("PEAK_DETECTOR", "Acc_V", 0.5))
features_list.append(mlc_configurator.mlc_feature("POSITIVE_PEAK_DETECTOR", "Acc_V", 0.5))
features_list.append(mlc_configurator.mlc_feature("NEGATIVE_PEAK_DETECTOR", "Acc_V", 0.5))
features_list.append(mlc_configurator.mlc_feature("ZERO_CROSSING", "Gyr_V", 0.5))
features_list.append(mlc_configurator.mlc_feature("POSITIVE_ZERO_CROSSING", "Gyr_V", 0.5))
features_list.append(mlc_configurator.mlc_feature("NEGATIVE_ZERO_CROSSING", "Gyr_V", 0.5))
features_list.append(mlc_configurator.mlc_feature("PEAK_DETECTOR", "Gyr_V", 0.5))
features_list.append(mlc_configurator.mlc_feature("POSITIVE_PEAK_DETECTOR", "Gyr_V", 0.5))
features_list.append(mlc_configurator.mlc_feature("NEGATIVE_PEAK_DETECTOR", "Gyr_V", 0.5))
"""

# Some examples of features on filtered inputs: 
#features_list.append(mlc_configurator.mlc_feature("MEAN","Acc_X_filter_1"))
#features_list.append(mlc_configurator.mlc_feature("ENERGY", "Acc_V_filter_2"))
#features_list.append(mlc_configurator.mlc_feature("ZERO_CROSSING", "Acc_V_filter_3", 0.5))



mlc_configurator.arff_generator( arff_calculus=arff_calculus,
               device_name = device_name, 
               datalogs = datalogs, 
               results = datalog_results, 
               mlc_odr = mlc_odr, 
               input_type = input_type, 
               accelerometer_fs = accelerometer_fs, 
               accelerometer_odr = accelerometer_odr, 
               gyroscope_fs = gyroscope_fs, 
               gyroscope_odr = gyroscope_odr, 
               n_decision_trees = n_decision_trees, 
               window_length = window_length, 
               filters_list = filters_list,  
               features_list = features_list, 
               arff_filename = arff_filename, 
               current_directory = current_directory)




###########################



if (n_decision_trees == 1):
    dectree_accuracy, dectree_nodes = decision_tree_generator.generateDecisionTree(
                                                        arff_filename = arff_filename, 
                                                        dectree_filename = dectree_filenames[0],
                                                        arff_calculus = arff_calculus)
else:
    for i in range(n_decision_trees) :
        arff_filename_i = arff_filename + str(i+1)
        decision_tree_generator.generate_subset_of_ARFF( arff_filename = arff_filename, 
                                                         arff_subset_filename = arff_filename_i, 
                                                         classes_subset = result_names[i] )
        logging.info("\n# Decision Tree %d:" %(i+1))
        dectree_accuracy, dectree_nodes = decision_tree_generator.generateDecisionTree( 
                                               arff_filename = arff_filename_i, 
                                               dectree_filename = dectree_filenames[i],
                                               arff_calculus = arff_calculus )



###################

# Meta-classifiers
# metaclassifierX_values contains the end counter values of the meta classifier associated to the decision tree 'X'
# 4 end counter values are available in LSM6DSOX (the first 4 values in "metaclasifierX_values")
# 8 end counter values are available in LSM6DSRX/ISM330DHCX (the 8 values in "metaclasifierX_values")
# values allowed for end counters are from 0 to 14
metaclassifier1_values = "0,0,0,0,0,0,0,0"
metaclassifier2_values = "0,0,0,0,0,0,0,0"
metaclassifier3_values = "0,0,0,0,0,0,0,0"
metaclassifier4_values = "0,0,0,0,0,0,0,0"
metaclassifier5_values = "0,0,0,0,0,0,0,0"
metaclassifier6_values = "0,0,0,0,0,0,0,0"
metaclassifier7_values = "0,0,0,0,0,0,0,0"
metaclassifier8_values = "0,0,0,0,0,0,0,0"
metaclassifier_values = [metaclassifier1_values, metaclassifier2_values, metaclassifier3_values, metaclassifier4_values, metaclassifier5_values, metaclassifier6_values, metaclassifier7_values, metaclassifier8_values]

mlc_configurator.ucf_generator( arff_calculus = arff_calculus,
                                device_name = device_name, 
                                arff_filename = arff_filename, 
                                dectree_filenames = dectree_filenames,
                                result_names = result_names, 
                                result_values = result_values, 
                                metaclassifier_values = metaclassifier_values, 
                                ucf_filename = ucf_filename, 
                                current_directory = current_directory )
                                
convert_ucf_to_h(_name, ucf_filename, h_filename)
