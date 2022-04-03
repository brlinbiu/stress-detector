import numpy as np
import pywt as pw


def QRS_detection(signal, sample_rate, max_bpm):

    # swt 4 level(according to swt_max_level function)
    (cA4, cD4), (cA3, cD3), (cA2, cD2), (cA1, cD1) = pw.swt(
        signal, wavelet="haar", level=4)
    d3 = cD3  # 2nd level detail coefficients

    # process cD3 efficient, make q peak and r peak more obvious
    avg = np.mean(d3)
    std = np.std(d3)
    sig_thres = [abs(i) if abs(i) > 2.0 * std else 0 for i in d3 - avg]

    # # find the narrowest window
    window = int((60.0 / max_bpm) * sample_rate)
    sig_len = len(signal)
    # # cal the window number
    windows_num = int(sig_len / window)
    map, qrs = [], []

    # iterate all windows
    for i in range(windows_num):
        # start index of current window
        start = i*window
        # end index of current window, if end index bigger than len,
        # end -> len
        end = min([(i + 1) * window, sig_len])
        # find the max value within current
        mx = max(sig_thres[start:end])
        # may have the condition all value within current window are zeros
        # so should tell at this step
        if mx > 0:
            # add k-v pair,k: index correspoding max value, v: max vlaue
            map.append((start + np.argmax(sig_thres[start:end]), mx))

    # check if width of 2 max value is too narrow
    # definition: if width < half of window.
    merge_width = window / 2
    i = 0
    while i < len(map) - 1:
        index = map[i][0]
        if map[i + 1][0] - map[i][0] < merge_width:
            # if latter one's value bigger
            if map[i + 1][1] > map[i][1]:
                # use latter one to append into qrs list
                index = map[i + 1][0]
            # skip latter one
            i += 1
        qrs.append(index)
        i += 1

    # determine exact point of r peak
    check_window = int(sample_rate / 8)
    r_peaks = [0] * len(qrs)
    for i, r_loc in enumerate(qrs):
        start = max(0, r_loc - check_window)
        end = min(sig_len, r_loc + check_window)
        # find max value around the r_loc
        max_val_pierod = np.absolute(
            signal[start:end] - np.mean(signal[start:end]))
        peak = np.argmax(max_val_pierod)
        r_peaks[i] = start + peak

    return r_peaks
