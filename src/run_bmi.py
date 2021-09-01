"""Run BMI Forcing Data Model.
Author: jgarrett
Date: 08/31/2021"""

import os
from bmi_forcing import BmiForcing

bmi=BmiForcing()

# Define config path
cfg_file=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data','forcing_config.yaml'))

bmi.initialize(cfg_file)

if(getattr(bmi._model,'_Debug')==1):
    print ("get_start_time: " + str(bmi.get_start_time()))
    print ("get_end_time:   " + str(bmi.get_end_time()))

    print("\nMODEL INFORMATION\n*****************")
    print (" component name: " + bmi.get_component_name())
    #print (" input item count: " + str(bmi.get_input_item_count()))
    print (" output item count: " + str(bmi.get_output_item_count()))
    #print (" input var names: " + bmi.get_input_var_names())
    print (" output var names: ")
    for n in bmi.get_output_var_names():
        print ("  " + n)
    
    print("\nVARIABLE INFORMATION\n********************")
    for var_name in bmi.get_output_var_names():  
        print (" " + var_name)
        print ("  units: " + bmi.get_var_units(var_name))
        print ("  itemsize: " + str(bmi.get_var_itemsize(var_name)))
        print ("  type: " + bmi.get_var_type(var_name))
        print ("  nbytes: " + str(bmi.get_var_nbytes(var_name)))
        print ("  grid: " + str(bmi.get_var_grid(var_name)))
        print ("  location: " + bmi.get_var_location(var_name))
        
    print("\nGRID INFORMATION\n****************")
    grid_id = 0 #there is only 1
    print (" grid_id: " + str(grid_id))
    print ("  rank: " + str(bmi.get_grid_rank(grid_id)))
    print ("  size: " + str(bmi.get_grid_size(grid_id)))
    print ("  type: " + bmi.get_grid_type(grid_id))
    
    #print("\nTIME INFORMATION\n****************\n")

for _ in range(5):
    bmi.update()
    if(getattr(bmi._model,'_Debug')==1):
        print ("\nget_current_time: " + str(bmi.get_current_time()))
        for var_name in bmi.get_output_var_names():  
            print (" " + var_name + ": " + str(bmi.get_value_ptr(var_name)))

bmi.finalize()        
    