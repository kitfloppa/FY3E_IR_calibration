from __future__ import annotations
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt

from fy3.dn_data_sec import DnDataSectors


class DnData:
    '''
    TODO: Написать описание.
    '''

    def __init__(self, data: np.array, k_mirror_side: np.array, sector_size: int = 292, sensor_count: int = 40) -> None:
        '''
        TODO: 
        '''
        
        self.__data = DnDataSectors(data, k_mirror_side, sector_size, sensor_count)


    def get_sections(self) -> DnDataSectors:
        '''
        TODO: 
        '''
        
        return self.__data


    def imshow(self, figsize: Tuple[int, int] = (10, 10), title: str = '') -> None:
        '''
        TODO: 
        '''

        fig, ax = plt.subplots(figsize=figsize)
        
        ax.title.set_text(title)
        ax.imshow(self.__data)


    def __str__(self) -> str:
        return f'{self.__data.__str__()}'


    @property
    def shape(self) -> Tuple[int, int]:
        return self.__data.shape


    @property
    def data(self) -> DnDataSectors:
        return self.__data
