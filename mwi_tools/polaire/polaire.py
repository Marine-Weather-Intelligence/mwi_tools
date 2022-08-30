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
    ax.plot(df_cloud_speed.TWA*np.pi/180, df_cloud_speed.speed, 'bo')
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
        ax[i//3, i-(i//3)*3].plot(df_cloud_speed.TWA*np.pi/180, df_cloud_speed.speed, 'bo', label="training_points")
        ax[i//3, i-(i//3)*3].set_theta_direction(-1)
        ax[i//3, i-(i//3)*3].set_theta_offset(np.pi / 2.0)
        ax[i//3, i-(i//3)*3].set_rlabel_position(-1)  # Move radial labels away from plotted line
        ax[i//3, i-(i//3)*3].grid(True)
        ax[i//3, i-(i//3)*3].legend()
    plt.show()