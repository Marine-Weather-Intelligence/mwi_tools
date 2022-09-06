#On doit imposer des règles de normalisation qui correspondent aux paramètres 
#(anticiper le fait que l'on puisse rajouter des valeurs supérieures à celles que l'on a aujourd'hui.
def remove_quantiles (df_input, config={}) :
    df = df_input.copy()
    for column in df.columns:
        if bool(config) : 
            q_low = config['q_low']
            q_hi  = config['q_hi']
            df = df[(df[column] < q_hi) & (df[column] > q_low)] 
            return df, None
        else : 
            q_low = df[column].quantile(0.01)
            q_hi  = df[column].quantile(0.99)
            config = {
                'q_low' : q_low,
                'q_hi' : q_hi
            }
            df = df[(df[column] < q_hi) & (df[column] > q_low)]
            return df, config

def normalisation_minmax_manuel(mini, maxi, value) : 
    delta = maxi-mini
    return (value-mini)/delta
    
def normalisation_standard_manuel(mean, std, value) : 
    return (value-mean)/std

def normalisation_minmax(column_input, config, param_name) : 
    column = column_input.copy()
    if bool(config) : 
        maxi = config[param_name]['maxi']
        mini  = config[param_name]['mini']
        column = column.apply(lambda x: normalisation_minmax_manuel(mini,maxi,x))
        return column, None
    else : 
        maxi = column.max()
        mini = column.min()
        config = {
            'maxi' : maxi,
            'mini' : mini
        }
        column = column.apply(lambda x: normalisation_minmax_manuel(mini,maxi,x))
        return column, config

def normalisation_standard(column_input, config, param_name) : 
    column = column_input.copy()
    if bool(config) : 
        mean = config[param_name]['mean']
        std  = config[param_name]['std']
        column = column.apply(lambda x: normalisation_standard_manuel(mean,std,x))
        return column, None
    else : 
        mean = column.mean()
        std = column.std()
    
        config = {
            'mean' : mean,
            'std' : std
        }
        column = column.apply(lambda x: normalisation_standard_manuel(mean,std,x))
        return column, config


def normalisation_angle(value, symetrique=True) : 
    #Symétrique
    if symetrique == True : 
        return abs(value)/180

    #Asymétrique
    else : 
        return (value+180)/360


