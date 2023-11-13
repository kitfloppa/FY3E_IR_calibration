from __future__ import annotations

import os
import h5py
import argparse


def main(image_path: str, georef_path: str, dirout_path: str) -> None: 
    file_name = os.path.basename(image_path).split('.')
    
    if len(file_name) != 2:
        raise NameError('File has the wrong name, try "filename".HDF')
    
    result_path = dirout_path + '/' + file_name[0] + '_WITH_GEO.' + file_name[1]
    
    data = h5py.File(image_path, 'r')
    geo = h5py.File(georef_path, 'r')
    result = h5py.File(result_path, 'w')

    for key in data.keys():
        data.copy(key, result)
    
    geo.copy(geo['Latitude'], result['/'], 'Latitude')
    geo.copy(geo['Longitude'], result['/'], 'Longitude')

    data.close()
    geo.close()
    result.close()

    print('File was created successfully !!!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='add_georeferencing.py',
                                     description='''Algorithm for adding georeferencing to L1 
                                                    satellite images for FY-3E satellite.\n\n
                                                    The file format is HDF.''')
    
    parser.add_argument('-i', '--image', type=str, help='path to L1 level satellite images without \
                                                        georeferencing (HDF format)', metavar='')
    
    parser.add_argument('-g', '--georef', type=str, help='path to georeferencing file (HDF format)', metavar='')
    parser.add_argument('-d', '--dirout', type=str, default='', help='path to output directory', metavar='')
    
    args = parser.parse_args()
    
    main(args.image, args.georef, args.dirout)