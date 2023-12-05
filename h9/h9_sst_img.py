from __future__ import annotations

import h5py
import numpy as np

from h9.sst_data import SstData


class WrongSatellite(Exception):
    pass


class H9SstImg:
    '''
    TODO: Написать описание.
    '''

    def __init__(self, file_path: str) -> None:
        '''
        TODO:
        '''

        data = h5py.File(file_path, 'r')
        self.__metadata = {key: value.decode('utf-8') \
                           if isinstance(value, bytes) \
                           else value \
                           for (key, value) in dict(data.attrs.items()).items()}

        if self.__metadata['platform'] != 'Himawari-9':
            raise WrongSatellite('Satellite is not Himawari-9.')
        
        self.__sst = SstData(np.array(data['sea_surface_temperature'][0]))

    @property
    def satellite_name(self) -> str:
        return self.__metadata['platform']
    
    @property
    def sst(self) -> np.array:
        return self.__sst