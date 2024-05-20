import os
import h5py
import argparse
import numpy as np
import pandas as pd

from datetime import datetime


DRIFTER_ID = 2

def main() -> None:
    parser = argparse.ArgumentParser(prog='buoy2csv.py',
                                     description='''buoy.nc to csv''')
    
    parser.add_argument('filename', type=str, help='path to buoy.nc file', metavar='')
    
    args = parser.parse_args()

    data_nc = h5py.File(args.filename)

    platform_type = np.array(data_nc['platform_type'])
    quality_level = np.array(data_nc['quality_level'])

    mask = np.logical_and(platform_type == DRIFTER_ID, quality_level >= 4)

    year = np.array(data_nc['year'])[mask]
    month = np.array(data_nc['month'])[mask]
    day = np.array(data_nc['day'])[mask]
    hour = np.array(data_nc['hour'])[mask]
    minute = np.array(data_nc['minute'])[mask]
    second = np.array(data_nc['second'])[mask]

    sst = np.array(data_nc['sst'])[mask]

    lat = np.array(data_nc['lat'])[mask]
    lon = np.array(data_nc['lon'])[mask]

    time = []

    for i in range(minute.shape[0]):
        time.append(datetime(year[i], month[i], day[i], hour[i], minute[i], second[i]))

    data = pd.DataFrame({'time': pd.to_datetime(time), 'lat': lat, 'lon': lon, 'sst': sst - 273.15})

    data.to_csv(os.path.splitext(args.filename)[0] + '.csv', index=False)

if __name__ == '__main__':
    main()