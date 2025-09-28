# script 0

import os
import pandas as pd

directory = "time_series_raw"
for filename in os.listdir(directory):
    result = pd.read_table(directory + '/' + filename, sep='\s+')
    result.columns = ['Decimal_Year',
                      'East (m)', 'North (m)', 'Vertical (m)',
                      'East_sig (m)', 'North_sig (m)', 'Vertical_sig (m)',
                      'E_N_cor', 'E_V_cor', 'N_V_cor',
                      'Time (sec past J2000)',
                      'Time_Year', 'Time_MM', 'Time_DD', 'Time_HR', 'Time_MN', 'Time_SS']
    filepath_to_write = (directory + '/' + filename) + '.csv'
    result.to_csv(filepath_to_write)
    x = 2