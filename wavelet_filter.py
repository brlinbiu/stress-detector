import numpy as np
import math
import pywt


def sgn(num):
    """
    sgn 函数
    """
    if(num > 0.0):
        return 1.0
    elif(num == 0.0):
        return 0.0
    else:
        return -1.0


def cal_sigma_stsf(cd1, data_len):
    """
    软阈值求 sigma，lambda
    """
    median_cd1 = np.median(cd1)
    sigma = (1.0 / 0.6745) * median_cd1
    lamda = sigma * math.sqrt(2.0 * math.log(float(data_len), math.e))
    return lamda


def cal_sigma_mgtsf(cd1, data_len):
    median_cd1 = np.median(cd1)
    cdn_1 = abs(cd1 - median_cd1)
    sigma = (1.0 / 0.6745) * np.median(cdn_1)
    args = math.sqrt(2.0 * math.log(float(data_len), math.e))
    t = sigma * args
    return sigma, t


def coeffs_filtering_stsf(cdn, lamda):
    for i in range(len(cdn)):
        if (abs(cdn[i]) > lamda/np.log2(2)):
            cdn[i] = sgn(cdn[i]) * (abs(cdn[i]) - lamda/np.log2(2))
        else:
            cdn[i] = 0.0


def coeffs_filtering_mgtsf(cdn, lamda, sigma):
    for i in range(len(cdn)):
        if(abs(cdn[i]) > lamda):
            cdn[i] = (math.pow(cdn[i], 2.0) -
                      math.pow((lamda - sigma), 2.0)) / cdn[i]
        else:
            cdn[i] = 0.0


def wavelet_filtering(input_data):
    data = input_data
    data = (data - min(data)) / (max(data) - min(data))
    data = data.T.values.tolist()
    wave = pywt.Wavelet('db6')
    [ca3, cd3, cd2, cd1] = pywt.wavedec(
        data, wavelet=wave, level=3)
    usecoeffs = []
    usecoeffs.append(ca3)
    # # MGTSF
    sigma, t = cal_sigma_mgtsf(cd1, len(data))
    alpha = 0.4
    lamda = t * alpha
    # # # 软阈值
    # lamda = cal_sigma_stsf(cd1, len(data))
    # 第一层第二层细节去除
    for i in range(len(cd1)):
        cd1[i] = 0.0
    # for i in range(len(cd2)):
    #     cd2[i] = 0.0
    coeffs_filtering_mgtsf(cd2, lamda, sigma)
    # MGTSF 滤波
    coeffs_filtering_mgtsf(cd3, lamda, sigma)
    # # # 软阈值滤波
    # coeffs_filtering_stsf(cd2, lamda)
    # coeffs_filtering_stsf(cd3, lamda)
    # 加入滤波后的细节
    usecoeffs.append(cd3)
    usecoeffs.append(cd2)
    usecoeffs.append(cd1)
    recoeffs = pywt.waverec(usecoeffs, wavelet=wave)
    return recoeffs
