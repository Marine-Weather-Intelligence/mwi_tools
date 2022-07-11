import subprocess
import pandas as pd
import progressbar
from datetime import timedelta
from google.cloud import storage
import datetime
from mwi_tools.divers import *
from mwi_tools.coordinates.format import *
from mwi_tools.datetime.calculate import *

storage_options = {"project":'stoked-folder-351109', "token":'/Users/basile/Desktop/SFE/projet_polaire/data/credentials_google_app.json'}


def get_values_from_position_grib(INPUT :str, lat_exp : float, lon_exp : float) -> dict: 
    """Get a dictionnary with all parameters values from a grib_file at the specified location

    Args:
        INPUT (str): Path to the grib file
        lat_exp (float): latitude in deg.dec
        lon_exp (float): longitude in deg.dec

    Returns:
        dict: dict of values of parameters
    """

    output = subprocess.check_output('grib_ls -l '+str(lat_exp)+','+str(lon_exp)+',1 -p shortName '+INPUT, shell=True)
    
    temp = str(output).split("\\n")
    d = dict()
    for i in range(2,28):
        line = temp[i]
        line = line.split()
        d[line[0]] = line[1]
    
    return d


def get_value_from_grib_dir (path:str, date:str, lat:float, lon:float) -> dict:
    """Select the name of the grib file in the grib dir and get the values of all parameters for this location, time and date

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
        round_inf_lat = "00"
    else : 
        round_inf_lat = str(round_inf_lat)
    if round_sup_lat == 0 : 
        round_sup_lat = "00"
    else : 
        round_sup_lat = str(round_sup_lat)
    round_left_lon = int((lon//10)*10)
    round_right_lon = round_left_lon+10
    if round_left_lon == 0 : 
        round_left_lon = "00"
    else : 
        round_left_lon = str(round_left_lon)
    if round_right_lon == 0 : 
        round_right_lon = "00"
    else : 
        round_right_lon = str(round_right_lon)

    dir_name = round_sup_lat+'_'+round_inf_lat+'_'+round_left_lon+'_'+round_right_lon
    file = path+'/'+dir_name+'/grib/'+date+'_'+dir_name+'.grib'

    return get_values_from_position_grib(file,lat,lon)

def fill_track_df_with_weather_data_old(df : pd, dir_path : str, param_list : list[str]) -> pd:
    """Fill the track dataframe with weather data from grib directory (era5)

    Args:
        df (pd): dataframe of track
        dir_path (str): path to directory with all grib files
        param_list (list): list of params that we want in the df

    Returns:
        pd: complete dataframe
    """
    param_dict = {
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

    atmo_list = ['temperature','wind_u','wind_v','pressure','sea_temperature']

    bar = progressbar.ProgressBar(maxval=len(df), \
        widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    
    bar.start()
    for i in range(len(df)) : 
        lat25 = df.loc[i, 'round_lat25']
        lon25 = df.loc[i, 'round_lon25']
        lat50 = df.loc[i, 'round_lat50']
        lon50 = df.loc[i, 'round_lon50']
        date = df.loc[i, 'round_datetime']
        dt = date.strftime("%Y%m%d_%H%M")
        for param in param_list : 
            if param == "precipitation" or param=="gusts" : 
                #Changer la date en arrondissant à 6h ou 18h
                if date.hour >= 18 : 
                    stepRange = date.hour - 18 +1
                    date6 = date.replace(hour=18)
                elif date.hour < 6: 
                    stepRange = date.hour + 6 +1
                    date6 = date.replace(hour=0) - timedelta(hours = 6)
                else : 
                    stepRange = date.hour -6 +1
                    date6 = date.replace(hour=6)

                dt6 = date6.strftime("%Y%m%d_%H%M") 
                df.loc[i, param] = get_value_from_grib_dir(dir_path, dt6,param_dict[param],lat25,lon25, stepRange)
            elif param in atmo_list :
                df.loc[i, param] = get_value_from_grib_dir(dir_path, dt,param_dict[param],lat25,lon25)
            else : 
                df.loc[i, param] = get_value_from_grib_dir(dir_path, dt,param_dict[param],lat50,lon50)
        bar.update(i+1)
    bar.finish()
    return df

def fill_track_df_with_weather_data (df : pd, dir_path : str, param_list : dict) -> pd:
    """Fill the track dataframe with weather data from grib directory (era5)

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

def get_df_from_posreport_list(pos_report_list:list[str], id :int, bucket: storage.Client.bucket) :
    """Create a dataframe of track for the boat with id from a list of posreport files 

    Args:
        pos_report_list (list[str]): list of path to posreport files
        id (int): id of the boat on pos report files
        bucket (storage.Client.Bucket): bucket for accessing posreport on cloud storage
    """

    lat = []
    lon = []
    time = []

    for path in pos_report_list : 
        file = bucket.blob(path).download_as_string().decode('utf-8')
        file = file.split('\r\n')
        for line in file : 
            line = line.split(";")
            if len(line) != 6 : 
                continue;
            elif int(line[1]) == id : 
                lat.append(line[2])
                lon.append(line[3])
                time.append(line[4])

    d = {'time':time, 'lat':lat, 'lon':lon}
    return pd.DataFrame(data=d)

def create_all_track_dataframes(id_dict: dict(), bucket: storage.Client.bucket, pos_report_list:list[str]) :
    """Create dataframe of track from posreport files for all id's in id_dict.

    Args:
        id_dict (dict()): dict of id's from name key
        bucket (storage.Client.Bucket): bucket where the posreports are stored
        pos_report_list (list[str]): list of path of posreport files
    """

    for name in id_dict : 
        id = id_dict[name]
        create_track_dataframe(id, name, bucket, pos_report_list)

def create_track_dataframe(id :int , name:str, bucket:storage.Client.bucket, pos_report_list:list[str]) :  
    """Create dataframe of track from posreport files.

    Args:
        id (int): id of the boat in posreport files
        name (str): Name of the boat for naming created file
        bucket (storage.Client.Bucket): bucket where the posreports are stored
        pos_report_list (list[str]): list of path of posreport files
    """
    df = get_df_from_posreport_list(pos_report_list, id, bucket)
    df['lon'] = df['lon'].apply(lambda x: convert_coord_to_degdec2(x))
    df['lat'] = df['lat'].apply(lambda x: convert_coord_to_degdec2(x))
    df['datetime'] = df['time'].apply(lambda x: datetime.datetime.strptime(x, "%m/%d/%y %H:%M"))
    df.drop('time', axis=1, inplace=True)
    
    #Add rounded values, usefull for searching weather data when using netcdf technique for example
    df['round_lon25'] = df['lon'].apply(x_round_25)
    df['round_lat25'] = df['lat'].apply(x_round_25)
    df['round_lon50'] = df['lon'].apply(x_round_50)
    df['round_lat50'] = df['lat'].apply(x_round_50)
    df['round_datetime'] = df['datetime'].apply(round_datetime)

    ## TO LOCAL DIRECTORY
    file_path = "/Users/basile/Desktop/SFE/projet_polaire/data/dataframe/"+name+"_VG20_simple_track.pkl" 
    df.to_pickle(file_path) 

    ## TO CLOUD STORAGE
    filepath = "gs://hokulea_data/tracks/"+name+"_VG20_simple_track.pkl"
    df.to_pickle(filepath, storage_options=storage_options) 