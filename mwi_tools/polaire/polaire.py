import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_polaire_df(file) : 
    f = open(file, "r")
    file_table = f.readlines()
    first_line = file_table[0].split('\t')
    first_line[-1] = first_line[-1][:-1]
    nb_TWS= len(first_line)
    nb_TWA = len(file_table)
    table = np.zeros((nb_TWA, nb_TWS))
    table[0,1:] = first_line[1:]
    for i in range (1, nb_TWA) : 
        line = file_table[i].split('\t')
        line[-1] = line[-1][:-1]
        table[i,:] = line
    df = pd.DataFrame(table[1:,1:], columns = table[0,1:])
    df.insert(0,'TWA',table[1:,0])
    return df

def closest_value_index(input_list, input_value):
    arr = np.asarray(input_list)
    i = (np.abs(arr - input_value)).argmin()
    return i


def set_ax_plot_polaire(df,ax, speed, index=None, nom=None) : 
    if index != None : 
        axe = ax[index]
    else : 
        axe = ax
        
    if speed == None : 
        #On plot toutes les polaires
        x = pd.concat([df['TWA']*np.pi/180,(2*np.pi-df['TWA']*np.pi/180).iloc[::-1]])
        for col_name in df.columns : 
            if col_name != 'TWA' : 
                col = pd.concat([df[col_name],df[col_name].iloc[::-1]])
                axe.plot(x, col, label=col_name)
        axe.set_title("Polaire complete\n"+str(nom or ''))
        axe.legend()
        
    else : 
        #On obtient l'indice du vent le plus proche
        wind_speed_index = closest_value_index(df.columns[1:], speed)
        
        #On plot uniquement cette polaire
        axe.plot(df['TWA']*np.pi/180, df.iloc[:,wind_speed_index+1], 'r')
        axe.plot(2*np.pi-df['TWA']*np.pi/180, df.iloc[:,wind_speed_index+1], 'r')
        

        axe.set_title("Wind speed " +str(df.columns[wind_speed_index+1])+" kts\n"+str(nom or ''))
        
    axe.set_theta_direction(-1)
    axe.set_theta_offset(np.pi / 2.0)
    axe.set_rlabel_position(-1)  # Move radial labels away from plotted line
    axe.grid(True)

def plot_polaire(df, speed=None, nom=None) :
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10,10))
    set_ax_plot_polaire(df, ax, speed, nom=nom)
    plt.show()
    
def plot_two_polaire(df1, df2, speed=None, nom1= None, nom2 = None) : 
    fig, ax = plt.subplots(nrows = 1, ncols=2, subplot_kw={'projection': 'polar'}, figsize=(20,20), sharey=True)
    set_ax_plot_polaire(df1, ax, speed, index=0, nom=nom1)
    set_ax_plot_polaire(df2, ax, speed, index=1, nom=nom2)
    plt.show()