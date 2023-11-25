from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from fy3.dn_data_sec import DnDataSectors


TRIM = 6132 # Need for crop useless data
SECTOR_SIZE = 292
SENSOR_COUNT = 40


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
    
    def imshow(self, figsize: (int, int) = (10, 10), title: str = '') -> None:
        fig, ax = plt.subplots(figsize=figsize)
        
        ax.title.set_text(title)
        ax.imshow(self.__data)
    
    def __str__(self) -> str:
        return f'{self.__data.__str__()}'
    
    @property
    def shape(self) -> (int, int):
        return self.__data.shape

    @property
    def data(self) -> np.array:
        return self.__data
