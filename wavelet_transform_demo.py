import pandas as pd
import matplotlib.pyplot as plt
import pywt as pw


data = pd.read_excel("data.xlsx", sheet_name="0-sitting",
                     header=0, usecols="B:F")
ecg = data[0].T.values.tolist()
# x = len(ecg)
coeffs = pw.swt(ecg, wavelet="haar", level=2, start_level=0, axis=-1)
d2 = coeffs[1][1]  # 2nd level detail coefficients
plt.subplot(2, 1, 1)
plt.xlim(0, 1000)
plt.plot(ecg)
plt.subplot(2, 1, 2)
plt.xlim(0, 1000)
plt.plot(d2)
plt.show()
