"""
    Splitting functions for grib files : 
    - split_grib_per_hour(grib_path, dir_name) --> Function spliting a grib file into one per hour
    - split_grib_directory_per_hour(path) --> Split per hour every grib from a directory containing subfolders of grib sorted geographically,
"""

import os
import metview as mv

def split_grib_per_hour(grib_path : str, dir_name:str): 
    """Function spliting a grib file into many small ones
    One grib file per hour

    Args:
        grib_path (str): "path to the grib file"
        dir_name (str): "Name of the directory where the grib files are located"

    """
    temp = grib_path.split('/')
    path = ''
    for i in range(len(temp)-1) : 
        path += temp[i]+'/'

    f = open(path+'rule.filter', 'w')
    f.write('write "'+path+'[validityDate]_[validityTime]_'+dir_name+'.grib";')
    f.close()

    os.system('grib_filter '+path+'rule.filter '+grib_path) 

def split_grib_directory_per_hour(path : str) -> None :
    """From a directory containing subfolders of grib sorted geographically, 
    split every grib into many grib such as there is one grib per timestamp

    Args:
        path (str): path to the main directory
    """
    list_dir = os.listdir(path)
    for dir in list_dir : 
        dir_path = path+'/'+dir+'/grib'
        list_files = os.listdir(dir_path)
        for file in list_files : 
            if file[0] != '.' and file != "rule.filter": 
                print(file)
                split_grib_per_hour(dir_path+'/'+file, dir)
        list_new_files = os.listdir(dir_path)
        for file in list_new_files : 
            if file[0] != '.' and file != "rule.filter" and file not in list_files:  
                temp = file.split('_')
                time = temp[1]
                if len(time) == 3 : 
                    temp[1] = '0'+time
                elif time == '0' : 
                    temp[1] = '0000'
                else : 
                    continue
                new_filename =""
                for i in range(len(temp)) : 
                    if i == 0 : 
                        new_filename += temp[i]
                    else : 
                        new_filename+='_'+temp[i]
                os.rename(dir_path+'/'+file, dir_path+'/'+new_filename)


def split_grib_by_area (inpath :str, lat_sup :float, lat_inf :float, lon_left :float, lon_right :float, lat_step:int, lon_step :int, outpath:str) -> None :
    """Split a grib file into many small grib files of size lat_step*lon_step

    Args:
        inpath (str): path of the first grib file, file is supposed to be named like this : model_date_latsup_latinf_lonleft_lonright.grib
        lat_sup (float): highest latitude of the split
        lat_inf (float): lowest latitude of the split
        lon_left (float): leftest latitude of the split
        lon_right (float): rightest latitude of the split
        lat_step (int): size of the split in latitude
        lon_step (int): size of the split in longitude
        outpath (str): path of the directory in which small grib files are saved, it create a folder per zone
    """

    filename = inpath.split('/')[-1]
    temp = filename.split('_')
    model = temp[0]
    date = temp[1]
    for lat1 in range(lat_sup, lat_inf, -lat_step) : 
        lat2 = lat1 - lat_step
        for lon1 in range(lon_left, lon_right, lon_step) : 
            lon2 = lon1 + lon_step
            if(int(lat1) == 0) :
                lat1 = '00'
            else : 
                lat1 = str(int(lat1))
            if(int(lat2) == 0) :
                lat2 = '00'
            else : 
                lat2 = str(int(lat2))
            if(int(lon1) == 0) :
                lon1 = '00'
            elif lon1 == -180 : 
                lon1 = '180'
            else : 
                lon1 = str(int(lon1))
            if(int(lon2) == 0) :
                lon2 = '00'
            elif lon2 == -180 : 
                lon2 = '180'
            else : 
                lon2 = str(int(lon2))
            area = [lat2, lon1, lat1, lon2]
            regrided = mv.read(source = inpath, area=[lat2, lon1, lat1, lon2])
            zone_name = area[2]+'_'+area[0]+'_'+area[1]+'_'+area[3]
            if not os.path.exists(outpath+'/'+zone_name) : 
                os.mkdir(outpath+'/'+zone_name)
            if not os.path.exists(outpath+'/'+zone_name+'/grib') : 
                os.mkdir(outpath+'/'+zone_name+'/grib')
            mv.write(outpath+'/'+zone_name+'/grib/'+model+'_'+date+'_'+zone_name+'.grib', regrided)