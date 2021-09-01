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

for _ in range(20):
    bmi.update()
    if(getattr(bmi._model,'_Debug')==1):
        print ("\nget_current_time: " + str(bmi.get_current_time()))
        print ("LWDOWN: " + str(bmi.get_value_ptr('land_surface_radiation~incoming~longwave__energy_flux')))

bmi.finalize()        
    