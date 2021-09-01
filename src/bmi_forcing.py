#! /usr/bin/env python
"""Basic Model Interface implementation for the 2D heat model."""

import numpy as np
from bmipy import Bmi
#import sys
from read_forcing_object import Forcing
BMI_SUCCESS = 1

class BmiForcing(Bmi):

    """Read Forcing"""

    _name = "Forcing BMI"
    _input_var_names = ()
    
    _output_var_names = ("land_surface_radiation~incoming~longwave__energy_flux",
    "land_surface_air__pressure",
    "atmosphere_air_water~vapor__relative_saturation",
    "atmosphere_water__liquid_equivalent_precipitation_rate",
    "land_surface_radiation~incoming~shortwave__energy_flux",
    "land_surface_air__temperature",
    "land_surface_wind__x_component_of_velocity",
    "land_surface_wind__y_component_of_velocity")

    # types array unneeded as we are directly calling python's dtype    
    #_output_var_types = ("float","float","float","float","float","float","float","float")    
    #_output_var_item_count = (1,1,1,1,1,1,1,1)
    #_output_var_units = ("W m-2","Pa","kg kg-1","kg m-2","W m-2","K","m s-1","m s-1")     
    #_output_var_grids = (0,0,0,0,0,0,0,0)
    #_output_var_locations = ("node","node","node","node","node","node","node","node","node")

    #------------------------------------------------------
    # Create a Python dictionary that maps CSDMS Standard
    # Names to the model's internal variable names.
    #------------------------------------------------------
    _var_name_map = { 
         'land_surface_radiation~incoming~longwave__energy_flux':'LWDOWN',
         'land_surface_air__pressure':'PSFC',
         'atmosphere_air_water~vapor__relative_saturation':'Q2D',
         'atmosphere_water__liquid_equivalent_precipitation_rate':'RAINRATE',
         'land_surface_radiation~incoming~shortwave__energy_flux':'SWDOWN',
         'land_surface_air__temperature':'T2D',
         'land_surface_wind__x_component_of_velocity':'U2D',
         'land_surface_wind__y_component_of_velocity':'V2D'}
    #------------------------------------------------------
    # Create a Python dictionary that maps CSDMS Standard
    # Names to the units of each model variable.
    #------------------------------------------------------
    _var_units_map = {
         'land_surface_radiation~incoming~longwave__energy_flux':'W m-2',
         'land_surface_air__pressure':'Pa',
         'atmosphere_air_water~vapor__relative_saturation':'kg kg-1',
         'atmosphere_water__liquid_equivalent_precipitation_rate':'kg m-2',
         'land_surface_radiation~incoming~shortwave__energy_flux':'W m-2',
         'land_surface_air__temperature':'K',
         'land_surface_wind__x_component_of_velocity':'m s-1',
         'land_surface_wind__y_component_of_velocity':'m s-1'}    
    
    def __init__(self):
        """Create a BmiForcing model that is ready for initialization."""
        self._model = None
        #self._values = {}
        #self._var_units = {}
        # this 2 could be mapped dictionary but all are same
        self._var_loc = "node" 
        self._grids = 0
        self._grid_type = {0: "scalar"}
        
        self._start_time_index = 0.0
        self._end_time_index = np.finfo("d").max
        self._current_time_index = 0
        self._time_units = "s"
        self._time_step = 3600

    def initialize(self, filename=None):
        """Initialize the Forcing model.

        Parameters
        ----------
        filename : str, optional
            Path to name of input file.
        """
        from datetime import datetime
        
        if filename is None:
            self._model = Forcing()
        # elif isinstance(filename, str):
        #     with open(filename, "r") as file_obj:
        #         self._model = Forcing.read_config(file_obj.read())
        else:
            self._model = Forcing.read_config(filename)  
        
        if(getattr(self._model,'_Debug')==1):print ("start time: " + str(datetime.fromisoformat(self._model._start_time_date)))    
        if(getattr(self._model,'_Debug')==1):print ("end time:   " + str(datetime.fromisoformat(self._model._end_time_date)))
        self._end_time_index = int((datetime.fromisoformat(self._model._end_time_date)-datetime.fromisoformat(self._model._start_time_date)).total_seconds()/3600.)

        # self._values = {"plate_surface__temperature": self._model.temperature}
        # self._var_units = {"plate_surface__temperature": "K"}
        # self._var_loc = {"plate_surface__temperature": "node"}
        # self._grids = {0: ["plate_surface__temperature"]}
        # self._grid_type = {0: "uniform_rectilinear"}
        
        self._model.read_forcing()        
        
        if(getattr(self._model,'_Debug')==1): print(getattr(self._model,'_time_series_df'))       
        return BMI_SUCCESS;       

    def update(self):
        """Advance model by one time step."""
        #Done - LKC        
        self._current_time_index=self._current_time_index+1
        
        return BMI_SUCCESS;

    def update_until(self, then):
        """Update model until a particular time.

        Parameters
        ----------
        then : float
            Time to run model until.
        """
        #Done - LKC 
        n_steps = (then - self.get_current_time()) / self.get_time_step()

        for _ in range(int(n_steps)):
            self.update()

        return BMI_SUCCESS;       
        

    def finalize(self):
        """Finalize model."""
        #Done - LKC 
        self._model = None
        return BMI_SUCCESS;       


    def get_value_ptr(self, var_name):
        #Done - LKC 
        """Reference to values.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.

        Returns
        -------
        array_like
            Value array.
        """
        #print(self._var_name_map[var_name])
        #print("This is the current time " + str(self._current_time_index))
        return getattr(self._model,'_time_series_df')[self._var_name_map[var_name]].iloc[self._current_time_index]
    
    def get_var_type(self, var_name):
        """Data type of variable.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.

        Returns
        -------
        str
            Data type.
        """
        return str(self.get_value_ptr(var_name).dtype)

    def get_var_units(self, var_name):
        """Get units of variable.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.

        Returns
        -------
        str
            Variable units.
        """
        return self._var_units_map[var_name]

    def get_var_nbytes(self, var_name):
        """Get units of variable.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.

        Returns
        -------
        int
            Size of data array in bytes.
        """
        return self.get_value_ptr(var_name).nbytes

    def get_var_itemsize(self, name):
        return np.dtype(self.get_var_type(name)).itemsize

    def get_var_location(self, name):
        
        if name in self._output_var_names:
            return self._var_loc

    def get_var_grid(self, var_name):
        """Grid id for a variable.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.

        Returns
        -------
        int
            Grid id.
        """
        # for grid_id, var_name_list in self._grids.items():
        #     if var_name in var_name_list:
        #         return grid_id
        
        if var_name in self._output_var_names:
            return self._grids  

    def get_grid_rank(self, grid_id):
        """Rank of grid.

        Parameters
        ----------
        grid_id : int
            Identifier of a grid.

        Returns
        -------
        int
            Rank of grid.
        """
        if grid_id == 0:
            return 1

    def get_grid_size(self, grid_id):
        """Size of grid.

        Parameters
        ----------
        grid_id : int
            Identifier of a grid.

        Returns
        -------
        int
            Size of grid.
        """
        if grid_id == 0:
            return 1


    def get_value(self, var_name, dest):
        """Copy of values.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        dest : ndarray
            A numpy array into which to place the values.

        Returns
        -------
        array_like
            Copy of values.
        """
        dest[:] = self.get_value_ptr(var_name).flatten()
        return dest

    def get_value_at_indices(self, var_name, dest, indices):
        """Get values at particular indices.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        dest : ndarray
            A numpy array into which to place the values.
        indices : array_like
            Array of indices.

        Returns
        -------
        array_like
            Values at indices.
        """
        dest[:] = self.get_value_ptr(var_name).take(indices)
        return dest

    def set_value(self, var_name, src):
        """Set model values.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        src : array_like
            Array of new values.
        """
        val = self.get_value_ptr(var_name)
        val[:] = src

    def set_value_at_indices(self, name, inds, src):
        """Set model values at particular indices.

        Parameters
        ----------
        var_name : str
            Name of variable as CSDMS Standard Name.
        src : array_like
            Array of new values.
        indices : array_like
            Array of indices.
        """
        val = self.get_value_ptr(name)
        val.flat[inds] = src

    def get_component_name(self):
        """Name of the component."""
        return self._name

    def get_input_item_count(self):
        """Get names of input variables."""
        return len(self._input_var_names)

    def get_output_item_count(self):
        """Get names of output variables."""
        return len(self._output_var_names)

    def get_input_var_names(self):
        """Get names of input variables."""
        return self._input_var_names

    def get_output_var_names(self):
        """Get names of output variables."""
        return self._output_var_names

    def get_grid_shape(self, grid_id, shape):
        raise NotImplementedError("get_grid_shape")

    def get_grid_spacing(self, grid_id, spacing):
        raise NotImplementedError("get_grid_spacing")

    def get_grid_origin(self, grid_id, origin):
        raise NotImplementedError("get_grid_origin")

    def get_grid_type(self, grid_id):
        """Type of grid."""
        return self._grid_type[grid_id]

    def get_start_time(self):
        """Start time of model."""
        return self._start_time_index

    def get_end_time(self):
        """End time of model."""
        return self._end_time_index

    def get_current_time(self):
        return self._current_time_index

    def get_time_step(self):
        return self._time_step

    def get_time_units(self):
        return self._time_units

    def get_grid_edge_count(self, grid):
        raise NotImplementedError("get_grid_edge_count")

    def get_grid_edge_nodes(self, grid, edge_nodes):
        raise NotImplementedError("get_grid_edge_nodes")

    def get_grid_face_count(self, grid):
        raise NotImplementedError("get_grid_face_count")

    def get_grid_face_nodes(self, grid, face_nodes):
        raise NotImplementedError("get_grid_face_nodes")

    def get_grid_node_count(self, grid):
        raise NotImplementedError("get_grid_node_count")

    def get_grid_nodes_per_face(self, grid, nodes_per_face):
        raise NotImplementedError("get_grid_nodes_per_face")

    def get_grid_face_edges(self, grid, face_edges):
        raise NotImplementedError("get_grid_face_edges")

    def get_grid_x(self, grid, x):
        raise NotImplementedError("get_grid_x")

    def get_grid_y(self, grid, y):
        raise NotImplementedError("get_grid_y")

    def get_grid_z(self, grid, z):
        raise NotImplementedError("get_grid_z")



    