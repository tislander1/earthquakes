# script 2

import os
import numpy as np
import pandas as pd
import json
from time import sleep
from datetime import datetime, date

input_dir = 'time_series_raw'
all_filenames = [f for f in os.listdir(input_dir) if f.endswith('.series.csv')]

reference_date = pd.to_datetime('2000-01-01')
files_containing_series_data = {}

ix = 0
for filename in all_filenames:
    
    if ix % 100 == 0:
        if ix > 0:
            master_df.to_csv(out_file)
            sleep(3)
        out_file = 'earthquakes_'+ str(ix) + '.csv'
        # create a master df to hold next 400 columns (otherwise it gets too large to use)
        # Create the 'days' column
        days = pd.Series(range(9400), name='days')
        # Create the 'datetime' column by adding days to the start date
        datetimes = reference_date + pd.to_timedelta(days, unit='D')
        # Create the DataFrame
        master_df = pd.DataFrame({'days_int': days, 'datetime': datetimes})
        out_file = 'earthquakes_'+ str(ix) + '.csv'
    ix = ix + 1

    print(ix, filename)
    df = pd.read_csv(input_dir + '/' +filename)
    station = filename.replace('.series.csv', '')
    files_containing_series_data[station] = out_file

    df['date'] = pd.to_datetime(dict(year=df.Time_Year, month=df.Time_MM, day=df.Time_DD))
    df['days_int'] = (df['date'] - reference_date).dt.days
    df = df.drop_duplicates(subset='days_int', keep='first')

    # Create a new DataFrame with the necessary columns from `df`
    # and rename them to avoid conflicts during the merge.
    df_to_merge = df[['days_int', 'East (m)', 'North (m)', 'Vertical (m)', 'East_sig (m)', 'North_sig (m)', 'Vertical_sig (m)']].rename(
        columns={'East (m)': str(station)+'.East (m)',
                 'North (m)': str(station)+'.North (m)',
                 'Vertical (m)': str(station)+'.Vertical (m)',
                 'East_sig (m)': str(station)+'.East Sigma (m)',
                 'North_sig (m)': str(station)+'.North Sigma (m)',
                 'Vertical_sig (m)': str(station)+'.Vertical Sigma (m)'}
    )
    # merge columns into master_df, using 'days_int' as the key.
    
    master_df = pd.merge(master_df, df_to_merge, on='days_int', how='left')
    print('df_to_merge_shape', df_to_merge.shape, 'master_df_shape', master_df.shape)

master_df.to_csv(out_file)

with open('info.json', 'w') as f:
    json.dump(files_containing_series_data, f)

x = 2