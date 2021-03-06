import requests
from datetime import datetime
import cdsapi


def get_grib_api_squid(lat_sup:float, lat_inf : float, lon_left : float, lon_right : float, model : str, variables:str, step_from:int, step_to:int, step_dt:int, out_path:str, credentials : list) -> None :
    """Download grib from API GRIB SQUID

    Args:
        lat_sup (float): latitude top (- for south)
        lat_inf (float): latitude bottom (- for south)
        lon_left (float): longitude left (- for west)
        lon_right (float): longitude right (- for west)
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
    with open(out_path+'/'+model+'_'+date_time+'_'+lat_sup+'_'+lat_inf+'_'+lon_left+'_'+lon_right+'.grib', 'wb') as out_file : 
        out_file.write(r.content)

    print(status)
    return None



def get_era5 (lat_sup:float,lat_inf:float,lon_left:float,lon_right:float,year:str,month:str,day:str,format:str, outpath:str) -> None :
    """Download era5 file from cds api 

    Args:
        lat_sup (float): latitude top (- for south)
        lat_inf (float): latitude bottom (- for south)
        lon_left (float): longitude left (- for west)
        lon_right (float): longitude right (- for west)
        year (str): year with format '2022'
        month (str): month with format '07' (don't forget the first 0 if there is one)
        day (str): day with format '17' (don't forget the first 0 if there is one)
        format (str): 'netddf' or 'grib'
        outpath (str): path of the directory where to store the file, don't put '/' at the end
    """    

    c = cdsapi.Client() 

    #Cree l'item a mettre dans l'api de requete
    item = {
            'product_type': 'reanalysis',
            'format': format,
            'variable': [
                '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_temperature',
                'instantaneous_10m_wind_gust','mean_sea_level_pressure','sea_surface_temperature','total_precipitation','air_density_over_the_oceans', 'maximum_individual_wave_height',
                'mean_direction_of_total_swell', 'mean_direction_of_wind_waves', 'mean_period_of_total_swell',
                'mean_period_of_wind_waves', 'mean_wave_direction',
                'mean_wave_direction_of_first_swell_partition', 'mean_wave_direction_of_second_swell_partition', 'mean_wave_period',
                'mean_wave_period_of_first_swell_partition', 'mean_wave_period_of_second_swell_partition', 'peak_wave_period',
                'period_corresponding_to_maximum_individual_wave_height', 'significant_height_of_combined_wind_waves_and_swell',
                'significant_height_of_total_swell', 'significant_height_of_wind_waves', 'significant_wave_height_of_first_swell_partition',
                'significant_wave_height_of_second_swell_partition',
            ],
            'year': year,
            'month': month,
            'day': day,
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            'area': [
                str(lat_sup), str(lon_left), str(lat_inf),
                str(lon_right),
            ],
        }

    
    full_date = year+month+day
    name = 'era5_'+full_date+'_'+str(int(lat_sup))+'_'+str(int(lat_inf))+'_'+str(int(lon_left))+'_'+str(int(lon_right))
    if format == 'netcdf' : 
        namefile = name+'.nc'
    else : 
        namefile = name+'.grib'
    
    c.retrieve('reanalysis-era5-single-levels',item, outpath+'/'+namefile)
