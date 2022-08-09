"""Diverse functions usefull for development purposes
"""
from math import *
import pandas as pd
import datetime

def x_round_25(x:float) -> float:
    """Round to the nearest 0.25 value

    Args:
        x (float): 

    Returns:
        float: rounded value
    """

    return round(x*4)/4

def x_round_50(x:float) -> float:
    """Round to the nearest 0.5 value

    Args:
        x (float): 

    Returns:
        float: rounded value
    """

    return round(x*2)/2

def round_10_sup(x:float) -> int: 
    return ceil(x/10)*10

def round_10_inf(x:float) -> int: 
    return floor(x/10)*10

def coord_gde_zone(df:pd.DataFrame, gd_zone:str)->list:
    """return the limits (latitude and longitude) of a big zone

    Args:
        df (pd.DataFrame): dataframe with information related to all geographic zone
        gd_zone (str): name of the big zone(atlantique_nord,mediterranee, nord, atlantique_sud, indien, pacifique_nord or pacifique_sud)

    Returns:
        list: list of float
    """
    lat_sup=df[df['gd_zone']==gd_zone]['lat sup'].max()
    lat_inf=df[df['gd_zone']==gd_zone]['lat inf'].min()
    lon_right=df[df['gd_zone']==gd_zone]['lon right'].max()
    lon_left=df[df['gd_zone']==gd_zone]['lon left'].min()
    return[lat_sup, lat_inf, lon_left, lon_right]

def available_modeles(df:pd.DataFrame, gd_zone:str)->list:
    """return the list of available model for a big zone

    Args:
        df (pd.DataFrame): dataframe with information related to all geographic zone
        gd_zone (str): name of the big zone(atlantique_nord,mediterranee, nord, atlantique_sud, indien, pacifique_nord or pacifique_sud)

    Returns:
        list: list of name of model (str)
    """
    liste=df[df['gd_zone']==gd_zone]['modeles'].unique()# on prend les modeles present dans chaque sous zones
    mod=[e.split(',') for e in liste]
    [mod[i+1].extend(mod[i]) for i in range(len(mod)-1)]
    tot=mod[-1]
    list_model=list(set(tot))
    return list_model

def print_log(line:str):
    """surcharge print to display the date and time of the print

    Args:
        line (str): string to print
    """
    d = datetime.datetime.now().strftime('[%y/%m/%d %H:%M] ') # actual time
    print(d+line)

