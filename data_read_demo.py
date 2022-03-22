import pandas as pd
import numpy as np

data = pd.read_excel("data.xlsx", sheet_name="0-sitting",
                     header=0, usecols="B:F")
ecg = data[0].T.values
