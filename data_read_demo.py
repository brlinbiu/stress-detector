import pandas as pd
import numpy as np
from qrs_detect_demo import QRS_detection

data = pd.read_excel("data.xlsx", sheet_name="0-sitting",
                     header=0, usecols="B:F")
ecg = data[0].T.values

qrs = QRS_detection(ecg, 250, 200)
print(qrs)