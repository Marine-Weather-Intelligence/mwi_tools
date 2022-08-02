import pandas as pd

def convert_toCSV(selected_parameter:str,name_grib:str, origine:str, destination:str):
    """create a csv from a grib with a parameter

    Args:
        selected_parameter (str): interesting parameter (add a space at the end)
        name_grib (str): _description_
        origine (str): _description_
        destination (str): _description_
    """
    print('---convert_toCSV')
    
    name_out_file=selected_parameter+'_'+name_grib[:-4]+'csv'

    os.system('grib_get_data -F "%.4f" -p validityDate,validityTime -w shortName='+ selected_parameter + ' ' + origine + '/' + name_grib + ' > ' + destination + '/' + name_out_file) 



def clean_data3(messy_file:str)->pd.dataFrame: 
    """return the dataframe from a csv file with 0.5° accuracy in space 

    Args:
        messy_file (str): _description_

    Returns:
        pd: _description_
    """
    print("-------------clean_data3")
    
    #csv lisible ( on remplace les espaces par des , )
    with open(messy_file, 'r') as f_in, open('temp_00.csv', 'w') as f_out:# on ouvre messy file en lecture seul et on écrit dans temp_00
        f_out.write(next(f_in))
        [f_out.write(','.join(line.split()) + '\n') for line in f_in]

    #ouverture du datatframe
    col=["Latitude","Longitude","Value","validityDate","validityTime"]
    
    df1=pd.read_csv('temp_00.csv', header=0,names=col,low_memory=False)
    
    df1.drop(df1.loc[df1['Latitude']=='Latitude'].index, inplace=True) # lignes avec les noms de colonnes

    #on attribue les bons types aux colonnes 
    df2=df1.astype({'Latitude': float, 'Longitude': float, "Value": float,"validityDate": int,"validityTime": int})

    #on enleve les lignes inutiles
    df2.drop(df2.loc[df2['Latitude'] % 0.5 !=0].index, inplace=True) # different pour ECMWF car: pas d'espace=0.4
    df2.drop(df2.loc[df2['Longitude'] % 0.5 !=0].index, inplace=True) 

    df2.loc[df2['Latitude']>180, 'Latitude'] = df2.loc[df2['Latitude']>180, 'Latitude']-360 #on garde les latitudes et longitudes entre -180 et 180
    df2.loc[df2['Longitude']>180, 'Longitude'] = df2.loc[df2['Longitude']>180, 'Longitude'] -360

    os.remove('temp_00.csv')
    df2.set_index(['Latitude','Longitude','validityDate','validityTime'], inplace=True)
    
    return df2