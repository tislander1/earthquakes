# script 4

import plotly.express as px
import pandas as pd
import numpy as np

def rect_to_polar_igs14_frame(vec):
    #converts from the x,y,z frame into lat,long,elevation

    vec = vec / 1e3 # mm to meters
    rad_2_deg = 180 / np.pi
    a = 6378137.0 #semimajor axis of earth, meters
    flattening = 1/298.257222101
    e_squared = 2*flattening - flattening**2    # squared first eccentricity

    longitude_rad = np.atan2(vec[1], vec[0])
    longitude_deg = longitude_rad * rad_2_deg

    # initial guesses for radius and latitude
    radius = np.linalg.norm(vec)
    p = np.sqrt(vec[0]**2 + vec[1]**2)  # distance to z axis
    latitude_rad = np.atan2(vec[2], p * (1 - e_squared))
    latitude_deg = latitude_rad * rad_2_deg

    for ix in range(5):
        N = a / np.sqrt(1 - e_squared * np.sin(latitude_rad)**2)    # N = radius of curvature in the prime vertical
        latitude_rad = np.atan2(vec[2] + e_squared * N * np.sin(latitude_rad), p)
        latitude_deg = latitude_rad * rad_2_deg
        x = 2
    latitude_deg = latitude_rad * rad_2_deg
    height_igs14 = p/(np.cos(latitude_rad)) - N
    return {'long': float(longitude_deg), 'lat': float(latitude_deg), 'elev_IGS14_ft': 3.28084*float(height_igs14)}


update_csv = True
if update_csv:
    df = pd.read_csv('Station info.csv')

    df['Long (deg)'] = 0.0
    df['Lat (deg)'] = 0.0
    df['Elev (ft) IGS14'] = 0.0

    for index, row in df.iterrows():
        x = 2
        xyz = np.array([row['X pos (mm)'], row['Y pos (mm)'], row['Z pos (mm)']])
        latlongheight = rect_to_polar_igs14_frame(xyz)
        df.loc[index, 'Long (deg)'] = latlongheight['long']
        df.loc[index, 'Lat (deg)'] = latlongheight['lat']
        df.loc[index, 'Elev (ft) IGS14'] = latlongheight['elev_IGS14_ft']
    df.to_csv('Station info 2.csv', index=False)

fig = px.scatter_3d(df, x='X pos (mm)', y='Y pos (mm)', z='Z pos (mm)', hover_data=['Station', 'Lat (deg)', 'Long (deg)'])
fig.show()