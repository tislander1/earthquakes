# script 1

import pandas as pd

with open('cartesian_positions_and_velocities.html') as f:
    data = f.readlines()
    data = data[6:] # get rid of first lines
all_fields = []
for ix in range(len(data)):
    line = data[ix]
    if ix % 2 == 0:
        fields1 = line.split()
        x = 2
    else:
        fields2 = line.split()
        fields = fields1 + fields2
        all_fields.append(fields)
df = pd.DataFrame(all_fields)
df.columns = ['Station', 'POS',
              'X pos (mm)', 'Y pos (mm)', 'Z pos (mm)',
              'Err X pos (mm)', 'Err Y pos (mm)', 'Err Z pos (mm)',
              'Station1', 'VEL', 'X vel (mm/yr)', 'Y vel (mm/yr)', 'Z vel (mm/yr)',
              'Err X vel (mm/yr)', 'Err Y vel (mm/yr)', 'Err Z vel (mm/yr)']
df = df.drop(columns = ['POS', 'VEL', 'Station1'])
df.to_csv('cartesian_positions_and_velocities.csv')
x = 2