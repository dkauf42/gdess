# -*- coding: utf-8 -*-
"""
Created September 2020

@author: Daniel E. Kaufman

This code is meant to serve as a collection of tools for use with the CO2 diagnostics development
Most of the routines are designed to work with xarray.DataArray types
"""

import os
import numpy as np
import xarray as xr

import logging
_logger = logging.getLogger(__name__)

# Define functions to be imported by *, e.g. from the local __init__ file
#   (also to avoid adding above imports to other namespaces)
__all__ = ['print_var_summary', 'get_var_stats', 'shared_constants']


def where_am_i():
    return os.path.dirname(os.path.abspath(__file__))


def print_var_summary(dataset: xr.Dataset, varname='CO2', return_dataset=False):
    """Brief stats for a dataset variable are printed.

    :param dataset:
    :param varname:
    :param return_dataset:
    :return:
    """
    # We check if there are units specified for this variable
    vu = None
    if 'units' in dataset[varname].attrs:
        vu = dataset[varname].units
    # We check if there is a long name specified for this variable
    ln = None
    if 'long_name' in dataset[varname].attrs:
        ln = dataset[varname].long_name

    stats_dict = get_var_stats(dataset[varname])

    _logger.info("Summary for <%s>%s%s:",
                 varname,
                 ' (units of ' + vu + ')' if vu else '',
                 ' (long_name: ' + ln + ')' if ln else '')
    _logger.info("  min: %s", str(stats_dict['min']))
    _logger.info("  mean: %s", str(stats_dict['mean']))
    _logger.info("  max: %s", str(stats_dict['max']))

    my_shape = dataset[varname].shape
    dim_strings = [f"{d}: {my_shape[i]}" for i, d in enumerate(dataset[varname].dims)]
    _logger.info("  shape: (" + ', '.join(dim_strings) + ")")

    if return_dataset:
        return dataset


def get_var_stats(dataarray):
    """ Provides a dictionary with summary statistics

    Input:
        XArray DataArray

    Returns:
        Dict
    """
    return {
        'min': dataarray.min().values.item(),
        'mean': dataarray.mean().values.item(),
        'max': dataarray.max().values.item()
    }

#%% [markdown]
# **$\Delta{mass_{CO_2}}$ - change in mass of $CO_2$ from timestep to timestep**

# \begin{align*}
#     && \Delta \texttt{glmean_TMCO2}_{t} = \texttt{glmean_TMCO2}_{t} - \texttt{glmean_TMCO2}_{t-1} && \forall t
# \end{align*}

# note: using TMCO2_FFF instead of TMCO2 because it is instantaneous value at end of month instead of a monthly mean

# <span style="color:blue">note from Bryce: </span>
# *When the output is specified to be written as instantaneous, then the value is equal to whatever the model value is when the output is written.  For monthly output, that would be at the end of the month.  Since SFCO2 = SFCO2_FFF (because the land and ocean fluxes are zero), then TMCO2 should be equal to TMCO2_FFF.  However, since TMCO2 is written out as a monthly average while TMCO2_FFF is equal to the value of TMCO2_FFF at the end of the month, they will differ some.  The change in TMCO2_FFF from the end of one month to the end of the next month should be exactly equal to the time-integrated fluxes of SFCO2_FFF over the course of that month (technically equal up to the numerical precision of the output data).*

