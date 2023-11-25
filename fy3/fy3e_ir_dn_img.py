from __future__ import annotations

import h5py
import numpy as np

from fy3.dn_data import DnData

'''
TODO: 
'''

class WrongSatellite(Exception):
    pass


class FY3EIrDnImg:
    '''
    TODO: Написать описание.
    '''

    def __init__(self, file_path: str) -> None:
        raw_data = h5py.File(file_path, mode='r')
        metadata = dict(raw_data.attrs.items())

        self.__satellite_name = metadata['Satellite Name'].decode('utf-8')

        if self.__satellite_name != 'FY-3E':
            raise WrongSatellite('Satellite is not FY-3E.')

        self.__dn_data_b6 = DnData(np.array(raw_data['Data']['EV_250_Emissive_b6']))
        self.__dn_data_b7 = DnData(np.array(raw_data['Data']['EV_250_Emissive_b7']))

        self.__kmirror_side = np.array(raw_data['Calibration']['Kmirror_Side'])

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
    def kmirror_side(self) -> np.array:
        return self.__kmirror_side
