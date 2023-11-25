from __future__ import annotations
from typing import List

import h5py
import numpy as np


TRIM = 6132 # Need for crop useless data
SECTOR_SIZE = 292
SENSOR_COUNT = 40


'''
TODO: Нужно добавить информацию о стороне зеркала для каждого сектора и набора 40-ка сенсоров.
'''


class DnDataSectors:
    '''
    TODO: Написать описание.
    '''
    
    def __init__(self, data: np.array, sectors_size: int, sensors_count: int) -> None:
        if data.ndim != 2:
            raise ValueError('Data is not two-dimensional matrix!')
        
        self.__sectors_size = sectors_size
        self.__sensors_count = sensors_count

        slices_data = []

        for i in range(data.shape[0] // self.sensors_count):
            sectors = []
            
            for j in range(data.shape[1] // self.sectors_size):
                sectors.append(data[i * self.sensors_count: self.sensors_count + (i * self.sensors_count), 
                                        j * self.sectors_size: self.sectors_size + (j * self.sectors_size)])
            
            slices_data.append(np.array(sectors))

        self.__sectors = np.array(slices_data)

    def get_sector_by_index(self, x: int, y: int) -> np.array:
        return self.__sectors[y // self.__sensors_count, x // self.__sectors_size]

    def __str__(self) -> str:
        return f'{self.__sectors.__str__()}'
    
    @property
    def shape(self) -> (int, int):
        return self.__sectors.shape

    @property
    def sectors(self) -> np.array:
        return self.__sectors
    
    @property
    def sectors_size(self) -> int:
        return self.__sectors_size
    
    @property
    def sensors_count(self) -> int:
        return self.__sensors_count


class DnData:
    '''
    TODO: Написать описание.
    '''

    def __init__(self, data: np.array, trim_to: int = TRIM) -> None:
        self.__data = data[:, :trim_to]

    def get_sections(self, 
                 sectors_size: int = SECTOR_SIZE,
                 sensors_count: int = SENSOR_COUNT) -> DnDataSectors:
        
        return DnDataSectors(self.data, sectors_size, sensors_count)
    
    @property
    def shape(self) -> (int, int):
        return self.__data.shape

    @property
    def data(self) -> np.array:
        return self.__data
        

class FY3EIrDnImg:
    '''
    TODO: Написать описание.
    '''

    def __init__(self, file_path: str) -> None:
        raw_data = h5py.File(file_path, mode='r')

        self.__dn_data_b6 = DnData(np.array(raw_data['Data']['EV_250_Emissive_b6']))
        self.__dn_data_b7 = DnData(np.array(raw_data['Data']['EV_250_Emissive_b7']))

    @property
    def dn_data_b6(self) -> DnData:
        return self.__dn_data_b6
    
    @property
    def dn_data_b7(self) -> DnData:
        return self.__dn_data_b7