#
# def shared_constants():
#     constants = {
#     'radius_earth'        : 6.37122e6,              # m -- value from the Common Infrastructure for Modeling the Earth (CIME)
#     'surface_area_earth'  : 4*np.pi*(6.37122e6**2), # m^2
#     'grav'                : 9.80616,                # m/s^2
#     'tsidereal'           : 86164.0,                # s  (sidereal day)
#     'sigb'                : 5.67e-8,                # W/m^2/K^4
#     'kboltz'              : 1.38065e-23,            # J/K (Boltzmann constant)
#     'Navo'                : 6.02214e23,             # molec/mol (Avogadro's number)
#     'mair'                : 0.028966,               # kg/mol (Molecular weight of dry air)
#     'mvap'                : 0.018016,               # kg/mol (Molecular weight of water vapor)
#     'Cpd'                 : 1.00464e3,              # J/kg/K (dry air specific heat)
#     'kappa'               : 2./5.,                  # Von Karman constant
#     'Lv'                  : 2.501e6,                # J/kg (Latent heat of vaporization)
#     'Lf'                  : 3.337e5,                # J/kg (Latent heat of fusion)
#     'rh2o'                : 1e3,                    # kg/m^3 (Density of water)
#     'Cpv'                 : 1.81e3,                 # J/kg/K (water vapor specific heat)
#     'Cl'                  : 4.188e3,                # J/kg/K (liquid water specific heat)
#     'Ci'                  : 2.11727e3,              # J/kg/K (ice water specific heat)
#     'Tmelt'               : 273.16,                 # K (melting point of ice)
#     'pstd'                : 1.01325e5,              # Pa (standard pressure)
#     'eSF'                 : 611.,                   # Pa (reference vapor pressure)
#     'pR'                  : 1e5,                    # Pa (reference pressure)
#     'tday'                : 86400.,                 # s (calendar day)
#     }
#
#     constants['Omega'] = 2*np.pi/constants['tsidereal']
#     # 1/s
#
#     constants['Rstar'] = constants['kboltz'] * constants['Navo']
#     # J/K (Universal gas constant)
#
#     constants['Rd']    = constants['Rstar'] / constants['mair']
#     # J/kg/K (dry air gas constant)
#
#     constants['Rv']    = constants['Rstar'] / constants['mvap']
#     # J/kg/K (water vapor gas constant)
#
#     constants['zvir']  = constants['Rv'] / constants['Rd'] - 1.
#     # ratio of gas constants
#
#     constants['rair']  = constants['pstd'] / \
#                          (constants['Rd'] * constants['Tmelt'])
#     # kg/m^3 (density of air at STP)
#
#     return constants

# # -*- coding: utf-8 -*-
# '''
# NAME
#     ncdump
# PURPOSE
#     To demonstrate how to read and write data with NetCDF files using
#     a NetCDF file from the NCEP/NCAR Reanalysis.
#     Plotting using Matplotlib and Basemap is also shown.
# PROGRAMMER(S)
#     Chris Slocum
# REVISION HISTORY
#     20140320 -- Initial version created and posted online
#     20140722 -- Added basic error handling to ncdump
#                 Thanks to K.-Michael Aye for highlighting the issue
# REFERENCES
#     netcdf4-python -- http://code.google.com/p/netcdf4-python/
#     NCEP/NCAR Reanalysis -- Kalnay et al. 1996
#         http://dx.doi.org/10.1175/1520-0477(1996)077<0437:TNYRP>2.0.CO;2
# '''
#
#
# def ncdump(nc_fid, verb=True):
#     '''
#     ncdump outputs dimensions, variables and their attribute information.
#     The information is similar to that of NCAR's ncdump utility.
#     ncdump requires a valid instance of Dataset.
#
#     Parameters
#     ----------
#     nc_fid : netCDF4.Dataset
#         A netCDF4 dateset object
#     verb : Boolean
#         whether or not nc_attrs, nc_dims, and nc_vars are printed
#
#     Returns
#     -------
#     nc_attrs : list
#         A Python list of the NetCDF file global attributes
#     nc_dims : list
#         A Python list of the NetCDF file dimensions
#     nc_vars : list
#         A Python list of the NetCDF file variables
#     '''
#     def print_ncattr(key):
#         """
#         Prints the NetCDF file attributes for a given key
#
#         Parameters
#         ----------
#         key : unicode
#             a valid netCDF4.Dataset.variables key
#         """
#         try:
#             print("\t\ttype:", repr(nc_fid.variables[key].dtype))
#             for ncattr in nc_fid.variables[key].ncattrs():
#                 print('\t\t%s:' % ncattr,\
#                       repr(nc_fid.variables[key].getncattr(ncattr)))
#         except KeyError:
#             print("\t\tWARNING: %s does not contain variable attributes") % key
#
#     # NetCDF global attributes
#     nc_attrs = nc_fid.ncattrs()
#     if verb:
#         print("NetCDF Global Attributes:")
#         for nc_attr in nc_attrs:
#             print('\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr)))
#     nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
#     # Dimension shape information.
#     if verb:
#         print("NetCDF dimension information:")
#         for dim in nc_dims:
#             print("\tName:", dim)
#             print("\t\tsize:", len(nc_fid.dimensions[dim]))
#             print_ncattr(dim)
#     # Variable information.
#     nc_vars = [var for var in nc_fid.variables]  # list of nc variables
#     if verb:
#         print("NetCDF variable information:")
#         for var in nc_vars:
#             if var not in nc_dims:
#                 print('\tName:', var)
#                 print("\t\tdimensions:", nc_fid.variables[var].dimensions)
#                 print("\t\tsize:", nc_fid.variables[var].size)
#                 print_ncattr(var)
#     return nc_attrs, nc_dims, nc_vars

