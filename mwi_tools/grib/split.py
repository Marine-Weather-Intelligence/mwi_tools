"""
    Splitting functions for grib files : 
    - split_grib_per_hour(grib_path, output_path) --> Function spliting a grib file into one per hour
    - split_grib_per_day(grib_path, output_path) --> Function spliting a grib file into one per day
    - split_grib_by_area (grib_path, lat_step, lon_step, output_path) --> Split a grib file into many small grib files of size lat_step*lon_step
"""

import os
import metview as mv

def split_grib_per_hour(grib_path:str, output_path:str) : 
    """Split a grib in grib/hour

    Args:
        grib_path (str): path to the input grib file
        output_path (str): path to the directory that will contain the splitted grib files (without / at the end)
    """
    filename = grib_path.split('/')[-1]
    temp = filename.split('_')
    model = temp[0]
    date = temp[1]
    lat_sup = temp[2]
    lat_inf = temp[3]
    lon_left = temp[4]
    lon_right = temp[5].split('.')[0]

    f = open(output_path+'/rule.filter', 'w')
    f.write('write "'+output_path+'/'+model+'_[validityDate]_[validityTime]_'+lat_sup+'_'+lat_inf+'_'+lon_left+'_'+lon_right+'.grib";')
    f.close()

    os.system('grib_filter '+output_path+'/rule.filter '+grib_path) 
    os.remove(output_path+'/rule.filter')

def split_grib_per_day(grib_path:str, output_path:str) : 
    """Split a grib in grib/day

    Args:
        grib_path (str): path to the input grib file
        output_path (str): path to the directory that will contain the splitted grib files (without / at the end)
    """

    filename = grib_path.split('/')[-1]
    temp = filename.split('_')
    model = temp[0]
    date = temp[1]
    lat_sup = temp[2]
    lat_inf = temp[3]
    lon_left = temp[4]
    lon_right = temp[5].split('.')[0]

    f = open(output_path+'/rule.filter', 'w')
    f.write('write "'+output_path+'/'+model+'_[validityDate]_'+lat_sup+'_'+lat_inf+'_'+lon_left+'_'+lon_right+'.grib";')
    f.close()

    os.system('grib_filter '+output_path+'/rule.filter '+grib_path) 
    os.remove(output_path+'/rule.filter')

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



def split_grib_by_area (grib_path :str, lat_step:int, lon_step :int, output_path:str) -> None :
    """Split a grib file into many small grib files of size lat_step*lon_step

    Args:
        inpath (str): path of the first grib file, file is supposed to be named like this : model_date_latsup_latinf_lonleft_lonright.grib
        lat_step (int): size of the split in latitude
        lon_step (int): size of the split in longitude
        output_path (str): path to the directory that will contain the splitted grib files (without / at the end), it create a folder per zone
    """

    filename = grib_path.split('/')[-1]
    temp = filename.split('_')
    if len(temp) == 6 : 
        model = temp[0]
        date = temp[1]
        lat_sup = temp[2]
        lat_inf = temp[3]
        lon_left = temp[4]
        lon_right = temp[5].split('.')[0]
        time = None
    else : 
        model = temp[0]
        date = temp[1]
        time = temp[2]
        lat_sup = temp[3]
        lat_inf = temp[4]
        lon_left = temp[5]
        lon_right = temp[6].split('.')[0]

    for lat1 in range(int(lat_sup), int(lat_inf), -lat_step) : 
        lat2 = lat1 - lat_step
        for lon1 in range(int(lon_left), int(lon_right), lon_step) : 
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
            # elif lon1 == -180 : 
            #     lon1 = '180'
            else : 
                lon1 = str(int(lon1))
            if(int(lon2) == 0) :
                lon2 = '00'
            # elif lon2 == -180 : 
            #     lon2 = '180'
            else : 
                lon2 = str(int(lon2))
            area = [lat2, lon1, lat1, lon2]

            regrided = mv.read(source = grib_path, area=[lat2, lon1, lat1, lon2])
            zone_name = area[2]+'_'+area[0]+'_'+area[1]+'_'+area[3]

            if not os.path.exists(output_path+'/'+zone_name) : 
                os.mkdir(output_path+'/'+zone_name)
            if not os.path.exists(output_path+'/'+zone_name+'/grib') : 
                os.mkdir(output_path+'/'+zone_name+'/grib')
            if time != None : 
                mv.write(output_path+'/'+zone_name+'/grib/'+model+'_'+date+'_'+time+'_'+zone_name+'.grib', regrided)
            else : 
                mv.write(output_path+'/'+zone_name+'/grib/'+model+'_'+date+'_'+zone_name+'.grib', regrided)