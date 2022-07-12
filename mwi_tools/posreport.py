"""
    Usefull functions for posreport files:
    - get_df_from_posreport_list(pos_report_list, id, bucket) --> Create a raw dataframe of track for the boat with id from a list of posreport files 
    - create_all_track_dataframes(id_dict, bucket, pos_report_list) --> Create dataframe of track from posreport files for all id's in id_dict
    - create_track_dataframe(id, name, bucket, pos_report_list) --> Create complete dataframe of track from posreport files.
"""
from google.cloud import storage
import datetime
import pandas as pd
from mwi_tools.divers import *
from mwi_tools.coordinates.format import *
from mwi_tools.datetime.calculate import *

def get_raw_df_from_posreport_list_cloud(pos_report_list:list[str], id :int, bucket: storage.Client.bucket) :
    """Create a raw dataframe of track for the boat with id from a list of posreport files stored in a cloud bucket  

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

def create_all_track_dataframes_from_cloud(id_dict: dict, bucket: storage.Client.bucket, pos_report_list:list[str], storage_options, race_name, cloud_save_path = None, local_save_path=None) :
    """Create dataframe of track from posreport files stored in cloud sotrage for all id's in id_dict.

    Args:
        id_dict (dict): dict of id's from name key
        bucket (storage.Client.Bucket): bucket where the posreports are stored
        pos_report_list (list[str]): list of path of posreport files
    """

    for name in id_dict : 
        id = id_dict[name]
        if cloud_save_path != None :
            cloud_filepath = cloud_save_path+name+"_"+race_name+"_simple_track.pkl"
        if local_save_path != None :
            local_path = local_save_path+name+"_"+race_name+"_simple_track.pkl"
        create_track_dataframe_from_cloud(id, name, bucket, pos_report_list, save_cloud_filepath=cloud_filepath, storage_options=storage_options, save_local_filepath=local_path)

def create_track_dataframe_from_cloud(id :int , name:str, bucket:storage.Client.bucket, pos_report_list:list[str], save_cloud_filepath = None ,storage_options = None, save_local_filepath=None) :  
    """Create complete dataframe of track from posreport files stored in cloud storage.

    Args:
        id (int): id of the boat in posreport files
        name (str): Name of the boat for naming created file
        bucket (storage.Client.Bucket): bucket where the posreports are stored
        pos_report_list (list[str]): list of path of posreport files
    """
    df = get_raw_df_from_posreport_list_cloud(pos_report_list, id, bucket)
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
    if save_local_filepath != None : 
        df.to_pickle(save_local_filepath) 

    ## TO CLOUD STORAGE
    if save_cloud_filepath != None :
        df.to_pickle(save_cloud_filepath, storage_options=storage_options) 
    
    return df