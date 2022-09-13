import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_polaire_df(file, true_polaire=False) : 
    f = open(file, "r")
    file_table = f.readlines()
    first_line = file_table[0].split('\t')
    first_line[-1] = first_line[-1][:-1]
    nb_TWS= len(first_line)
    nb_TWA = len(file_table)
    table = np.zeros((nb_TWA, nb_TWS))
    table[0,1:] = first_line[1:]
    if true_polaire : 
        for i in range (1, len(table[0])) : 
            speed = int(table[0, i])
            speed = speed / 1.1
            table[0, i] = round(speed,0)
    for i in range (1, nb_TWA) : 
        line = file_table[i].split('\t')
        line[-1] = line[-1][:-1]
        for j in range(len(line)) : 
            if float(line[j]) < 0 : 
                line[j] = 0
        table[i,:] = line
    df = pd.DataFrame(table[1:,1:], columns = table[0,1:])
    df.insert(0,'TWA',table[1:,0])
    return df

def closest_value_index(input_list, input_value):
    arr = np.asarray(input_list)
    i = (np.abs(arr - input_value)).argmin()
    return i


def set_ax_plot_polaire(df,ax, speed, index=None, nom=None, color='r', label="", symetrique=False) : 
    if index != None : 
        s = ax.shape
        if len(ax.shape) == 2 : 
            line = index//s[1]
            axe = ax[line, index - line*s[1]]
        else : 
            axe = ax[index]
    else : 
        axe = ax
        
    if speed == None : 
        #On plot toutes les polaires
        if symetrique : 
            x = df['TWA']*np.pi/180
        else : 
            x = pd.concat([df['TWA']*np.pi/180,(2*np.pi-df['TWA']*np.pi/180).iloc[::-1]])
        for col_name in df.columns : 
            if col_name != 'TWA' : 
                if symetrique : 
                    col = df[col_name]
                else : 
                    col = pd.concat([df[col_name],df[col_name].iloc[::-1]])
                axe.plot(x, col, label=str(col_name)+" kts")
        axe.set_title("Polaire complete\n"+str(nom or ''))
        axe.legend()
        
    elif isinstance(speed, list) : 
        #On plot toutes les polaires qui sont dans speed
        if symetrique : 
            x = df['TWA']*np.pi/180
        else : 
            x = pd.concat([df['TWA']*np.pi/180,(2*np.pi-df['TWA']*np.pi/180).iloc[::-1]])
        for col_name in df.columns : 
            if col_name != 'TWA' : 
                if symetrique : 
                    col = df[col_name]
                else : 
                    col = pd.concat([df[col_name],df[col_name].iloc[::-1]])
                axe.plot(x, col, label=str(col_name)+" kts")
        axe.set_title("Polaire complete\n"+str(nom or ''))
        axe.legend()
    else : 
        #On obtient l'indice du vent le plus proche
        wind_speed_index = closest_value_index(df.columns[1:], speed)
        
        #On plot uniquement cette polaire
        axe.plot(df['TWA']*np.pi/180, df.iloc[:,wind_speed_index+1], color, label=label)
        if not(symetrique) : 
            axe.plot(2*np.pi-df['TWA']*np.pi/180, df.iloc[:,wind_speed_index+1], color)
        

        axe.set_title("Wind speed " +str(df.columns[wind_speed_index+1])+" kts\n"+str(nom or ''))
        
    axe.set_theta_direction(-1)
    axe.set_theta_offset(np.pi / 2.0)
    axe.set_rlabel_position(-1)  # Move radial labels away from plotted line
    axe.grid(True)
    if symetrique : 
            axe.set_thetamin(0)
            axe.set_thetamax(180)

    if speed != None :
        return df.columns[wind_speed_index+1]

def plot_polaire(df, speed=None, nom=None, symetrique=False) :
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10,10))
    set_ax_plot_polaire(df, ax, speed, nom=nom, symetrique=symetrique)
    plt.show()
    
def plot_two_polaire(df1, df2, speed=None, nom1= None, nom2 = None, symetrique=False) : 
    fig, ax = plt.subplots(nrows = 1, ncols=2, subplot_kw={'projection': 'polar'}, figsize=(20,20), sharey=True)
    set_ax_plot_polaire(df1, ax, speed, index=0, nom=nom1, symetrique=symetrique)
    set_ax_plot_polaire(df2, ax, speed, index=1, nom=nom2, symetrique=symetrique)
    plt.show()

def plot_polaire_and_cloud(df, df_cloud, speed, symetrique=False, nom=None) :
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10,10))
    df_cloud_speed = df_cloud.loc[(df_cloud['TWS'] >= speed-0.5) & (df_cloud['TWS'] <= speed+0.5)].copy()
    if symetrique : 
        df_cloud_speed.loc[df_cloud['TWA'] < 0, ['TWA']] = df_cloud_speed.loc[df_cloud['TWA'] < 0, ['TWA']].apply(lambda x : -x)
    ax.plot(df_cloud_speed.TWA*np.pi/180, df_cloud_speed.speed, 'bo', markersize=5)
    set_ax_plot_polaire(df, ax, speed, nom=nom, symetrique=symetrique, label="predicted polar")
    plt.show()