def normalize_df(df2, type, remove_outliers=False, normalize_speed=False, historique=True, symetrique=True, config={}) : 
    config_norm = dict()
    df=df2.copy()
    if remove_outliers : 
        df, config_quantiles = remove_quantiles(df, config)
        if not bool(config): 
            config_norm.update(config_quantiles)

    if type == 'minmax' :
        df.loc[:,'TWS'], config_TWS = normalisation_minmax(df['TWS'], config, 'TWS')
        df.loc[:,'i10fg'], config_i10fg = normalisation_minmax(df['i10fg'], config, 'i10fg')
        df.loc[:,'gust_diff'], config_gust_diff = normalisation_minmax(df['gust_diff'], config, 'gust_diff')
        df.loc[:,'hh1'], config_hh1 = normalisation_minmax(df['hh1'], config, 'hh1')
        df.loc[:,'hh2'], config_hh2 = normalisation_minmax(df['hh2'], config, 'hh2')
        df.loc[:,'shww'], config_shww = normalisation_minmax(df['shww'], config, 'shww')
        df.loc[:,'shts'], config_shts = normalisation_minmax(df['shts'], config, 'shts')
        df.loc[:,'swh'], config_swh = normalisation_minmax(df['swh'], config, 'swh')
        df.loc[:,'hmax'], config_hmax = normalisation_minmax(df['hmax'], config, 'hmax')
        df.loc[:,'tp'], config_tp = normalisation_minmax(df['tp'], config, 'tp')
        df.loc[:,'t2m'], config_t2m = normalisation_minmax(df['t2m'], config, 't2m')
        df.loc[:,'sst'], config_sst = normalisation_minmax(df['sst'], config, 'sst')
        df.loc[:,'air_density'], config_air_density = normalisation_minmax(df['air_density'], config, 'air_density')
        if symetrique : 
            df.loc[:,'mats'], config_mats = normalisation_minmax(abs(df['mats']), config, 'mats')
            df.loc[:,'maww'], config_maww = normalisation_minmax(abs(df['maww']), config, 'maww')
            df.loc[:,'mwa'], config_mwa = normalisation_minmax(abs(df['mwa']), config, 'mwa')
            df.loc[:,'mah1'], config_mah1 = normalisation_minmax(abs(df['mah1']), config, 'mah1')
            df.loc[:,'mah2'], config_mah2 = normalisation_minmax(abs(df['mah2']), config, 'mah2')
            df.loc[:,'TWA'], config_TWA = normalisation_minmax(abs(df['TWA']), config, 'TWA')
        else : 
            df.loc[:,'mats'], config_mats = normalisation_minmax(df['mats'], config, 'mats')
            df.loc[:,'maww'], config_maww = normalisation_minmax(df['maww'], config, 'maww')
            df.loc[:,'mwa'], config_mwa = normalisation_minmax(df['mwa'], config, 'mwa')
            df.loc[:,'mah1'], config_mah1 = normalisation_minmax(df['mah1'], config, 'mah1')
            df.loc[:,'mah2'], config_mah2 = normalisation_minmax(df['mah2'], config, 'mah2')
            df.loc[:,'TWA'], config_TWA = normalisation_minmax(df['TWA'], config, 'TWA')
        df.loc[:,'ph1'], config_ph1 = normalisation_minmax(df['ph1'], config, 'ph1')
        df.loc[:,'ph2'], config_ph2 = normalisation_minmax(df['ph2'], config, 'ph2')
        df.loc[:,'mpww'], config_mpww = normalisation_minmax(df['mpww'], config, 'mpww')
        df.loc[:,'mpts'], config_mpts = normalisation_minmax(df['mpts'], config, 'mpts')
        df.loc[:,'mwp'], config_mwp = normalisation_minmax(df['mwp'], config, 'mwp')
        df.loc[:,'pmax'], config_pmax = normalisation_minmax(df['pmax'], config, 'pmax')
        df.loc[:,'peak_wave_period'], config_peak_wave_period = normalisation_minmax(df['peak_wave_period'], config, 'peak_wave_period')
        df.loc[:,'msl'], config_msl = normalisation_minmax(df['msl'], config, 'msl')

        if normalize_speed : 
            df.loc[:,'speed'], config_speed = normalisation_minmax(df['speed'], config, 'speed')
        
        if not bool(config) :   
            config_norm['TWS'] = config_TWS
            config_norm['i10fg'] = config_i10fg
            config_norm['gust_diff'] = config_gust_diff
            config_norm['hh1'] = config_hh1
            config_norm['hh2'] = config_hh2
            config_norm['shww'] = config_shww
            config_norm['shts'] = config_shts
            config_norm['swh'] = config_swh
            config_norm['hmax'] = config_hmax
            config_norm['tp'] = config_tp
            config_norm['t2m'] = config_t2m
            config_norm['sst'] = config_sst
            config_norm['air_density'] = config_air_density
            config_norm['mats'] = config_mats
            config_norm['mwa'] = config_mwa
            config_norm['mah1'] = config_mah1
            config_norm['mah2'] = config_mah2
            config_norm['TWA'] = config_TWA
            config_norm['maww'] = config_maww
            config_norm['ph1'] = config_ph1
            config_norm['ph2'] = config_ph2
            config_norm['mpww'] = config_mpww
            config_norm['mpts'] = config_mpts
            config_norm['mwp'] = config_mwp
            config_norm['pmax'] = config_pmax
            config_norm['peak_wave_period'] = config_peak_wave_period
            config_norm['msl'] = config_msl
            if normalize_speed : 
                config_norm['speed'] = config_speed

    elif type == 'standard' :
        df.loc[:,'TWS'], config_TWS = normalisation_standard(df['TWS'], config, 'TWS')
        df.loc[:,'i10fg'], config_i10fg = normalisation_standard(df['i10fg'], config, 'i10fg')
        df.loc[:,'gust_diff'], config_gust_diff = normalisation_standard(df['gust_diff'], config, 'gust_diff')
        df.loc[:,'hh1'], config_hh1 = normalisation_standard(df['hh1'], config, 'hh1')
        df.loc[:,'hh2'], config_hh2 = normalisation_standard(df['hh2'], config, 'hh2')
        df.loc[:,'shww'], config_shww = normalisation_standard(df['shww'], config, 'shww')
        df.loc[:,'shts'], config_shts = normalisation_standard(df['shts'], config, 'shts')
        df.loc[:,'swh'], config_swh = normalisation_standard(df['swh'], config, 'swh')
        df.loc[:,'hmax'], config_hmax = normalisation_standard(df['hmax'], config, 'hmax')
        df.loc[:,'tp'], config_tp = normalisation_standard(df['tp'], config, 'tp')
        df.loc[:,'t2m'], config_t2m = normalisation_standard(df['t2m'], config, 't2m')
        df.loc[:,'sst'], config_sst = normalisation_standard(df['sst'], config, 'sst')
        df.loc[:,'air_density'], config_air_density = normalisation_standard(df['air_density'], config, 'air_density')
        if symetrique : 
            df.loc[:,'mats'], config_mats = normalisation_standard(abs(df['mats']), config, 'mats')
            df.loc[:,'maww'], config_maww = normalisation_standard(abs(df['maww']), config, 'maww')
            df.loc[:,'mwa'], config_mwa = normalisation_standard(abs(df['mwa']), config, 'mwa')
            df.loc[:,'mah1'], config_mah1 = normalisation_standard(abs(df['mah1']), config, 'mah1')
            df.loc[:,'mah2'], config_mah2 = normalisation_standard(abs(df['mah2']), config, 'mah2')
            df.loc[:,'TWA'], config_TWA = normalisation_standard(abs(df['TWA']), config, 'TWA')
        else :
            df.loc[:,'mats'], config_mats = normalisation_standard(df['mats'], config, 'mats')
            df.loc[:,'maww'], config_maww = normalisation_standard(df['maww'], config, 'maww')
            df.loc[:,'mwa'], config_mwa = normalisation_standard(df['mwa'], config, 'mwa')
            df.loc[:,'mah1'], config_mah1 = normalisation_standard(df['mah1'], config, 'mah1')
            df.loc[:,'mah2'], config_mah2 = normalisation_standard(df['mah2'], config, 'mah2')
            df.loc[:,'TWA'], config_TWA = normalisation_standard(df['TWA'], config, 'TWA')
        df.loc[:,'ph1'], config_ph1 = normalisation_standard(df['ph1'], config, 'ph1')
        df.loc[:,'ph2'], config_ph2 = normalisation_standard(df['ph2'], config, 'ph2')
        df.loc[:,'mpww'], config_mpww = normalisation_standard(df['mpww'], config, 'mpww')
        df.loc[:,'mpts'], config_mpts = normalisation_standard(df['mpts'], config, 'mpts')
        df.loc[:,'mwp'], config_mwp = normalisation_standard(df['mwp'], config, 'mwp')
        df.loc[:,'pmax'], config_pmax = normalisation_standard(df['pmax'], config, 'pmax')
        df.loc[:,'peak_wave_period'], config_peak_wave_period = normalisation_standard(df['peak_wave_period'], config, 'peak_wave_period')
        df.loc[:,'msl'], config_msl = normalisation_standard(df['msl'], config, 'msl')

        if normalize_speed : 
            df.loc[:,'speed'], config_speed = normalisation_standard(df['speed'], config, 'speed')

        if not bool(config) :   
            config_norm['TWS'] = config_TWS
            config_norm['i10fg'] = config_i10fg
            config_norm['gust_diff'] = config_gust_diff
            config_norm['hh1'] = config_hh1
            config_norm['hh2'] = config_hh2
            config_norm['shww'] = config_shww
            config_norm['shts'] = config_shts
            config_norm['swh'] = config_swh
            config_norm['hmax'] = config_hmax
            config_norm['tp'] = config_tp
            config_norm['t2m'] = config_t2m
            config_norm['sst'] = config_sst
            config_norm['air_density'] = config_air_density
            config_norm['mats'] = config_mats
            config_norm['mwa'] = config_mwa
            config_norm['mah1'] = config_mah1
            config_norm['mah2'] = config_mah2
            config_norm['TWA'] = config_TWA
            config_norm['maww'] = config_maww
            config_norm['ph1'] = config_ph1
            config_norm['ph2'] = config_ph2
            config_norm['mpww'] = config_mpww
            config_norm['mpts'] = config_mpts
            config_norm['mwp'] = config_mwp
            config_norm['pmax'] = config_pmax
            config_norm['peak_wave_period'] = config_peak_wave_period
            config_norm['msl'] = config_msl
            if normalize_speed : 
                config_norm['speed'] = config_speed

    else : #type == manuel
        if historique : 
            if not bool(config) : 
                #Vent moyen 0-45 kts
                config_TWS = {
                    'mini' : 0,
                    'maxi' : 60
                }
                #Rafales histo 0-70kts
                config_i10fg = {
                    'mini' : 0,
                    'maxi' : 70
                }
                #Gust-diff relative 0-10
                config_gust_diff = {
                    'mini' : 0,
                    'maxi' : 15
                }
                #Wave height 0-10m
                config_hh1 = {
                    'mini' : 0,
                    'maxi' : 10
                }
                config_hh2 = {
                    'mini' : 0,
                    'maxi' : 10
                }
                config_shww = {
                    'mini' : 0,
                    'maxi' : 10
                }
                config_shts = {
                    'mini' : 0,
                    'maxi' : 10
                }
                config_swh = {
                    'mini' : 0,
                    'maxi' : 10
                }
                #hmax 0-15m
                config_hmax = {
                    'mini' : 0,
                    'maxi' : 15
                }
                #Precip 0-40mm (m) en 1h
                config_tp = {
                    'mini' : 0,
                    'maxi' : 40e-3
                }
                #température 0-50°C --> 273 - 323K
                config_t2m = {
                    'mini' : 273,
                    'maxi' : 323
                }
                #Température eau 0-30°C --> 273 - 303K 
                config_sst = {
                    'mini' : 273,
                    'maxi' : 303
                }
                #air density (kg.m-3) 1.05 - 1.40 kg.m-3
                config_air_density = {
                    'mini' : 1.05,
                    'maxi' : 1.40
                }
                #periodes 0-30s
                config_ph1 = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_ph2 = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_mpww = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_mpts = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_mwp = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_pmax = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_peak_wave_period = {
                    'mini' : 0,
                    'maxi' : 30
                }
                #Pression 910-1050hPa (Pa)
                config_msl = {
                    'mini' : 91000,
                    'maxi' : 105000
                }
                

                df.loc[:,'TWS'] = df['TWS'].apply(lambda x: normalisation_minmax_manuel(config_TWS['mini'],config_TWS['maxi'],x))
                df.loc[:,'i10fg'] = df['i10fg'].apply(lambda x: normalisation_minmax_manuel(config_i10fg['mini'],config_i10fg['maxi'],x))
                df.loc[:,'gust_diff'] = df['gust_diff'].apply(lambda x: normalisation_minmax_manuel(config_gust_diff['mini'],config_gust_diff['maxi'],x))
                df.loc[:,'hh1'] = df['hh1'].apply(lambda x: normalisation_minmax_manuel(config_hh1['mini'],config_hh1['maxi'],x))
                df.loc[:,'hh2'] = df['hh2'].apply(lambda x: normalisation_minmax_manuel(config_hh2['mini'],config_hh2['maxi'],x))
                df.loc[:,'shww'] = df['shww'].apply(lambda x: normalisation_minmax_manuel(config_shww['mini'],config_shww['maxi'],x))
                df.loc[:,'shts'] = df['shts'].apply(lambda x: normalisation_minmax_manuel(config_shts['mini'],config_shts['maxi'],x))
                df.loc[:,'swh'] = df['swh'].apply(lambda x: normalisation_minmax_manuel(config_swh['mini'],config_swh['maxi'],x))
                df.loc[:,'hmax'] = df['hmax'].apply(lambda x: normalisation_minmax_manuel(config_hmax['mini'],config_hmax['maxi'],x))
                df.loc[:,'tp'] = df['tp'].apply(lambda x: normalisation_minmax_manuel(config_tp['mini'],config_tp['maxi'],x))
                df.loc[:,'t2m'] = df['t2m'].apply(lambda x: normalisation_minmax_manuel(config_t2m['mini'],config_t2m['maxi'],x))
                df.loc[:,'sst'] = df['sst'].apply(lambda x: normalisation_minmax_manuel(config_sst['mini'],config_sst['maxi'],x))
                df.loc[:,'air_density'] = df['air_density'].apply(lambda x: normalisation_minmax_manuel(config_air_density['mini'],config_air_density['maxi'],x))
                df.loc[:,'ph1'] = df['ph1'].apply(lambda x: normalisation_minmax_manuel(config_ph1['mini'],config_ph1['maxi'],x))
                df.loc[:,'ph2'] = df['ph2'].apply(lambda x: normalisation_minmax_manuel(config_ph2['mini'],config_ph2['maxi'],x))
                df.loc[:,'mpww'] = df['mpww'].apply(lambda x: normalisation_minmax_manuel(config_mpww['mini'],config_mpww['maxi'],x))
                df.loc[:,'mpts'] = df['mpts'].apply(lambda x: normalisation_minmax_manuel(config_mpts['mini'],config_mpts['maxi'],x))
                df.loc[:,'mwp'] = df['mwp'].apply(lambda x: normalisation_minmax_manuel(config_mwp['mini'],config_mwp['maxi'],x))
                df.loc[:,'pmax'] = df['pmax'].apply(lambda x: normalisation_minmax_manuel(config_pmax['mini'],config_pmax['maxi'],x))
                df.loc[:,'peak_wave_period'] = df['peak_wave_period'].apply(lambda x: normalisation_minmax_manuel(config_peak_wave_period['mini'],config_peak_wave_period['maxi'],x))
                df.loc[:,'msl'] = df['msl'].apply(lambda x: normalisation_minmax_manuel(config_msl['mini'],config_msl['maxi'],x))
                if normalize_speed : 
                    #Speed 0-50 kts
                    config_speed = {
                    'mini' : 0,
                    'maxi' : 50
                    }
                    df.loc[:,'speed'] = df['speed'].apply(lambda x: normalisation_minmax_manuel(config_speed['mini'],config_speed['maxi'],x))


            else : 
                df.loc[:,'TWS'], config_TWS = normalisation_minmax(df['TWS'], config, 'TWS')
                df.loc[:,'i10fg'], config_i10fg = normalisation_minmax(df['i10fg'], config, 'i10fg')
                df.loc[:,'gust_diff'], config_gust_diff = normalisation_minmax(df['gust_diff'], config, 'gust_diff')
                df.loc[:,'hh1'], config_hh1 = normalisation_minmax(df['hh1'], config, 'hh1')
                df.loc[:,'hh2'], config_hh2 = normalisation_minmax(df['hh2'], config, 'hh2')
                df.loc[:,'shww'], config_shww = normalisation_minmax(df['shww'], config, 'shww')
                df.loc[:,'shts'], config_shts = normalisation_minmax(df['shts'], config, 'shts')
                df.loc[:,'swh'], config_swh = normalisation_minmax(df['swh'], config, 'swh')
                df.loc[:,'hmax'], config_hmax = normalisation_minmax(df['hmax'], config, 'hmax')
                df.loc[:,'tp'], config_tp = normalisation_minmax(df['tp'], config, 'tp')
                df.loc[:,'t2m'], config_t2m = normalisation_minmax(df['t2m'], config, 't2m')
                df.loc[:,'sst'], config_sst = normalisation_minmax(df['sst'], config, 'sst')
                df.loc[:,'air_density'], config_air_density = normalisation_minmax(df['air_density'], config, 'air_density')
                df.loc[:,'ph1'], config_ph1 = normalisation_minmax(df['ph1'], config, 'ph1')
                df.loc[:,'ph2'], config_ph2 = normalisation_minmax(df['ph2'], config, 'ph2')
                df.loc[:,'mpww'], config_mpww = normalisation_minmax(df['mpww'], config, 'mpww')
                df.loc[:,'mpts'], config_mpts = normalisation_minmax(df['mpts'], config, 'mpts')
                df.loc[:,'mwp'], config_mwp = normalisation_minmax(df['mwp'], config, 'mwp')
                df.loc[:,'pmax'], config_pmax = normalisation_minmax(df['pmax'], config, 'pmax')
                df.loc[:,'peak_wave_period'], config_peak_wave_period = normalisation_minmax(df['peak_wave_period'], config, 'peak_wave_period')
                df.loc[:,'msl'], config_msl = normalisation_minmax(df['msl'], config, 'msl')

                if normalize_speed : 
                    df.loc[:,'speed'], config_speed = normalisation_minmax(df['speed'], config, 'speed')


            #angles vagues/vent -180 - 180° 
            df.loc[:,'mats'] = df['mats'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))
            df.loc[:,'maww'] = df['maww'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))
            df.loc[:,'mwa'] = df['mwa'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))
            df.loc[:,'mah1'] = df['mah1'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))
            df.loc[:,'mah2'] = df['mah2'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))
            df.loc[:,'TWA'] = df['TWA'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))
           

        else : 
            #CHANGER LES PARAMS MANUELS pour des params plus intelligents
            if not bool(config) : 
                #Vent moyen 0-45 kts
                config_TWS = {
                    'mini' : 0,
                    'maxi' : 45
                }
                #Rafales histo 0-70kts
                config_i10fg = {
                    'mini' : 0,
                    'maxi' : 70
                }
                #Gust-diff relative 0-10
                config_gust_diff = {
                    'mini' : 0,
                    'maxi' : 10
                }
                #Wave height 0-10m
                config_hh1 = {
                    'mini' : 0,
                    'maxi' : 10
                }
                config_hh2 = {
                    'mini' : 0,
                    'maxi' : 10
                }
                config_shww = {
                    'mini' : 0,
                    'maxi' : 10
                }
                config_shts = {
                    'mini' : 0,
                    'maxi' : 10
                }
                config_swh = {
                    'mini' : 0,
                    'maxi' : 10
                }
                #hmax 0-15m
                config_hmax = {
                    'mini' : 0,
                    'maxi' : 15
                }
                #Precip 0-40mm (m) en 1h
                config_tp = {
                    'mini' : 0,
                    'maxi' : 40e-3
                }
                #température 0-50°C --> 273 - 323K
                config_t2m = {
                    'mini' : 273,
                    'maxi' : 323
                }
                #Température eau 0-30°C --> 273 - 303K 
                config_sst = {
                    'mini' : 273,
                    'maxi' : 303
                }
                #air density (kg.m-3) 1.05 - 1.40 kg.m-3
                config_air_density = {
                    'mini' : 1.05,
                    'maxi' : 1.40
                }
                #periodes 0-30s
                config_ph1 = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_ph2 = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_mpww = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_mpts = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_mwp = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_pmax = {
                    'mini' : 0,
                    'maxi' : 30
                }
                config_peak_wave_period = {
                    'mini' : 0,
                    'maxi' : 30
                }
                #Pression 910-1050hPa (Pa)
                config_msl = {
                    'mini' : 91000,
                    'maxi' : 105000
                }
                

                df.loc[:,'TWS'] = df['TWS'].apply(lambda x: normalisation_minmax_manuel(config_TWS['mini'],config_TWS['maxi'],x))
                df.loc[:,'i10fg'] = df['i10fg'].apply(lambda x: normalisation_minmax_manuel(config_i10fg['mini'],config_i10fg['maxi'],x))
                df.loc[:,'gust_diff'] = df['gust_diff'].apply(lambda x: normalisation_minmax_manuel(config_gust_diff['mini'],config_gust_diff['maxi'],x))
                df.loc[:,'hh1'] = df['hh1'].apply(lambda x: normalisation_minmax_manuel(config_hh1['mini'],config_hh1['maxi'],x))
                df.loc[:,'hh2'] = df['hh2'].apply(lambda x: normalisation_minmax_manuel(config_hh2['mini'],config_hh2['maxi'],x))
                df.loc[:,'shww'] = df['shww'].apply(lambda x: normalisation_minmax_manuel(config_shww['mini'],config_shww['maxi'],x))
                df.loc[:,'shts'] = df['shts'].apply(lambda x: normalisation_minmax_manuel(config_shts['mini'],config_shts['maxi'],x))
                df.loc[:,'swh'] = df['swh'].apply(lambda x: normalisation_minmax_manuel(config_swh['mini'],config_swh['maxi'],x))
                df.loc[:,'hmax'] = df['hmax'].apply(lambda x: normalisation_minmax_manuel(config_hmax['mini'],config_hmax['maxi'],x))
                df.loc[:,'tp'] = df['tp'].apply(lambda x: normalisation_minmax_manuel(config_tp['mini'],config_tp['maxi'],x))
                df.loc[:,'t2m'] = df['t2m'].apply(lambda x: normalisation_minmax_manuel(config_t2m['mini'],config_t2m['maxi'],x))
                df.loc[:,'sst'] = df['sst'].apply(lambda x: normalisation_minmax_manuel(config_sst['mini'],config_sst['maxi'],x))
                df.loc[:,'air_density'] = df['air_density'].apply(lambda x: normalisation_minmax_manuel(config_air_density['mini'],config_air_density['maxi'],x))
                df.loc[:,'ph1'] = df['ph1'].apply(lambda x: normalisation_minmax_manuel(config_ph1['mini'],config_ph1['maxi'],x))
                df.loc[:,'ph2'] = df['ph2'].apply(lambda x: normalisation_minmax_manuel(config_ph2['mini'],config_ph2['maxi'],x))
                df.loc[:,'mpww'] = df['mpww'].apply(lambda x: normalisation_minmax_manuel(config_mpww['mini'],config_mpww['maxi'],x))
                df.loc[:,'mpts'] = df['mpts'].apply(lambda x: normalisation_minmax_manuel(config_mpts['mini'],config_mpts['maxi'],x))
                df.loc[:,'mwp'] = df['mwp'].apply(lambda x: normalisation_minmax_manuel(config_mwp['mini'],config_mwp['maxi'],x))
                df.loc[:,'pmax'] = df['pmax'].apply(lambda x: normalisation_minmax_manuel(config_pmax['mini'],config_pmax['maxi'],x))
                df.loc[:,'peak_wave_period'] = df['peak_wave_period'].apply(lambda x: normalisation_minmax_manuel(config_peak_wave_period['mini'],config_peak_wave_period['maxi'],x))
                df.loc[:,'msl'] = df['msl'].apply(lambda x: normalisation_minmax_manuel(config_msl['mini'],config_msl['maxi'],x))
                if normalize_speed : 
                    #Speed 0-50 kts
                    config_speed = {
                    'mini' : 0,
                    'maxi' : 50
                    }
                    df.loc[:,'speed'] = df['speed'].apply(lambda x: normalisation_minmax_manuel(config_speed['mini'],config_speed['maxi'],x))


            else : 
                df.loc[:,'TWS'], config_TWS = normalisation_minmax(df['TWS'], config, 'TWS')
                df.loc[:,'i10fg'], config_i10fg = normalisation_minmax(df['i10fg'], config, 'i10fg')
                df.loc[:,'gust_diff'], config_gust_diff = normalisation_minmax(df['gust_diff'], config, 'gust_diff')
                df.loc[:,'hh1'], config_hh1 = normalisation_minmax(df['hh1'], config, 'hh1')
                df.loc[:,'hh2'], config_hh2 = normalisation_minmax(df['hh2'], config, 'hh2')
                df.loc[:,'shww'], config_shww = normalisation_minmax(df['shww'], config, 'shww')
                df.loc[:,'shts'], config_shts = normalisation_minmax(df['shts'], config, 'shts')
                df.loc[:,'swh'], config_swh = normalisation_minmax(df['swh'], config, 'swh')
                df.loc[:,'hmax'], config_hmax = normalisation_minmax(df['hmax'], config, 'hmax')
                df.loc[:,'tp'], config_tp = normalisation_minmax(df['tp'], config, 'tp')
                df.loc[:,'t2m'], config_t2m = normalisation_minmax(df['t2m'], config, 't2m')
                df.loc[:,'sst'], config_sst = normalisation_minmax(df['sst'], config, 'sst')
                df.loc[:,'air_density'], config_air_density = normalisation_minmax(df['air_density'], config, 'air_density')
                df.loc[:,'ph1'], config_ph1 = normalisation_minmax(df['ph1'], config, 'ph1')
                df.loc[:,'ph2'], config_ph2 = normalisation_minmax(df['ph2'], config, 'ph2')
                df.loc[:,'mpww'], config_mpww = normalisation_minmax(df['mpww'], config, 'mpww')
                df.loc[:,'mpts'], config_mpts = normalisation_minmax(df['mpts'], config, 'mpts')
                df.loc[:,'mwp'], config_mwp = normalisation_minmax(df['mwp'], config, 'mwp')
                df.loc[:,'pmax'], config_pmax = normalisation_minmax(df['pmax'], config, 'pmax')
                df.loc[:,'peak_wave_period'], config_peak_wave_period = normalisation_minmax(df['peak_wave_period'], config, 'peak_wave_period')
                df.loc[:,'msl'], config_msl = normalisation_minmax(df['msl'], config, 'msl')

                if normalize_speed : 
                    df.loc[:,'speed'], config_speed = normalisation_minmax(df['speed'], config, 'speed')


            #angles vagues/vent -180 - 180° 
            df.loc[:,'mats'] = df['mats'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))
            df.loc[:,'maww'] = df['maww'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))
            df.loc[:,'mwa'] = df['mwa'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))
            df.loc[:,'mah1'] = df['mah1'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))
            df.loc[:,'mah2'] = df['mah2'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))
            df.loc[:,'TWA'] = df['TWA'].apply(lambda x: normalisation_angle(x, symetrique=symetrique))

        if not bool(config) :   
            config_norm['TWS'] = config_TWS
            config_norm['i10fg'] = config_i10fg
            config_norm['gust_diff'] = config_gust_diff
            config_norm['hh1'] = config_hh1
            config_norm['hh2'] = config_hh2
            config_norm['shww'] = config_shww
            config_norm['shts'] = config_shts
            config_norm['swh'] = config_swh
            config_norm['hmax'] = config_hmax
            config_norm['tp'] = config_tp
            config_norm['t2m'] = config_t2m
            config_norm['sst'] = config_sst
            config_norm['air_density'] = config_air_density
            config_norm['ph1'] = config_ph1
            config_norm['ph2'] = config_ph2
            config_norm['mpww'] = config_mpww
            config_norm['mpts'] = config_mpts
            config_norm['mwp'] = config_mwp
            config_norm['pmax'] = config_pmax
            config_norm['peak_wave_period'] = config_peak_wave_period
            config_norm['msl'] = config_msl
            if normalize_speed : 
                config_norm['speed'] = config_speed

    if bool(config) : 
        return df, None
    else :
        return df, config_norm

