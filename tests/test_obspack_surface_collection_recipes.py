import os
import re
import pytest

import numpy as np
import xarray as xr

from gdess import load_stations_dict
from gdess.data_source.observations.load import load_data_with_regex
from gdess.data_source.observations.subset import binTimeLat, binLonLat, by_datetime
from gdess.data_source.observations.gvplus_surface import Collection
from gdess.data_source.observations.gvplus_name_utils import \
    get_dict_of_all_station_filenames, get_dict_of_station_codes_and_names


@pytest.fixture
def newEmptySurfaceStation():
    mySurfaceInstance = Collection()
    return mySurfaceInstance

@pytest.fixture
def globalview_datasetdict(globalview_test_data_path):
    p = re.compile(r'co2_([a-zA-Z0-9]*)_surface.*\.nc$')
    return load_data_with_regex(globalview_test_data_path, compiled_regex_pattern=p)

def test_station_MLO_is_present(newEmptySurfaceStation):
    station_dict = load_stations_dict()
    assert 'mlo' in station_dict

def test_station_MLO_in_all_station_filenames(globalview_test_data_path):
    a = get_dict_of_all_station_filenames(str(globalview_test_data_path) + os.sep)
    assert 'mlo' in a.keys()

def test_station_MLO_in_all_station_datasets(globalview_test_data_path):
    a = get_dict_of_station_codes_and_names(str(globalview_test_data_path) + os.sep)
    assert 'mlo' in a.keys()

def test_station_MLO_in_loaded_datasets(globalview_datasetdict):
    assert 'mlo' in globalview_datasetdict.keys()

def test_return_type_from_timelatbinned_dataset(globalview_datasetdict):
    binned = binTimeLat(globalview_datasetdict['mlo'])
    assert isinstance(binned, tuple)

def test_return_type_from_lonlatbinned_dataset(globalview_datasetdict):
    binned = binLonLat(globalview_datasetdict['mlo'])
    assert isinstance(binned, tuple)

def test_return_type_from_datetime_binning(globalview_datasetdict):
    binned = by_datetime(globalview_datasetdict['mlo'],
                         start=np.datetime64("2000-01-01"),
                         end=np.datetime64("2000-03-01"))
    assert isinstance(binned, xr.Dataset)

def test_simplest_preprocessed_type(globalview_test_data_path, newEmptySurfaceStation):
    newEmptySurfaceStation.preprocess(datadir=globalview_test_data_path, station_name='mlo')
    assert isinstance(newEmptySurfaceStation.stepA_original_datasets['mlo'], xr.Dataset)


def test_recipe_input_year_error(globalview_test_data_path, newEmptySurfaceStation):
    recipe_options = {
        'ref_data': globalview_test_data_path,
        'start_yr': "198012",
        'end_yr': "201042",
        'station_code': 'mlo'}
    with pytest.raises(SystemExit):
        newEmptySurfaceStation.run_recipe_for_timeseries(verbose='DEBUG', options=recipe_options)


def test_recipe_input_stationcode_error(globalview_test_data_path, newEmptySurfaceStation):
    recipe_options = {
        'ref_data': globalview_test_data_path,
        'start_yr': "1980",
        'end_yr': "2010",
        'station_code': 'asdkjhfasg'}
    with pytest.raises(SystemExit):
        newEmptySurfaceStation.run_recipe_for_timeseries(verbose='DEBUG', options=recipe_options)


def test_timeseries_recipe_completes_with_no_errors(globalview_test_data_path, newEmptySurfaceStation):
    recipe_options = {
        'ref_data': globalview_test_data_path,
        'start_yr': "1980",
        'end_yr': "2010",
        'station_code': 'mlo'}
    try:
        newEmptySurfaceStation.run_recipe_for_timeseries(verbose='DEBUG', options=recipe_options)
    except Exception as exc:
        assert False, f"'run_recipe_for_timeseries' raised an exception {exc}"
