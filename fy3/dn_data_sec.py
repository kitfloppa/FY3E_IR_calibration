from __future__ import annotations
from typing import Tuple

import numpy as np


class Sector:
    '''
    TODO: Написать описание.
    '''

    def __init__(self, data: np.array, x_index: int, y_index: int, mirror_side: int) -> None:
        '''
        TODO: Написать описание.
        '''
        
        self.__sector = data
        self.__x_index = x_index
        self.__y_index = y_index
        self.__mirror_side = mirror_side

    def __getitem__(self, item: int | Tuple[int, int] | slice | Tuple[slice, slice]):
        if isinstance(item, int) or isinstance(item, slice):
            return self.__sector[item]
        else:
            return self.__sector[item]
        
    def __str__(self) -> str:
        return f'{self.__sector.__str__()}'

    @property
    def shape(self) -> Tuple[int, int]:
        return self.__sector.shape
    
    @property
    def sectors_index(self) -> Tuple[int, int]:
        return (self.__x_index, self.__y_index)
    
    @property
    def mirror_side(self) -> int:
        return self.__mirror_side
    
    @property
    def sector_data(self) -> np.array:
        return self.__sector


class SectorEx:
    @staticmethod
    def mean(sector: Sector) -> float:
        return np.mean(sector.sector_data)


class DnDataSectors:

    '''
    TODO: Написать описание.
    '''
    
    def __init__(self, data: np.array, k_mirror_side: np.array, sectors_size: int, sensors_count: int) -> None:
        '''
        TODO: 
        '''

        if data.ndim != 2:
            raise ValueError('Data is not two-dimensional matrix.')
        
        self.__sectors_size = sectors_size
        self.__sensors_count = sensors_count
        self.__k_mirror_side = k_mirror_side

        slices_data = []

        for i in range(data.shape[0] // self.sensors_count):
            sectors = []
            
            for j in range(data.shape[1] // self.sectors_size):
                sectors.append(data[i * self.sensors_count: self.sensors_count + (i * self.sensors_count), 
                                        j * self.sectors_size: self.sectors_size + (j * self.sectors_size)])
            
            slices_data.append(np.array(sectors))

        self.__sectors = np.array(slices_data)

    def __getitem__(self, item: int | Tuple[int, int] | slice | Tuple[slice, slice]):
        if isinstance(item, int) or isinstance(item, slice):
            return self.__sectors[item]
        else:
            return self.__sectors[item]

    def __getitem__(self, item: int | Tuple[int, int] | slice | Tuple[slice, slice]):
        if isinstance(item, int) or isinstance(item, slice):
            return self.__sectors[item]
        else:
            return self.__sectors[item]

    def get_sector_by_index(self, x: int, y: int) -> np.array:
        '''
        TODO: 
        '''

        x_index = y // self.__sensors_count
        y_index = x // self.__sectors_size

        return Sector(self.__sectors[x_index, y_index], x_index, y_index, self.__k_mirror_side[x_index])

    def __str__(self) -> str:
        return f'{self.__sectors.__str__()}'
    
    @property
    def shape(self) -> Tuple[int, int, int, int]:
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
