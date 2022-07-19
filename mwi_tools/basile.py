import pandas as pd
import mwi_tools.coordinates.calculate as mwicc
import mwi_tools.wind as mwiw

def calculate_features_df_weather(df) : 
    """Calculate and add some features to a weather/track dataframe like heading, gust difference, angles
    This function is made for the Vendee Globe 2020 files

    Args:
        df_weather (pd.dataframe): Dataframe containing the track and all the weather data corresponding to each position
    """

    #Eliminate two first days of VG 
    df = df[df['datetime'] >= '2020-11-09'].reset_index()
    df.drop('index', axis=1, inplace=True)

    #Deal with naan
    df = df.replace(9999, pd.NA)
    df = df.replace('NaN', pd.NA)
    df = df.fillna(method='ffill')

    #Delete duplicate
    df.drop_duplicates(subset ="datetime", keep = 'first', inplace=True)

    #Add heading and boat speed
    df = df.sort_values(by=['datetime'])
    df = df.reset_index()
    df.drop('index', axis=1, inplace=True)
    for i in range(0, len(df)-1) : 
        dt = (df.loc[i+1, 'datetime'] - df.loc[i, 'datetime']).total_seconds()
        pos1 = (df.loc[i, 'lat'], df.loc[i, 'lon'])
        pos2 = (df.loc[i+1, 'lat'], df.loc[i+1, 'lon'])
        df.loc[i, 'speed'] = mwicc.get_speed(pos1, pos2, dt)
        cap = mwicc.get_heading(pos1, pos2)
        if cap == None : 
            if i == 0 : 
                df.loc[i, 'cap'] = 0
            else : 
                df.loc[i, 'cap'] = df.loc[i-1,'cap']
        else : 
            df.loc[i, 'cap'] = cap

    #Don't forget to delete last line which has no speed
    df = df.iloc[:-1 , :]


    #Calculate TWS and TWD
    df['TWD'] = df.apply(lambda x : mwiw.get_dir(x.u10, x.v10), axis=1)
    df['TWS'] = df.apply(lambda x :mwiw.get_TWS(x.u10, x.v10), axis=1)

    #Convert m/S gust in knots
    df['i10fg'] = df['i10fg'].apply(lambda x: round(x*1.94384,1))
    
    #Add gust diff

    def set_diff_gust(x) : 
        diff = x['i10fg']-x['TWS']
        if (diff < 0) : 
            diff = 0
        return diff/x['TWS']

    df['gust_diff'] = df.apply(lambda x: set_diff_gust(x), axis=1)


    #Add TWA
    df['TWA'] = df.apply(lambda x : mwiw.set_TWA(x.TWD, x.cap), axis=1)
    df.drop('TWD', axis=1, inplace=True)
    df.drop('u10', axis=1, inplace=True)
    df.drop('v10', axis=1, inplace=True)

    #Change waves direction to wave angle
    #Total swell
    df['mats'] = df.apply(lambda x : round(mwiw.set_TWA(x.mdts, x.cap)), axis=1)
    df.drop('mdts', axis=1, inplace=True)

    #Wind waves
    df['maww'] = df.apply(lambda x : round(mwiw.set_TWA(x.mdww, x.cap)), axis=1)
    df.drop('mdww', axis=1, inplace=True)

    #Mean wave
    df['mwa'] = df.apply(lambda x : round(mwiw.set_TWA(x.mwd, x.cap)), axis=1)
    df.drop('mwd', axis=1, inplace=True)

    #Swell 1
    df['mah1'] = df.apply(lambda x : round(mwiw.set_TWA(x.p140122, x.cap)), axis=1)
    df.drop('p140122', axis=1, inplace=True)

    #Swell 2
    df['mah2'] = df.apply(lambda x : round(mwiw.set_TWA(x.p140125, x.cap)), axis=1)
    df.drop('p140125', axis=1, inplace=True)

    df.drop('cap', axis=1, inplace=True)

    #Correct column names
    df['air_density'] = df['p140209']
    df.drop('p140209', axis=1, inplace=True)

    df['ph1'] = round(df['p140123'],1)
    df.drop('p140123', axis=1, inplace=True)

    df['ph2'] = round(df['p140126'],1)
    df.drop('p140126', axis=1, inplace=True)

    df['hh1'] = round(df['p140121'],1)
    df.drop('p140121', axis=1, inplace=True)

    df['hh2'] = round(df['p140124'],1)
    df.drop('p140124', axis=1, inplace=True)

    df['peak_wave_period'] = round(df['pp1d'],1)
    df.drop('pp1d', axis=1, inplace=True)

    df['hmax'] = round(df['hmax'],1)
    df['mpts'] = round(df['mpts'],1)
    df['mpww'] = round(df['mpww'],1)
    df['mwp'] = round(df['mwp'],1)
    df['pmax'] = round(df['tmax'],1)
    df.drop('tmax', axis=1, inplace=True)
    df['shts'] = round(df['shts'],1)
    df['swh'] = round(df['swh'],1)
    df['shww'] = round(df['shww'],1)


    return df