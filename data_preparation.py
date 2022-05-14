from ecg_gudb_database import GUDb
from hrv import HRV
from qrs_detection import QRS_detection as detect
import numpy as np
import pandas as pd


def cal_single_eigen_values(subject_no, subject_action):
    array = []
    sample_rate = GUDb.fs
    hrv_class = HRV(sample_rate)
    max_bpm = 150
    data = pd.read_excel("data.xlsx",
                         sheet_name=str(subject_no) + subject_action,
                         header=0, usecols="B:F")[0]
    rr = detect(data, sample_rate, max_bpm)
    array.append(hrv_class.pNN50(rr))
    array.append(hrv_class.RMSSD(rr))
    hr = hrv_class.HR(rr)
    array.append(np.mean(hr))
    array.append(np.std(hr))
    array.append(hrv_class.fAnalysis(rr))
    array.append(hrv_class.lf)
    array.append(hrv_class.hf)
    return array


def cal_all_eigen_values():
    values = []
    for i in range(GUDb.total_subjects):
        values.append(cal_single_eigen_values(i, '-sitting'))
        values.append(cal_single_eigen_values(i, '-maths'))
    return values


def write_to_excel(subject_no, subject_action, writer):
    ecg_class = GUDb(subject_no, subject_action)
    arrays = np.vstack((ecg_class.cs_V2_V1, ecg_class.einthoven_I,
                        ecg_class.einthoven_II, ecg_class.einthoven_III))
    dataframe = pd.DataFrame(arrays).T
    dataframe.to_excel(writer, str(subject_no) + '-' + subject_action)


# total_subjects = GUDb.total_subjects
# writer = pd.ExcelWriter("raw_data.xlsx")
# for i in range(total_subjects):
#     for action in GUDb.experiments[0:2]:
#         write_to_excel(i, action, writer)
# writer.save()
# writer.close()
# # print(ecg_class.einthoven_I)
