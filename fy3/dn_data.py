from __future__ import annotations
from typing_extensions import Literal

import numpy as np
import matplotlib.pyplot as plt

from fy3.dn_data_sec import DnDataSectors


SECTOR_SIZE = 292
SENSOR_COUNT = 40


class DnData:
    '''
    TODO: Написать описание.
    '''

    def __init__(self, data: np.array) -> None:
        '''
        TODO: 
        '''
        
        self.__data = data


    def get_sections(self, 
                 sectors_size: int = SECTOR_SIZE,
                 sensors_count: int = SENSOR_COUNT) -> DnDataSectors:
        '''
        TODO: 
        '''
        
        return DnDataSectors(self.data, sectors_size, sensors_count)


    def imshow(self, figsize: (int, int) = (10, 10), title: str = '') -> None:
        '''
        TODO: 
        '''

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
