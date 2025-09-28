#script 3

import pandas as pd
import json

df = pd.read_csv('cartesian_positions_and_velocities.csv')

with open('info.json', 'r') as f:
    info = json.load(f)
x = 2
df['File'] = df['Station'].map(info)
df.to_csv('Station info.csv')