from __future__ import annotations

import h5py
import numpy as np

def crop_image_by_sections(raw_data: np.array, 
                           sectors_size: int = 292, 
                           sensors_count: int = 40) -> np.array:
    slices_data = []

    for i in range(raw_data.shape[0] // sensors_count):
        sectors = []
        
        for j in range(raw_data.shape[1] // sectors_size):
            sectors.append(raw_data[i * sensors_count: sensors_count + (i * sensors_count), 
                                    j * sectors_size: sectors_size + (j * sectors_size)])
        
        slices_data.append(np.array(sectors))

    return np.array(slices_data)


class FY3E_IR_IMAGE:
    def __init__(self, file_path: str) -> None:
        raw_data = h5py.File(file_path)
        
        self.data = raw_data