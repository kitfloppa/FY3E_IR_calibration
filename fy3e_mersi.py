from __future__ import annotations

import io
import struct
import datetime
import numpy as np


HEADER_SIZE = 1159544
METADATA_SIZE = 554
SV_SCAN_SIZE = 25920
VOC_SCAN_SIZE = 17280
BB_SCAN_SIZE = 8640
TRANSPORT_BLOCK_SIZE = 9216
KM_DATA_SIZE = 2304

SYNCHROSERIES_SIZE = 10

SENSORS_COUNT = 40

# Colibrators
SV_BLOCK_SIZE = 216
SV_DN_INLINE_COUNT = 144

VOC_BLOCK_SIZE = 144
VOC_DN_INLINE_COUNT = 96

BB_BLOCK_SIZE = 72
BB_DN_INLINE_COUNT = 48


def read_uint12(data_chunk):
    data = np.frombuffer(data_chunk, dtype=np.uint8)
    fst_uint8, mid_uint8, lst_uint8 = np.reshape(data, (data.shape[0] // 3, 3)).astype(np.uint16).T
    fst_uint12 = (fst_uint8 << 4) + (mid_uint8 >> 4)
    snd_uint12 = ((mid_uint8 % 16) << 8) + lst_uint8
    
    return np.reshape(np.concatenate((fst_uint12[:, None], snd_uint12[:, None]), axis=1), 2 * fst_uint12.shape[0])


class MersiScanlineMetadata:
    def __init__(self, frame_count, day_count, time_interval, time_count, cal_signal_dn, bracket_calibrator_temp_dn,
                 voc_temp_dn, cool_temp_voltage_dn, instrument_status_records, status_telemetry, k_mirror_motor_temp_dn,
                 main_mirror_temp_dn, refl_mirror_temp_dn, vis_detector_temp_dn, near_ir_detector_temp_dn,
                 swir_drv_temp_dn, vis_drv_temp_dn, ir_drv_temp_dn, obs_mode_voc, bb_temp_cnt, scans_type, obs_mode):
        self.frame_count = frame_count
        self.day_count = day_count
        self.time_interval = time_interval
        self.time_count = time_count
        self.cal_signal_dn = cal_signal_dn
        self.bracket_calibrator_temp_dn = bracket_calibrator_temp_dn
        self.voc_temp_dn = voc_temp_dn
        self.cool_temp_voltage_dn = cool_temp_voltage_dn
        self.instrument_status_records = instrument_status_records
        self.status_telemetry = status_telemetry
        self.k_mirror_motor_temp_dn = k_mirror_motor_temp_dn
        self.main_mirror_temp_dn = main_mirror_temp_dn
        self.refl_mirror_temp_dn = refl_mirror_temp_dn
        self.vis_detector_temp_dn = vis_detector_temp_dn
        self.near_ir_detector_temp_dn = near_ir_detector_temp_dn
        self.swir_drv_temp_dn = swir_drv_temp_dn
        self.vis_drv_temp_dn = vis_drv_temp_dn
        self.ir_drv_temp_dn = ir_drv_temp_dn
        self.obs_mode_voc = obs_mode_voc
        self.bb_temp_cnt = bb_temp_cnt
        self.scans_type = scans_type
        self.obs_mode = obs_mode


class ParseResultMersi:
    def __init__(self, 
                 b6: np.ndarray, 
                 b7: np.ndarray,
                 km_1: np.ndarray,
                 km_2: np.ndarray,
                 km_3: np.ndarray,
                 km_4: np.ndarray,
                 metadata: list[MersiScanlineMetadata],
                 sv_dn: list[bytes],
                 voc_dn: list[bytes],
                 bb_dn: list[bytes]) -> None:
        
        self.b6 = b6
        self.b7 = b7
        self.km_1 = km_1
        self.km_2 = km_2
        self.km_3 = km_3
        self.km_4 = km_4
        self.metadata = metadata
        self.sv_dn = sv_dn
        self.voc_dn = voc_dn
        self.bb_dn = bb_dn

    
class ParseTelemetryResult:
    def __init__(self, b6, b7, km) -> None:
        self.b6 = b6
        self.b7 = b7
        self.km = km


def parse_scanline_metadata(stream: io.BufferedIOBase) -> MersiScanlineMetadata:
        data = stream.read(METADATA_SIZE)

        frame_count = struct.unpack('i', data[:4])[0]
        day_count = datetime.date(2000, 1, 1) + datetime.timedelta(days=struct.unpack('H', data[8:10])[0])
        time_interval = struct.unpack('I', data[10:14])[0]
        time_count = struct.unpack('Q', data[14:22])[0]

        cal_signal_dn = np.zeros(5, dtype=np.uint16)
        bracket_calibrator_temp_dn = np.zeros(2, dtype=np.uint16)
        voc_temp_dn = 0
        cool_temp_voltage_dn = np.zeros(3, dtype=np.uint16)
        instrument_status_records = np.zeros(3, dtype=np.uint16)
        status_telemetry = np.zeros(2, dtype=np.uint16)
        k_mirror_motor_temp_dn = np.zeros(4, dtype=np.uint16)
        main_mirror_temp_dn = 0
        refl_mirror_temp_dn = 0
        vis_detector_temp_dn = 0
        near_ir_detector_temp_dn = 0
        swir_drv_temp_dn = 0
        vis_drv_temp_dn = 0
        ir_drv_temp_dn = np.zeros(2, dtype=np.uint16)
        obs_mode_voc = np.zeros(3, dtype=np.uint16)
        bb_temp_cnt = np.zeros(7, dtype=np.uint16)
        scans_type = 0
        obs_mode = 0

        telemetry_info = data[0x43:0x43 + 0x1e3]

        buffer_17 = telemetry_info[0x3f:]
        cal_signal_dn[:2] = read_uint12(buffer_17[:3])

        buffer_1 = buffer_17[0x3:]
        cal_signal_dn[2:4] = read_uint12(buffer_1[:3])

        buffer_2 = buffer_1[0x3:]
        cal_signal_dn[4], bracket_calibrator_temp_dn[0] = read_uint12(buffer_2[:3])
        bracket_calibrator_temp_dn[1], voc_temp_dn = read_uint12(buffer_2[3:6])

        buffer_3 = telemetry_info[0x4b:]
        cool_temp_voltage_dn[:2] = read_uint12(buffer_3[:3])

        buffer_4 = buffer_3[0x3:]
        cool_temp_voltage_dn[2], instrument_status_records[0] = read_uint12(buffer_4[:3])

        buffer_5 = buffer_4[0x3:]
        instrument_status_records[1], status_telemetry[0] = read_uint12(buffer_5[:3])
        status_telemetry[1], _ = read_uint12(buffer_5[3:6])

        buffer_6 = telemetry_info[0x54:]
        k_mirror_motor_temp_dn[:2] = read_uint12(buffer_6[:3])

        buffer_7 = buffer_6[0x3:]
        k_mirror_motor_temp_dn[2:4] = read_uint12(buffer_7[:3])

        buffer_8 = buffer_7[0x3:]
        main_mirror_temp_dn, refl_mirror_temp_dn = read_uint12(buffer_8[:3])

        buffer_9 = buffer_8[0x3:]
        vis_detector_temp_dn, near_ir_detector_temp_dn = read_uint12(buffer_9[:3])

        buffer_10 = buffer_9[0x3:]
        swir_drv_temp_dn, vis_drv_temp_dn = read_uint12(buffer_10[:3])

        buffer_11 = buffer_10[0x3:]
        ir_drv_temp_dn[:] = read_uint12(buffer_11[:3])

        buffer_12 = buffer_11[0x3:]
        instrument_status_records[2], obs_mode_voc[0] = read_uint12(buffer_12[:3])
        obs_mode_voc[1:] = read_uint12(buffer_12[3:6])

        buffer_14 = telemetry_info[0x1d7:]
        bb_temp_cnt[:2] = read_uint12(buffer_14[:3])

        buffer_15 = buffer_14[0x3:]
        bb_temp_cnt[2:4] = read_uint12(buffer_15[:3])

        buffer_16 = buffer_15[0x3:]
        bb_temp_cnt[4:6] = read_uint12(buffer_16[:3])
        bb_temp_cnt[6], flags = read_uint12(buffer_16[3:6])
        scans_type = flags & 1
        obs_mode = ((flags & 0x10) >> 4)
        obs_mode = obs_mode & 1, (obs_mode >> 1) & 1, (obs_mode >> 2) & 1, (obs_mode >> 3) & 1

        return MersiScanlineMetadata(frame_count, day_count, time_interval, time_count, cal_signal_dn,
                                     bracket_calibrator_temp_dn, voc_temp_dn, cool_temp_voltage_dn,
                                     instrument_status_records, status_telemetry, k_mirror_motor_temp_dn,
                                     main_mirror_temp_dn,
                                     refl_mirror_temp_dn, vis_detector_temp_dn, near_ir_detector_temp_dn,
                                     swir_drv_temp_dn, vis_drv_temp_dn,
                                     ir_drv_temp_dn, obs_mode_voc, bb_temp_cnt, scans_type, obs_mode)


def parse(stream: io.BufferedIOBase, scanline_number: int) -> ParseResultMersi:
    data = stream.read(HEADER_SIZE)

    section_1, section_2 = [], []
    section_3, section_4, section_5, section_6 = [], [], [], []

    data2_agg, data3_agg, data4_agg, data5_agg = [], [], [], []

    for _ in range(scanline_number):
        data2 = parse_scanline_metadata(stream)
        data2_agg.append(data2)

        data2 = stream.read(SYNCHROSERIES_SIZE)
        data3 = stream.read(SV_SCAN_SIZE)
        data3_agg.append(data3)

        data2 = stream.read(SYNCHROSERIES_SIZE)
        data4 = stream.read(VOC_SCAN_SIZE)
        data4_agg.append(data4)

        data2 = stream.read(SYNCHROSERIES_SIZE)
        data5 = stream.read(BB_SCAN_SIZE)
        data5_agg.append(data5)
        
        for _ in range(SENSORS_COUNT):
            data = stream.read(SYNCHROSERIES_SIZE)
            data = stream.read(TRANSPORT_BLOCK_SIZE)
            section_1.append(read_uint12(data))

        for _ in range(SENSORS_COUNT):
            data = stream.read(SYNCHROSERIES_SIZE)
            data = stream.read(TRANSPORT_BLOCK_SIZE)
            section_2.append(read_uint12(data))
            
        for _ in range(SENSORS_COUNT):
            data = stream.read(SYNCHROSERIES_SIZE)
            data = stream.read(TRANSPORT_BLOCK_SIZE)
            
            section_3.append(read_uint12(data[:KM_DATA_SIZE]))
            section_4.append(read_uint12(data[KM_DATA_SIZE:KM_DATA_SIZE * 2]))
            section_5.append(read_uint12(data[KM_DATA_SIZE * 2:KM_DATA_SIZE * 3]))
            section_6.append(read_uint12(data[KM_DATA_SIZE * 3:KM_DATA_SIZE * 4]))

    b6_image = np.array(section_1)
    b7_image = np.array(section_2)
    km_1_image = np.array(section_3)
    km_2_image = np.array(section_4)
    km_3_image = np.array(section_5)
    km_4_image = np.array(section_6)
    data2_agg = data2_agg
    data3_agg = data3_agg
    data4_agg = data4_agg
    data5_agg = data5_agg

    return ParseResultMersi(b6_image,
                            b7_image,
                            km_1_image,
                            km_2_image,
                            km_3_image,
                            km_4_image,
                            data2_agg,
                            data3_agg,
                            data4_agg,
                            data5_agg)


def parse_telemetry_data(data: np.ndarray, scan_size: int, block_size: int, dn_inline_coun: int) -> ParseTelemetryResult:
    b6_data = np.zeros((len(data), SENSORS_COUNT, dn_inline_coun))
    b7_data = np.zeros((len(data), SENSORS_COUNT, dn_inline_coun))
    km_data = np.zeros((len(data), SENSORS_COUNT, dn_inline_coun))
    
    for i, block_all in enumerate(data):
        blocks = []
        
        for block_index in range(0, scan_size, block_size):
            blocks.append(read_uint12(block_all[block_index:block_index + block_size]))

        b6_data[i] = blocks[:SENSORS_COUNT]
        b7_data[i] = blocks[SENSORS_COUNT:SENSORS_COUNT * 2]
        km_data[i] = blocks[SENSORS_COUNT * 2:SENSORS_COUNT * 3]

    return ParseTelemetryResult(b6_data, b7_data, km_data)
