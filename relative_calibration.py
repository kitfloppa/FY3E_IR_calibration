from __future__ import annotations
from typing import List

import numpy as np
import fy3e_mersi


SV_SCAN_SIZE = 25920
VOC_SCAN_SIZE = 17280

# Colibrators
SV_BLOCK_SIZE = 216
SV_DN_INLINE_COUNT = 144

VOC_BLOCK_SIZE = 144
VOC_DN_INLINE_COUNT = 96

BB_BLOCK_SIZE = 72
BB_DN_INLINE_COUNT = 48


def mean_all_data(data: np.ndarray) -> np.ndarray:
    data_1_2_mirrors = np.stack([data[::2], data[1::2]])

    return np.full(2, np.mean(data_1_2_mirrors))


def mean_by_sensor_data(data: np.ndarray) -> np.ndarray:
    data_1_2_mirrors = np.stack([data[::2], data[1::2]])
    
    return np.mean(data_1_2_mirrors, axis=(1, 3))


def coeff_calulation(mean_all_1: np.ndarray, mean_all_2: np.ndarray, mean_by_sensor_1: np.ndarray, mean_by_sensor_2: np.ndarray) -> List[float, float]:
    alpha = (mean_all_2[..., None] - mean_all_1[..., None]) / (mean_by_sensor_2 - mean_by_sensor_1)
    beta = mean_all_1[..., None] - alpha * mean_by_sensor_1

    return alpha, beta


def coeff_calulation_b6(sv_b6_data: np.ndarray, voc_b6_data: np.ndarray) -> List[np.ndarray, np.ndarray]:
    sv_b6_data = sv_b6_data[2:]
    sv_b6_mean_all = mean_all_data(sv_b6_data)
    sv_b6_sensors_mean = mean_by_sensor_data(sv_b6_data)

    voc_b6_data = voc_b6_data[2:]
    voc_b6_mean_all = mean_all_data(voc_b6_data)
    voc_b6_sensors_mean = mean_by_sensor_data(voc_b6_data)

    return coeff_calulation(sv_b6_mean_all, voc_b6_mean_all, sv_b6_sensors_mean, voc_b6_sensors_mean)


def apply_coeff_for_image(data: np.array, alpha: float, beta: float, start_mirror_side: int) -> np.array:
    data_corrected = np.zeros(data.shape)

    for i in range(data.shape[0]):
        data_corrected[i] = np.round(alpha[(i // 40 + start_mirror_side + 1) % 2][i % 40] * data[i] + beta[(i // 40 + start_mirror_side + 1) % 2][i % 40])

    return data_corrected


def apply_coeff_for_telemetry(data: np.array, alpha: float, beta: float, start_mirror_side: int) -> np.array:
    data_corrected = np.zeros(data.shape)

    for i in range(data.shape[0]):
        data_corrected[i] = alpha[..., None][(i // 40 + start_mirror_side + 1) % 2] * data[i] + beta[..., None][(i // 40 + start_mirror_side + 1) % 2]

    return data_corrected