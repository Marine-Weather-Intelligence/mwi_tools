import requests
from datetime import datetime

def get_grib_api_squid(lat_sup:float, lat_inf : float, lon_left : float, lon_right : float, model : str, variables:str, step_from:int, step_to:int, step_dt:int, out_path:str, credentials : list) -> None :
    """Download grib from API GRIB SQUID

    Args:
        lat_sup (float): latitude top
        lat_inf (float): latitude bottom
        lon_left (float): longitude left
        lon_right (float): longitude right
        model (str): model to choose between --> ['gfs1','gfs05','gfs025','arome0025','arome001','arpege05','arpege01','iconEU','iconGlobal','ecmwf', 'ww3','mfwam01','mfwam0025']
        variables (str): variables separated by a coma in a string ex : "10u,10v,prmsl,2t,gust,apcp" or "swper,mpww,swdir,dirpw,perpw,swell,shww,swh,wvdir"
        step_from (int): Either a validityTime to start with or 'now' to get the first available timestep
        step_to (int): last timestep, must be a multiple of step_dt, ex : 384 for 16 days
        step_dt (int): 1,3,... timestep between forecast
        out_path (str): path of the directory where the grib file will be downloaded ie '/data'
        credentials (list): [email, password, id, pwd] Credentials to access the squid API

    Returns:
        None: None
    """    

    modeldict = {
        'gfs1' : 'gfs_1_0',
        'gfs05' : 'gfs_0_5',
        'gfs025' : 'gfs_0_25',
        'arome0025' : 'arome_0_025',
        'arome001' : 'arome_0_01',
        'arpege05' : 'arpege_0_5',
        'arpege01' : 'arpege_0_1',
        'iconEU' : 'icon_eu',
        'iconGlobal' : 'icon_global',
        'ecmwf' : 'ecmwf_0_4', 
        'ww3' : 'ww3_glo',
        'mfwam01' : 'mfwam_arpege_0_1',
        'mfwam0025' : 'mfwam_arome_0_025'
    }
   

    model_req = modeldict[model]
    
    if(lat_sup == 0) :
        lat_sup = '00'
    else : 
        lat_sup = str(int(lat_sup))
    if(lat_inf == 0) :
        lat_inf = '00'
    else : 
        lat_inf = str(int(lat_inf))
    if(lon_left == 0) :
        lon_left = '00'
    elif lon_left == -180 : 
        lon_left = '180'
    else : 
        lon_left = str(int(lon_left))
    if(lon_right == 0) :
        lon_right = '00'
    elif lon_right == -180 : 
        lon_right = '180'
    else : 
        lon_right = str(int(lon_right))
    
    area = lat_sup+' '+lon_left+' '+lat_inf+' '+lon_right

    xml = '<grib_request version="1" model="'+model_req+'" step_from="'+str(step_from)+'" step_to="'+str(step_to)+'" step_dt="'+str(step_dt)+'" var="'+variables+'" ll="'+area+'" compress="no" grib_version="2" />'

    URL = "https://grib-server.greatcircle.be/v4/grib-requests"

    PARAMS = {'email':credentials[0], 'password':credentials[1], 'xml':xml}

    id = credentials[2]
    pwd = credentials[3]

    r = requests.post(url = URL, data = PARAMS, auth=(id, pwd)) 

    status = r.status_code

    now = datetime.now()
    date_time = now.strftime("%Y%m%d")
    with open(out_path+'/'+model+'_'+date_time+'_'+lat_sup+'_'+lon_left+'_'+lat_inf+'_'+lon_right+'.grib', 'wb') as out_file : 
        out_file.write(r.content)

    print(status)
    return None
