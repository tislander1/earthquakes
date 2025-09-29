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


station_info = 'Station info 2.csv'
station_name = 'JLN5'
num_stations = 10

station_df = pd.read_csv(station_info)
station_list, stations_with_dist_df = find_nearest_stations(df=station_df,
                                                            station_name=station_name,
                                                            num_stations=num_stations)
print(stations_with_dist_df)

