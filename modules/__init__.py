from __future__ import annotations

import os
import h5py


def fy3e_l1_add_georeferencing(image_file_path: str, geo_file_path: str, dirout_file_path: str) -> None: 
    file_name = [piece.upper() for piece in os.path.basename(image_file_path).split('.')]
    
    if 'HDF' not in file_name:
        raise NameError('File has the wrong name, try "filename".HDF')
    
    result_path = dirout_file_path + '/' + file_name[0] + '_WITH_GEO.' + file_name[1]
    
    data = h5py.File(image_file_path, 'r')
    geo = h5py.File(geo_file_path, 'r')
    result = h5py.File(result_path, 'w')

    for key in data.keys():
        if key != 'Geolocation':
            data.copy(key, result)
    
    geo.copy(geo['Latitude'], result['/'], 'Latitude')
    geo.copy(geo['Longitude'], result['/'], 'Longitude')

    data.close()
    geo.close()
    result.close()

    print('File was created successfully !!!')