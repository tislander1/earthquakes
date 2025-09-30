# script 5

import pandas as pd
import numpy as np

def find_nearest_stations(df, station_name, num_stations):
    station_dict = {}
    df['Dist (km)'] = 0
    # df['compass_angle'] = 0
    # df['elevation'] = 0
    for index, row in df.iterrows():
        station_dict[row['Station']] = dict(row)
    x_main = station_dict[station_name]['X pos (mm)']
    y_main = station_dict[station_name]['Y pos (mm)']
    z_main = station_dict[station_name]['Z pos (mm)']

    for k in station_dict:
        station_dict[k]['Dist (km)'] = float(np.sqrt(
            (station_dict[k]['X pos (mm)'] - x_main)**2 +
            (station_dict[k]['Y pos (mm)'] - y_main)**2 +
            (station_dict[k]['Z pos (mm)'] - z_main)**2)) / 1e6
    stations_with_dist_df = pd.DataFrame(list(station_dict.values())).sort_values(by = 'Dist (km)').head(num_stations+1)
    columns_to_drop = [item for item in stations_with_dist_df.columns if 'Unnamed' in item or 'Err' in item]
    if columns_to_drop:
        stations_with_dist_df = stations_with_dist_df.drop(columns = columns_to_drop)
        station_list = list(stations_with_dist_df['Station'])
    return station_list, stations_with_dist_df

def get_training_data(stations_sorted_by_dist_df):
    ix = 0
    for index, row in stations_sorted_by_dist_df.iterrows():
        station = row['Station']
        file = row['File']
        df_in = pd.read_csv('time_series/' + file)
        if ix == 0:
            df_columns = ['days_int', 'datetime']
            df_out = pd.DataFrame(df_in[df_columns])
        df_columns = [station + '.' + 'East (m)',
                      station + '.' + 'North (m)',
                      station + '.' + 'Vertical (m)']
        df_out = pd.concat([df_out, df_in[df_columns]], axis=1)
        ix = ix + 1
    return df_out


station_info = 'Station info 2.csv'
num_stations = 10
station_df = pd.read_csv(station_info)
all_stations_list = list(station_df['Station'])
for station_name in all_stations_list:
    neighbor_stations_list, stations_sorted_by_dist_df = find_nearest_stations(df = station_df,
                                                                station_name = station_name,
                                                                num_stations = num_stations)
    print(stations_sorted_by_dist_df)
    neighbors_df = get_training_data(stations_sorted_by_dist_df)
    neighbors_df.to_csv('dataset/time_series_near_' + str(station_name) +'.csv')
    stations_sorted_by_dist_df.to_csv('dataset/'+ str(station_name) +'_info.csv')
    print(station_name + ' written.')