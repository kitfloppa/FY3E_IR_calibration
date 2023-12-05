from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

class SstData:
    '''
    TODO: Написать описание.
    '''

    def __init__(self, data: np.array) -> None:
        '''
        TODO: 
        '''

        self.__data = data

    def imshow(self, figsize: (int, int) = (10, 10), title: str = '') -> None:
        '''
        TODO: 
        '''

        fig, ax = plt.subplots(figsize=figsize)
        
        ax.title.set_text(title)
        ax.imshow(self.__data)

    @property
    def shape(self) -> (int. int):
        return self.__data.shape

    @property
    def data(self) -> np.array:
        return self.__data