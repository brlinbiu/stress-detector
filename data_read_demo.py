import pandas as pd

data = pd.read_excel("data.xlsx", sheet_name="0-sitting",
                     header=0, usecols="B:F")
ecg = data[0].T.values

# qrs = QRS_detection(ecg, 250, 200)
# print(qrs)
