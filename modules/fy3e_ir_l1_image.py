from __future__ import annotations
from typing import List

import h5py
import numpy as np


TRIM = 6132
SECTOR_SIZE = 292
SENSOR_COUNT = 40


class DnData:
    def __init__(self, data: np.array, trim_to: int = TRIM):
        self.data = data[:, :trim_to]

    def get_sections(self, 
                 sectors_size: int = SECTOR_SIZE,
                 sensors_count: int = SENSOR_COUNT) -> np.array:
        
        slices_data = []

        for i in range(self.data.shape[0] // sensors_count):
            sectors = []
            
            for j in range(self.data.shape[1] // sectors_size):
                sectors.append(self.data[i * sensors_count: sensors_count + (i * sensors_count), 
                                        j * sectors_size: sectors_size + (j * sectors_size)])
            
            slices_data.append(np.array(sectors))

        return np.array(slices_data)
        

class FY3EIrDnImg:
    def __init__(self, file_path: str) -> None:
        raw_data = h5py.File(file_path, mode='r')

        self.dn_data_b6 = DnData(np.array(raw_data['Data']['EV_250_Emissive_b6']))
        self.dn_data_b7 = DnData(np.array(raw_data['Data']['EV_250_Emissive_b7']))

   