def drop_columns(df, c_dict) : 
    for column in c_dict : 
        if c_dict[column] == 0 : 
            df.drop(column, axis=1, inplace=True, errors='ignore')

def pipeline_preprocessing(df_input, speed_treshold_sup = 160, speed_treshold_inf = 30, norm_type = 'minmax', remove_outliers=False, normalize_speed=False, historique=True, symetrique=True) : 
    df = df_input.copy()
    config = {
        'type' : norm_type, 
        'remove_outliers' : remove_outliers, 
        'normalize_speed' : normalize_speed, 
        'historique' : historique, 
        'symetrique' : symetrique
    }

    #On met un treshold sur les valeurs de TWA trop haute ou trop basse 
    df.loc[(abs(df.TWA) > speed_treshold_sup), 'speed'] = 0
    df.loc[(abs(df.TWA) < speed_treshold_inf), 'speed'] = 0
    

    config['speed_treshold_sup'] = speed_treshold_sup
    config['speed_treshold_inf'] = speed_treshold_inf

    #On normalise toutes les données
    df, config_norm = normalize_df(df, type=norm_type,remove_outliers=remove_outliers, normalize_speed=normalize_speed, historique=historique, symetrique=symetrique)
    config.update(config_norm)

    #Data augmentation for 0
    df.append([df.loc[(abs(df.TWA) > speed_treshold_sup)]]*5,ignore_index=True)
    df.append([df.loc[(abs(df.TWA) < speed_treshold_sup)]]*5,ignore_index=True)

    #On enlève les param inutiles
    c_dict = {
    'lat' : 0,
    'lon' : 0,
    'datetime' : 0,
    'i10fg' : 0,
    'msl' : 1,
    't2m' : 1,
    'sst' : 0,
    'tp' : 1,
    'hmax' : 0,
    'shts' : 1,
    'mpts' : 0,
    'shww' : 1,
    'mpww' : 1,
    'swh' : 1,
    'mwp' : 1,
    'speed' : 1,
    'TWS' : 1,
    'gust_diff' : 1,
    'TWA' : 1,
    'mats' : 0,
    'maww' : 0,
    'mwa' : 1,
    'mah1' : 1,
    'mah2' : 1,
    'air_density' : 0,
    'ph1' : 1,
    'ph2' : 1,
    'hh1' : 1,
    'hh2' : 1,
    'peak_wave_period' : 0,
    'pmax' : 0
    }

    config['cdict'] = c_dict
    drop_columns(df, c_dict)

    #Save config file

    return df, config

def pipeline_preprocessing_from_config(df_input, config) : 
    df = df_input.copy()
    #On met un treshold sur les valeurs de TWA trop haute ou trop basse 
    speed_treshold_sup = config['speed_treshold_sup']
    speed_treshold_inf = config['speed_treshold_inf']
    df.loc[(abs(df.TWA) > speed_treshold_sup), 'speed'] = 0
    df.loc[(abs(df.TWA) < speed_treshold_inf), 'speed'] = 0

    #On normalise toutes les données
    norm_type = config['type'] 
    remove_outliers = config['remove_outliers']
    normalize_speed = config['normalize_speed']
    historique = config['historique']
    symetrique = config['symetrique']
    df, _ = normalize_df(df, type=norm_type,remove_outliers=remove_outliers, normalize_speed=normalize_speed, historique=historique, symetrique=symetrique, config=config)

    #On enlève les param inutiles
    c_dict = config['cdict']
    drop_columns(df, c_dict)

    return df