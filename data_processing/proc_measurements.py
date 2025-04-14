import time
import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy import optimize


def get_split_times(inj_f_name):
    times = []
    with open(inj_f_name, 'r') as f:
        injections = csv.reader(f, delimiter=',')
        for row in injections:
            s = row[0]
            t = s[20:]
            times.append(float(t))
    return times


def get_split_idx(times, time):
    for i in range(len(times)):
        t = times[i]
        if t < time:
            continue
        else:
            return i
    return -1


def write_csv_results(cir_f_name, cir_data):
    times = cir_data[0, :]
    cir = cir_data[1, :]
    with open(cir_f_name, 'w') as cir_file:
        cir_writer = csv.writer(cir_file, delimiter=',')
        for i in range(len(times)):
            cir_writer.writerow([times[i]] + [cir[i]])


def calc_lin_correction(data, size, start = 0, end = -1):
    beginning = np.mean(data[start:start+size-1])
    ending = np.mean(data[end-size:end])
    slope = (ending - beginning) / len(data[start:end])
    print(slope)
    slope_correction = []
    for i in range(len(data)):
        slope_correction.append(i * slope)
    return slope_correction

def calc_lin_func(slope, offset, times):
    lin_func = []
    for t in times:
        lin_func.append(offset + slope * t)
    return np.asarray(lin_func)


def calc_mse(observed, expected):
    sub = np.subtract(expected, observed)
    squ = np.square(sub)
    mse = np.mean(squ)
    return mse


def model(params: np.ndarray, args):
    slope = params[0]
    offset = params[1]
    data = args[0]
    times = args[1]
    lin_func = calc_lin_func(slope, offset, times)
    return calc_mse(data, lin_func)


def opt_lin_correction(data, times, slope, offset):
    x0 = np.array([slope, offset])
    args = np.array([data, times])
    bnds = ((None, None), (None, None))
    return optimize.minimize(fun=model, x0=x0, args=args, method='SLSQP', bounds=bnds,
                               options={'maxiter': 500, 'disp': False})



def proc_abs_file(file_name, split_times):
    x = []
    timex = []
    ch2_o = []
    ch2 = []
    ch3 = []
    i = 0
    n_imps = -1

    with open(file_name,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        first_line = True
        for row in plots:
            if first_line:
                first_line = False
                continue
            x.append(i)
            timex.append(float(row[0]))
            ch2_o.append(float(row[5]))
            ch3.append(float(row[5]))
            i = i+1

    plt.plot(x, ch2_o, color='g', label="CH2")

    # correct the slope introduced by sensor drift
    slope_correction = calc_lin_correction(ch2_o, 10,
                                           get_split_idx(timex, split_times[0]),
                                           get_split_idx(timex, split_times[-1]))
    # alternative slope correction
    #slope_opt = opt_lin_correction(ch2_o[get_split_idx(timex, split_times[0]):get_split_idx(timex, split_times[-1])],
                                   #timex[get_split_idx(timex, split_times[0]):get_split_idx(timex, split_times[-1])],
                                   #0, 0)
    #slope_correction = calc_lin_func(slope_opt.x[0], 0, timex)
    for i in range(len(timex)):
        ch2.append(ch2_o[i] - slope_correction[i])
    plt.grid(True)
    plt.xlabel('Time')
    plt.ylabel('MHz')
    plt.title('Channel 2 - Absolutwerte')
    plt.legend()
    plt.show()


    # prepare the splits
    split_idxs = []
    for i in range(0, len(split_times)):
        idx = get_split_idx(timex, split_times[i])
        if idx == -1:
            raise ValueError('Times do not match Measurement Input!', split_times[i])
        split_idxs.append(idx)
    n_imps = len(split_times)
    imp_len = float('inf')
    idx_dist = max(split_idxs)
    for i in range(1, len(split_times)):
        d = split_times[i] - split_times[i - 1]
        if d < imp_len:
            imp_len = d
        d = split_idxs[i] - split_idxs[i - 1]
        if d < idx_dist:
            idx_dist = d
    d = max(timex) - split_times[-1]
    if d < imp_len:
        imp_len = d
    d = len(timex) - 1 - split_idxs[-1]
    if d < idx_dist:
        idx_dist = d
    idx_dist = 400

    # do the splits
    splits_list = np.zeros((n_imps, idx_dist))
    for i in range(0, n_imps):
        start_idx = split_idxs[i]
        end_idx = start_idx + idx_dist
        resp = np.array(ch2[start_idx:end_idx])
        resp = resp * -1  # treat absolute value of the frequency shift
        resp = resp - resp[0]
        splits_list[i, :] = resp

    ms = [(n / 100) for n in x[1:idx_dist + 1]]

    for i in range(0, n_imps):
        plt.plot(ms, splits_list[i, :], '--', label=str(i))

    # average the splits
    splits_avg = np.mean(splits_list, axis=0)
    splits_std = np.std(splits_list, axis=0)
    plt.plot(ms, splits_avg, '-', color='black', label='avg')
    plt.xlabel('Time [s]')
    plt.ylabel('Hz')
    plt.title('Splits')
    plt.legend()
    plt.show()
    return np.array([ms, splits_avg])

# process measurement data with absolute frequency shift values
# average values can then be written into output file
f_name = 'Blutmessung_5cm_15cms'
directory = '../data/blood/90degree/'
meas_input = directory+f_name+'.csv'
inj_input = directory+f_name+'.txt'
cir_output = directory+f_name+'_avg.csv'
split_times = get_split_times(inj_input)
cir = proc_abs_file(meas_input, split_times[2:])
write_csv_results(cir_output, cir)