def plot_multiple_polaire_and_cloud(df, df_cloud, df_true, symetrique=False, nom=None) :
    wind_list = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
    fig, ax = plt.subplots(nrows = 6, ncols=3, subplot_kw={'projection': 'polar'}, figsize=(20,40), sharey=True)
    for i in range(18) :
        speed = wind_list[i] 
        speed = set_ax_plot_polaire(df_true, ax, speed,index=i, nom=nom, color='g', label="true_polar", symetrique=symetrique)
        set_ax_plot_polaire(df, ax, speed,index=i, nom=nom, color='r', label="predicted_polar", symetrique=symetrique)
        df_cloud_speed = df_cloud.loc[(df_cloud['TWS'] >= speed-0.5) & (df_cloud['TWS'] <= speed+0.5)].copy()
        if symetrique : 
            df_cloud_speed.loc[df_cloud['TWA'] < 0, ['TWA']] = df_cloud_speed.loc[df_cloud['TWA'] < 0, ['TWA']].apply(lambda x : -x)
        ax[i//3, i-(i//3)*3].plot(df_cloud_speed.TWA*np.pi/180, df_cloud_speed.speed, 'bo', label="training_points", markersize=3)
        ax[i//3, i-(i//3)*3].set_theta_direction(-1)
        ax[i//3, i-(i//3)*3].set_theta_offset(np.pi / 2.0)
        ax[i//3, i-(i//3)*3].set_rlabel_position(-1)  # Move radial labels away from plotted line
        ax[i//3, i-(i//3)*3].grid(True)
        ax[i//3, i-(i//3)*3].legend()
        if symetrique : 
            ax[i//3, i-(i//3)*3].set_thetamin(0)
            ax[i//3, i-(i//3)*3].set_thetamax(180)
    plt.show()


def create_entry(TWS, TWA, gust=None, temp_air=288, temp_eau=288, pressure=101300, precip=0, hmax=0, pmax=7.4, peak_wave_period=10.9 ,shts=1.5, mpts=9, mats=0, shww=0.5, mpww=4, maww=0, swh=1.5, mwp=8.6, mwa=0, hh1=1, ph1=10, mah1=0, hh2=0.5, ph2=8.5, mah2=0, air_density=1.225) : 
    if(gust == None) : 
        gust = TWS
    gust_diff = gust - TWS
    d = {'TWS': [TWS], 'TWA': [TWA], 'i10fg' : [gust], 't2m' : [temp_air], 'msl' : [pressure], 'sst':[temp_eau], 'tp':[precip], 'hmax':[hmax], 'mpts':[mpts], 'mpww':[mpww], 'mwp':[mwp], 'swh':[swh], 'shts':[shts], 'shww':[shww], 'gust_diff':[gust_diff], 'mats':[mats], 'maww':[maww], 'mwa':[mwa], 'mah1':[mah1], 'mah2':[mah2], 'air_density':[air_density], 'ph1':[ph1], 'ph2':[ph2], 'hh1':[hh1], 'hh2':[hh2], 'peak_wave_period':[peak_wave_period], 'pmax':[pmax]}
    df = pd.DataFrame(data=d)
    return df
    
    
    
def create_wind_polar_file(reg, file, pipeline_preprocessing_from_config, config) : 
    #Cree un fichier de polaire de vitesse en fonction de la force du vent et TWA 
    #Prend les autres paramètres comme valeur nominale 
    
    f=open(file, "w")
    TWA_list = [10, 15, 20, 25, 30,35,40,45,50,60,70,80,90,100,110,120,130,135,140,145,150,155,160,170,180]
    TWS_list = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26, 28, 30,32,34]
    
    #Prmeière ligne
    line = "TWA/TWS"
    for TWS in TWS_list : 
        line+="\t"+str(TWS)
    f.write(line+"\n")
    
    #Suite des lignes
    for TWA in TWA_list : 
        line = str(TWA)
        for TWS in TWS_list : 
            entry = create_entry(TWS, TWA)
            entry = pipeline_preprocessing_from_config(entry, config)
            speed = reg.predict(entry[['TWA','TWS']])
            line+= "\t"+str(round(speed[0],1))
        f.write(line+"\n")
    f.close()


def create_wind_polar_file_full(reg, file, pipeline_preprocessing_from_config, config) : 
    #Cree un fichier de polaire de vitesse en fonction de la force du vent et TWA 
    #Prend les autres paramètres comme valeur nominale 
    
    f=open(file, "w")
    TWA_list = [10, 15, 20, 25, 30,35,40,45,50,60,70,80,90,100,110,120,130,135,140,145,150,155,160,170,180]
    TWS_list = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26, 28, 30,32,34]
    
    #Prmeière ligne
    line = "TWA/TWS"
    for TWS in TWS_list : 
        line+="\t"+str(TWS)
    f.write(line+"\n")
    
    #Suite des lignes
    for TWA in TWA_list : 
        line = str(TWA)
        for TWS in TWS_list : 
            entry = create_entry(TWS, TWA)
            entry = pipeline_preprocessing_from_config(entry, config)
            entry.drop('speed', axis=1, inplace=True, errors='ignore')
            speed = reg.predict(entry)
            line+= "\t"+str(round(speed[0],1))
        f.write(line+"\n")
    f.close()