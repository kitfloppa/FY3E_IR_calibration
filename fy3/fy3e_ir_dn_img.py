from __future__ import annotations

import h5py
import numpy as np

from fy3.dn_data import DnData


class WrongSatellite(Exception):
    pass


class FY3EIrDnImg:
    '''
    TODO: Написать описание.
    '''

    def __init__(self, img_file_path: str, goe_file_path: str = '') -> None:
        '''
        TODO: 
        '''

        if goe_file_path:
            geo_raw_data = h5py.File(goe_file_path, mode='r')
            geo_metadata = dict(geo_raw_data.attrs.items())

            self.__latitude = DnData(np.array(geo_raw_data['Latitude']))
            self.__longitude = DnData(np.array(geo_raw_data['Longitude']))

            if geo_metadata['Satellite Name'].decode('utf-8') != 'FY-3E':
                raise WrongSatellite('Satellite is not FY-3E.')

        img_raw_data = h5py.File(img_file_path, mode='r')
        img_metadata = dict(img_raw_data.attrs.items())

        self.__satellite_name = img_metadata['Satellite Name'].decode('utf-8')

        if self.__satellite_name != 'FY-3E':
            raise WrongSatellite('Satellite is not FY-3E.')

        self.__dn_data_b6 = DnData(np.array(img_raw_data['Data']['EV_250_Emissive_b6']))
        self.__dn_data_b7 = DnData(np.array(img_raw_data['Data']['EV_250_Emissive_b7']))

        self.__kmirror_side = np.array(img_raw_data['Calibration']['Kmirror_Side'])


    @property
    def satellite_name(self) -> str:
        return self.__satellite_name


    @property
    def dn_data_b6(self) -> DnData:
        return self.__dn_data_b6


    @property
    def dn_data_b7(self) -> DnData:
        return self.__dn_data_b7


    @property
    def latitude(self) -> DnData:
        return self.__latitude


    @property
    def longitude(self) -> DnData:
        return self.__longitude


    @property
    def kmirror_side(self) -> np.array:
        return self.__kmirror_side
