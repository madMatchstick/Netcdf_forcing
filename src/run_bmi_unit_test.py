"""Run BMI Forcing Data Model.
Author: jgarrett
Date: 08/31/2021"""

import os
import sys
import numpy as np
from bmi_forcing import BmiForcing


# setup a "success counter" for number of passing and failing bmi functions
# keep track of funciton fails
pass_count = 0
fail_count = 0
fail_list = []

def bmi_except(fstring):
    """Prints message and updates counter and list

    Parameters
    ----------
    fstring : str
        Name of failing BMI function 
    """
    
    global fail_count, fail_list
    print(" *BMI ERROR* in " + fstring)
    fail_count += 1
    fail_list.append(fstring)

bmi=BmiForcing()

print("\nBEGIN BMI UNIT TEST\n*******************\n");

# Define config path
cfg_file=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data','forcing_config.yaml'))

if os.path.exists(cfg_file):
    print(" configuration found: " + cfg_file)
else:
    print(" no configuration found, exiting...")
    sys.exit()

# initialize()
print(" initializing...");
try: 
    bmi.initialize(cfg_file)
    pass_count += 1
except:
    bmi_except('initialize()')

print("\nMODEL INFORMATION\n*****************")

# get_component_name()
try:
    print (" component name: " + bmi.get_component_name())
    pass_count += 1
except:
    bmi_except('get_component_name()')

# get_input_item_count()
try:
    print (" input item count: " + str(bmi.get_input_item_count()))
    pass_count += 1
except:
    bmi_except('get_input_item_count()')

# get_output_item_count()
try:
    print (" output item count: " + str(bmi.get_output_item_count()))
    pass_count += 1
except:
    bmi_except('get_output_item_count()')

# get_input_var_names()
try:    
    # only print statement if names exist
    test_get_input_var_names =  bmi.get_input_var_names()
    if len(test_get_input_var_names) > 0:
        print (" input var names: ")
        for var_in in test_get_input_var_names:
            print ("  " + var_in)
    pass_count += 1
except:
    bmi_except('get_input_var_names()')

# get_input_var_names()
try:    
    # only print statement if out var list not null
    test_get_output_var_names =  bmi.get_output_var_names()
    if len(test_get_output_var_names) > 0:
        print (" output var names: ")
        for var_out in test_get_output_var_names:
            print ("  " + var_out)
    pass_count += 1
except:
    bmi_except('get_output_item_count()')
    
print("\nVARIABLE INFORMATION\n********************")

for var_name in (bmi.get_output_var_names()+bmi.get_input_var_names()):  
    print (" " + var_name)

    # get_var_units()
    try: 
        print ("  units: " + bmi.get_var_units(var_name))
        pass_count += 1
    except:
        bmi_except('get_var_units()')
    
    # get_var_itemsize()
    try:
        print ("  itemsize: " + str(bmi.get_var_itemsize(var_name)))
        pass_count += 1
    except:
        bmi_except('get_var_itemsize')

    # get_var_type()
    try:
        print ("  type: " + bmi.get_var_type(var_name))
        pass_count += 1
    except:
        bmi_except('get_var_type')

    # get_var_nbytes()
    try:
        print ("  nbytes: " + str(bmi.get_var_nbytes(var_name)))
        pass_count += 1
    except:
        bmi_except('get_var_nbytes')

    # get_var_grid
    try:
        print ("  grid id: " + str(bmi.get_var_grid(var_name)))
        pass_count += 1
    except:
        bmi_except('get_var_grid')

    # get_var_location
    try:
        print ("  location: " + bmi.get_var_location(var_name))
        pass_count += 1
    except:
        bmi_except('get_var_location')


print("\nGRID INFORMATION\n****************")
grid_id = 0 # there is only 1
print (" grid id: " + str(grid_id))

# get_grid_rank()
try:
    print ("  rank: " + str(bmi.get_grid_rank(grid_id)))
    pass_count += 1
except:
    bmi_except('get_grid_rank')

# get_grid_size()
try:    
    print ("  size: " + str(bmi.get_grid_size(grid_id)))
    pass_count += 1
except:
    bmi_except('get_grid_size')

# get_grid_type()    
try:
    print ("  type: " + bmi.get_grid_type(grid_id))
    pass_count += 1
except:
    bmi_except('get_grid_type')    

print("\nTIME INFORMATION\n****************")
print (" start time: " + str(bmi.get_start_time()))
print (" end time: " + str(bmi.get_end_time()))
print (" time step: " + str(bmi.get_time_step()))
print (" time units: " + bmi.get_time_units())

dest0 = np.empty(bmi.get_grid_size(0), dtype=float)
dest1 = np.empty(1, dtype=float)

for _ in range(5):
    bmi.update()
    print ("\nget_current_time: " + str(bmi.get_current_time()))
    for var_name in bmi.get_output_var_names():  
        print (" " + var_name + ":" )
        print ("  get value ptr: " + str(bmi.get_value_ptr(var_name)))
        print ("  get value: " + str(bmi.get_value(var_name, dest0)))
        try: 
            test_get_value_at_indices = bmi.get_value_at_indices(var_name, dest1, [1])
            print ("  get value at indices: " + str( test_get_value_at_indices))
        except: 
            bmi_except('get_value_at_indices')
bmi.update_until(100000)
print ("\nget_current_time: " + str(bmi.get_current_time()))

bmi.finalize()        
    