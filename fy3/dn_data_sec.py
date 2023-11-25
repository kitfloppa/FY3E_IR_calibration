from __future__ import annotations

import numpy as np


class DnDataSectors:
    '''
    TODO: Написать описание.
    '''
    
    def __init__(self, data: np.array, sectors_size: int, sensors_count: int) -> None:
        if data.ndim != 2:
            raise ValueError('Data is not two-dimensional matrix.')
        
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
    def shape(self) -> (int, int, int, int):
        
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
