import os

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