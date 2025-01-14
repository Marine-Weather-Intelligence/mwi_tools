import pandas as pd

def remove_missing_variables(df):
    df2 = df.dropna()
    df3=df2.reset_index(drop=True)
    return df3


def removing_useless_columns(df): 
    cols_to_drop = [col for col in df.columns if col.startswith('round')]
    df = df.drop(columns=cols_to_drop)
    return df


def to_numerical_values(df): 
    df['TWavA'] = pd.to_numeric(df['TWavA'], errors='coerce')
    df['abs_TWavA'] = pd.to_numeric(df['abs_TWavA'], errors='coerce')
    df['TWS'] = pd.to_numeric(df['TWS'], errors='coerce')
    df['TWA'] = pd.to_numeric(df['TWA'], errors='coerce')
    df['abs_TWA'] = pd.to_numeric(df['abs_TWA'], errors='coerce')
    df['speed'] = pd.to_numeric(df['speed'], errors='coerce')
    df['mwd'] = pd.to_numeric(df['mwd'], errors='coerce')
    df['mwp'] = pd.to_numeric(df['mwp'], errors='coerce')
    df['swh'] = pd.to_numeric(df['swh'], errors='coerce')
    return df


def remove_change_of_tack(df): 
    sign_changes = df['TWA'] * df['TWA'].shift(-1) < 0
    indices_to_drop = set(sign_changes[sign_changes].index)  
    indices_to_drop.update(sign_changes[sign_changes].index + 1)
    df = df.drop(indices_to_drop, errors='ignore')
    df=df.reset_index(drop=True)
    return df

# only racing boats --> limit range to do 
def all_the_same_timesteps(df): 
    df['datetime'] = pd.to_datetime(df['datetime'])
    time_diffs = df['datetime'].diff()
    time_diff_counts = time_diffs.value_counts()
    most_frequent_time_diff = time_diff_counts.idxmax() 
    df = df[time_diffs == pd.Timedelta(most_frequent_time_diff)]
    df=df.reset_index(drop=True)
    return df


def removing_supposed_wrong_values(df): 
    ## The goal is to remove values that don't seem logical judged by their previous and following values 
    ## past one and following one have similar conditions but this one changes a lot in speed and a lot in wind conditions
    condition_TWA_TWS = (abs(df['TWA'] - df['TWA'].shift(-1)) >= 10) | \
                    (abs(df['TWS'] - df['TWS'].shift(-1)) >= 10)
    
    similarity_condition = (
        (abs(df['TWA'].shift(1) - df['TWA'].shift(-1)) <= 20) &  # Small difference between i-1 and i+1 for TWA
        (abs(df['TWS'].shift(1) - df['TWS'].shift(-1)) <= 10)    # Small difference between i-1 and i+1 for TWS
    )

    condition_speed = abs(df['speed'] - df['speed'].shift(-1)) >= 5
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    time_diffs = df['datetime'].diff()
    time_diff_counts = time_diffs.value_counts()
    most_frequent_time_diff = time_diff_counts.idxmax() 
    condition_datetime = (df['datetime'].shift(-1) - df['datetime']) == pd.Timedelta(most_frequent_time_diff)
    
    combined_condition = condition_speed & condition_TWA_TWS & similarity_condition & condition_datetime

    indices_matching = df[combined_condition].index.tolist()

    df = df.drop(indices_matching)
    df = df.reset_index(drop=True)

    return df


def slow_with_wind(df):
    df = df[~((df['speed'] < 3) & (df['TWS'] > 5))]
    df=df.reset_index(drop=True)
    return df


def too_close_to_the_wind(df): 
    df = df[~((df['abs_TWA'] < 20) & (df['TWS'] > 10))]
    df = df.reset_index(drop=True)
    return df