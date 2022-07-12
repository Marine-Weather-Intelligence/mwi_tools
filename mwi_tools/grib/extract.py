"""
    Extracting functions for grib files:
    - get_values_from_position_grib(INPUT, lat, lon) --> Get dict with all values from position and time in a specific daily grib INPUT
    - get_value_from_grib_dir(path, date, lat, lon) --> Select name of the grib file containing values we want
    - fill_track_df_with_weather_data(df, dir_path, param_list) --> Fill track df with weather values from grib in dir_path
"""

import subprocess
import pandas as pd
import progressbar
from datetime import timedelta


def get_values_from_position_grib(INPUT : str, lat_exp : float, lon_exp : float, time : str) -> dict: 
    """Get a dictionnary with all parameters values from a daily grib_file at the specified location and time

    Args:
        INPUT (str): Path to the grib file
        lat_exp (float): latitude in deg.dec
        lon_exp (float): longitude in deg.dec
        time (str) : time as a string, 23:00 --> '2300'

    Returns:
        dict: dict of values of parameters
    """

    output = subprocess.check_output('grib_ls -l '+str(lat_exp)+','+str(lon_exp)+',1 -p shortName, -w validityTime='+time+' '+INPUT, shell=True)
    
    temp = str(output).split("\\n")
    d = dict()
    for i in range(2,28):
        line = temp[i]
        line = line.split()
        d[line[0]] = line[1]
    
    return d


def get_value_from_grib_dir (path:str, date:str, lat:float, lon:float) -> dict:
    """Select the name of the grib file in the grib dir and get the values of all parameters for this location, time and date
    The grib directory must be ordered this way : 
    grib_dir/
    ├── 20201203/
    │   ├── 20201203_-10_-20_-100_-90.grib
    │   ├── 20201203_-10_-20_-110_-100.grib
    │   ├── 20201203_-10_-20_-120_-110.grib
    │   └── 20201203_-10_-20_-130_-120.grib
    ├── 20201204/
    │   ├── 20201204_-10_-20_-100_-90.grib
    │   ├── 20201204_-10_-20_-110_-100.grib
    │   ├── 20201204_-10_-20_-120_-110.grib
    │   └── 20201204_-10_-20_-130_-120.grib
    └── 20201205/
        ├── 20201205_-10_-20_-100_-90.grib
        ├── 20201205_-10_-20_-110_-100.grib
        ├── 20201205_-10_-20_-120_-110.grib
        └── 20201205_-10_-20_-130_-120.grib

    Args:
        path (str): Path to directory in which the grib files are stored
        date (str): date of type '20201203_0900'
        lat (float): latitude in deg.dec
        lon (float): longitude in deg.dec

    Returns:
        dict: dict of values of parameters
    """
    round_inf_lat = int((lat//10)*10)
    round_sup_lat = round_inf_lat+10
    if round_inf_lat == 0 : 
        round_inf_lat = "0"
    else : 
        round_inf_lat = str(round_inf_lat)
    if round_sup_lat == 0 : 
        round_sup_lat = "0"
    else : 
        round_sup_lat = str(round_sup_lat)
    round_left_lon = int((lon//10)*10)
    round_right_lon = round_left_lon+10
    if round_left_lon == 0 : 
        round_left_lon = "0"
    else : 
        round_left_lon = str(round_left_lon)
    if round_right_lon == 0 : 
        round_right_lon = "0"
    else : 
        round_right_lon = str(round_right_lon)

    temp = date.split('_')
    date = temp[0]
    time = temp[1]
    dir_name = round_sup_lat+'_'+round_inf_lat+'_'+round_left_lon+'_'+round_right_lon
    file = path+'/'+date+'/'+date+'_'+dir_name+'.grib'

    return get_values_from_position_grib(file,lat,lon, time)


def fill_track_df_with_weather_data (df : pd, dir_path : str, param_list : dict) -> pd:
    """Fill the track dataframe with weather data from grib directory (era5)
    This function takes every position in the track dataframe and look for the corresponding weather data in the grib directory

    Args:
        df (pandas): dataframe of track
        dir_path (str): path to directory with all grib files
        param_list (list): list of params that we want in the df

    Returns:
        pandas: complete dataframe
    """
    param_dict_in = {
    'temperature': '2t',
    'wind_u' : '10u',
    'wind_v' : '10v',
    'gusts' : 'i10fg',
    'pressure' : 'msl',
    'air_density' : 'rhoao',
    'sea_temperature' : 'sst',
    'mer_max' : 'hmax',
    'period_mer_max' : 'tmax',
    'peak_wave_period' : 'pp1d',
    'height_total_swell' : 'shts',
    'dir_total_swell' : 'mdts',
    'period_total_swell' : 'mpts',
    'height_wind_waves' : 'shww',
    'dir_wind_waves' : 'mdww',
    'period_wind_waves' : 'mpww',
    'wave_height' : 'swh',
    'mean_wave_direction' : 'mwd',
    'mean_wave_period' : 'mwp',
    'height_swell1' : 'swh1',
    'direction_swell1' : 'mwd1',
    'period_swell1' : 'mwp1',
    'height_swell2' : 'swh2',
    'direction_swell2' : 'mwd2',
    'period_swell2' : 'mwp2',
    'precipitation' : 'tp'
    }

    param_dict_out = {
    'temperature': 't2m',
    'wind_u' : 'u10',
    'wind_v' : 'v10',
    'gusts' : 'i10fg',
    'pressure' : 'msl',
    'air_density' : 'p140209',
    'sea_temperature' : 'sst',
    'mer_max' : 'hmax',
    'period_mer_max' : 'tmax',
    'peak_wave_period' : 'pp1d',
    'height_total_swell' : 'shts',
    'dir_total_swell' : 'mdts',
    'period_total_swell' : 'mpts',
    'height_wind_waves' : 'shww',
    'dir_wind_waves' : 'mdww',
    'period_wind_waves' : 'mpww',
    'wave_height' : 'swh',
    'mean_wave_direction' : 'mwd',
    'mean_wave_period' : 'mwp',
    'height_swell1' : 'p140121',
    'direction_swell1' : 'p140122',
    'period_swell1' : 'p140123',
    'height_swell2' : 'p140124',
    'direction_swell2' : 'p140125',
    'period_swell2' : 'p140126',
    'precipitation' : 'tp'
    }

    bar = progressbar.ProgressBar(maxval=len(df), \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    
    bar.start()
    for i in range(len(df)) : 
        lon = df.loc[i, 'lon']
        lat = df.loc[i, 'lat']
        date = df.loc[i, 'round_datetime']
        dt = date.strftime("%Y%m%d_%H%M")
        dict_values = get_value_from_grib_dir(dir_path, dt,lat,lon)
        for param in param_list :
            if param_list[param] : 
                df.loc[i, param_dict_out[param]] = float(dict_values[param_dict_in[param]])
        bar.update(i+1)
    bar.finish()
    return df