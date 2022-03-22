from ecg_gudb_database import GUDb
import numpy as np
import pandas as pd


def write_to_excel(subject_no, subject_action, writer):
    ecg_class = GUDb(subject_no, subject_action)
    arrays = np.vstack((ecg_class.cs_V2_V1, ecg_class.einthoven_I,
                        ecg_class.einthoven_II, ecg_class.einthoven_III))
    dataframe = pd.DataFrame(arrays).T
    dataframe.to_excel(writer, str(subject_no) + '-' + subject_action)


total_subjects = GUDb.total_subjects
writer = pd.ExcelWriter("data.xlsx")
for i in range(total_subjects):
    for action in GUDb.experiments[0:2]:
        write_to_excel(i, action, writer)
writer.save()
writer.close()
# print(ecg_class.einthoven_I)
