"""Read Forcing data.
Author: lcunha
Date: 08/19/2021"""

import yaml
from datetime import datetime
import pandas as pd
class Forcing(object):

    def __init__(
        self, 
        STAND_ALONE=1,
        start_time_date="2007-01-01 05:00:00", 
        end_time_date="2007-01-10 05:00:00",
        Netcdf_File=None,
        Debug=1
    ):    
        """Create a new Forcing model."""
        
        self._STAND_ALONE = STAND_ALONE
        self._start_time_date = start_time_date
        self._end_time_date = end_time_date
        self._Netcdf_File = Netcdf_File     
        self._Debug = Debug          
        self._time_series_df = pd.DataFrame()
        self._long_name = []
        self._units = []
        self._time = 0.0
        self._time_step = 1.0
    def time(self):
        """Current model time."""
        return self._time
        
    @classmethod
    def read_config(cls, file_like):
        """Create a Forcing object from a file-like object.
        Parameters
        ----------
        file_like : file_like
            Input parameter file.
        Returns
        -------
        Forcing
            A new instance of a Forcing object.
            """

        with open(file_like) as f:
            config = yaml.safe_load(f)        
        return cls(**config)    
    
    def read_forcing(self):
        
        """Reads netcdf for specific time window  """
        import netCDF4 as netcdf

        #print (self._Netcdf_File)
        nc = netcdf.Dataset(self._Netcdf_File)
        #varsInFile = nc.variables.keys()
        time_units = nc.variables['Time'].units
        #Cat_ID=nc['catID'][:]
        vname=['RAINRATE', 'T2D', 'Q2D', 'U2D', 'V2D', 'PSFC', 'SWDOWN', 'LWDOWN']
    
        if("hours since " in time_units):
            date_from=datetime.fromisoformat(time_units.replace("hours since ",""))
            #print (date_from)
        else:
            #print ("Check units ")
            exit(0)
        index_beg=int((datetime.fromisoformat(self._start_time_date)-date_from).total_seconds()/3600)
        #print (index_beg)
        if(self._end_time_date==-9):
            index_end=index_beg+1
        else:
            index_end=int((datetime.fromisoformat(self._end_time_date)-date_from).total_seconds()/3600)
        #print (index_end)
        for v in vname:
            Temp_df=pd.DataFrame(nc.variables[v][index_beg:index_end].data,columns=[v])
            self._time_series_df = pd.concat([self._time_series_df, Temp_df], axis=1)
            self._long_name.append(nc.variables[v].long_name)
            self._units.append(nc.variables[v].units)
 
    # def advance_in_time(self):
    #     """Move cursor"""
    #
        
    #     self._time += self._time_step
        
